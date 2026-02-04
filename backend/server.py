from flask import Flask, request, jsonify
from flask_cors import CORS
import models
from auth import hash_password, verify_password, generate_token, require_auth, require_admin
import json

app = Flask(__name__)
CORS(app)

# ==================== Authentication Routes ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User registration"""
    data = request.json
    
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    phone = data.get('phone')
    address = data.get('address')
    
    if not email or not password or not full_name:
        return jsonify({'error': 'Email, password, and full name are required'}), 400
    
    # Check if user already exists
    existing_user = models.get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 409
    
    # Hash password and create user
    password_hash = hash_password(password)
    user_id = models.create_user(email, password_hash, full_name, phone, address)
    
    if user_id:
        token = generate_token(user_id, email)
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': full_name
            }
        }), 201
    else:
        return jsonify({'error': 'Failed to create user'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = models.get_user_by_email(email)
    
    if not user or not verify_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    token = generate_token(user['id'], user['email'])
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'phone': user.get('phone'),
            'address': user.get('address')
        }
    })

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user info"""
    user = models.get_user_by_id(request.user['user_id'])
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user)

# ==================== Product Routes ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filters"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))
    category_id = request.args.get('category_id')
    search = request.args.get('search')
    brand = request.args.get('brand')
    
    offset = (page - 1) * limit
    
    products = models.get_all_products(
        limit=limit,
        offset=offset,
        category_id=category_id,
        search=search,
        brand=brand
    )
    
    # Parse JSON specifications
    for product in products:
        if product.get('specifications'):
            try:
                product['specifications'] = json.loads(product['specifications'])
            except:
                product['specifications'] = {}
    
    return jsonify({
        'products': products,
        'page': page,
        'limit': limit
    })

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product details"""
    product = models.get_product_by_id(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Parse JSON specifications
    if product.get('specifications'):
        try:
            product['specifications'] = json.loads(product['specifications'])
        except:
            product['specifications'] = {}
    
    return jsonify(product)

@app.route('/api/products/featured', methods=['GET'])
def get_featured():
    """Get featured products"""
    limit = int(request.args.get('limit', 6))
    products = models.get_featured_products(limit)
    
    # Parse JSON specifications
    for product in products:
        if product.get('specifications'):
            try:
                product['specifications'] = json.loads(product['specifications'])
            except:
                product['specifications'] = {}
    
    return jsonify(products)

# ==================== Cart Routes ====================

@app.route('/api/cart', methods=['GET'])
@require_auth
def get_cart():
    """Get user's cart"""
    user_id = request.user['user_id']
    cart_items = models.get_user_cart(user_id)
    
    total = 0
    for item in cart_items:
        item_price = item['discount_price'] if item['discount_price'] else item['price']
        total += float(item_price) * item['quantity']
    
    return jsonify({
        'items': cart_items,
        'total': round(total, 2)
    })

@app.route('/api/cart', methods=['POST'])
@require_auth
def add_to_cart():
    """Add item to cart"""
    user_id = request.user['user_id']
    data = request.json
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    # Check if product exists
    product = models.get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Check stock
    if product['stock_quantity'] < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_id = models.add_to_cart(user_id, product_id, quantity)
    
    return jsonify({
        'message': 'Item added to cart',
        'cart_id': cart_id
    }), 201

@app.route('/api/cart/<int:cart_id>', methods=['PUT'])
@require_auth
def update_cart(cart_id):
    """Update cart item quantity"""
    data = request.json
    quantity = data.get('quantity')
    
    if quantity is None or quantity < 1:
        return jsonify({'error': 'Valid quantity is required'}), 400
    
    success = models.update_cart_item(cart_id, quantity)
    
    if success:
        return jsonify({'message': 'Cart updated successfully'})
    else:
        return jsonify({'error': 'Failed to update cart'}), 500

@app.route('/api/cart/<int:cart_id>', methods=['DELETE'])
@require_auth
def remove_cart_item(cart_id):
    """Remove item from cart"""
    user_id = request.user['user_id']
    success = models.remove_from_cart(cart_id, user_id)
    
    if success:
        return jsonify({'message': 'Item removed from cart'})
    else:
        return jsonify({'error': 'Failed to remove item'}), 500

# ==================== Order Routes ====================

@app.route('/api/orders', methods=['POST'])
@require_auth
def create_order():
    """Create a new order"""
    user_id = request.user['user_id']
    data = request.json
    
    shipping_address = data.get('shipping_address')
    payment_method = data.get('payment_method', 'cod')
    
    if not shipping_address:
        return jsonify({'error': 'Shipping address is required'}), 400
    
    # Get cart items
    cart_items = models.get_user_cart(user_id)
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate total
    total = 0
    for item in cart_items:
        item_price = item['discount_price'] if item['discount_price'] else item['price']
        total += float(item_price) * item['quantity']
    
    # Create order
    order_id = models.create_order(user_id, total, shipping_address, payment_method)
    
    if not order_id:
        return jsonify({'error': 'Failed to create order'}), 500
    
    # Add order items
    for item in cart_items:
        item_price = item['discount_price'] if item['discount_price'] else item['price']
        models.add_order_item(order_id, item['product_id'], item['quantity'], item_price)
    
    # Clear cart
    models.clear_user_cart(user_id)
    
    return jsonify({
        'message': 'Order created successfully',
        'order_id': order_id,
        'total': round(total, 2)
    }), 201

@app.route('/api/orders', methods=['GET'])
@require_auth
def get_orders():
    """Get user's orders"""
    user_id = request.user['user_id']
    orders = models.get_user_orders(user_id)
    
    return jsonify(orders)

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@require_auth
def get_order(order_id):
    """Get order details"""
    user_id = request.user['user_id']
    order = models.get_order_by_id(order_id, user_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    order_items = models.get_order_items(order_id)
    order['items'] = order_items
    
    return jsonify(order)

# ==================== Admin Routes ====================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login"""
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    admin = models.get_admin_by_username(username)
    
    if not admin or not verify_password(password, admin['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = generate_token(admin['id'], admin['email'], is_admin=True)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'admin': {
            'id': admin['id'],
            'username': admin['username'],
            'email': admin['email']
        }
    })

@app.route('/api/admin/products', methods=['POST'])
@require_admin
def admin_create_product():
    """Create a new product (admin only)"""
    data = request.json
    
    required_fields = ['name', 'brand', 'category_id', 'price', 'description', 'image_url', 'stock_quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    product_id = models.create_product(
        name=data['name'],
        brand=data['brand'],
        category_id=data['category_id'],
        price=data['price'],
        discount_price=data.get('discount_price'),
        description=data['description'],
        specifications=data.get('specifications', {}),
        image_url=data['image_url'],
        stock_quantity=data['stock_quantity'],
        is_featured=data.get('is_featured', False)
    )
    
    if product_id:
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
    else:
        return jsonify({'error': 'Failed to create product'}), 500

@app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
@require_admin
def admin_update_product(product_id):
    """Update a product (admin only)"""
    data = request.json
    
    success = models.update_product(product_id, **data)
    
    if success:
        return jsonify({'message': 'Product updated successfully'})
    else:
        return jsonify({'error': 'Failed to update product'}), 500

@app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
@require_admin
def admin_delete_product(product_id):
    """Delete a product (admin only)"""
    success = models.delete_product(product_id)
    
    if success:
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete product'}), 500

@app.route('/api/admin/orders', methods=['GET'])
@require_admin
def admin_get_orders():
    """Get all orders (admin only)"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    offset = (page - 1) * limit
    
    orders = models.get_all_orders(limit, offset)
    
    return jsonify({
        'orders': orders,
        'page': page,
        'limit': limit
    })

@app.route('/api/admin/orders/<int:order_id>', methods=['PUT'])
@require_admin
def admin_update_order(order_id):
    """Update order status (admin only)"""
    data = request.json
    
    status = data.get('status')
    payment_status = data.get('payment_status')
    
    success = models.update_order_status(order_id, status, payment_status)
    
    if success:
        return jsonify({'message': 'Order updated successfully'})
    else:
        return jsonify({'error': 'Failed to update order'}), 500

# ==================== Category Routes ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = models.get_all_categories()
    return jsonify(categories)

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    print("🚀 E-Commerce API Server Starting...")
    print("📍 Server running on http://localhost:5000")
    print("📖 API Documentation:")
    print("   - Auth: /api/auth/signup, /api/auth/login")
    print("   - Products: /api/products, /api/products/featured")
    print("   - Cart: /api/cart")
    print("   - Orders: /api/orders")
    print("   - Admin: /api/admin/login, /api/admin/products, /api/admin/orders")
    app.run(debug=True, host='0.0.0.0', port=5000)
