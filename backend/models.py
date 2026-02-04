from database import execute_query, execute_one
import json

# User Models
def create_user(email, password_hash, full_name, phone=None, address=None):
    """Create a new user"""
    query = """
        INSERT INTO users (email, password_hash, full_name, phone, address)
        VALUES (%s, %s, %s, %s, %s)
    """
    return execute_query(query, (email, password_hash, full_name, phone, address))

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT * FROM users WHERE email = %s"
    return execute_one(query, (email,))

def get_user_by_id(user_id):
    """Get user by ID"""
    query = "SELECT id, email, full_name, phone, address, created_at FROM users WHERE id = %s"
    return execute_one(query, (user_id,))

# Admin Models
def get_admin_by_username(username):
    """Get admin by username"""
    query = "SELECT * FROM admin_users WHERE username = %s"
    return execute_one(query, (username,))

# Product Models
def get_all_products(limit=50, offset=0, category_id=None, search=None, brand=None):
    """Get all products with optional filters"""
    conditions = []
    params = []
    
    if category_id:
        conditions.append("category_id = %s")
        params.append(category_id)
    
    if search:
        conditions.append("(name LIKE %s OR description LIKE %s OR brand LIKE %s)")
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])
    
    if brand:
        conditions.append("brand = %s")
        params.append(brand)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE {where_clause}
        ORDER BY p.created_at DESC
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])
    
    return execute_query(query, tuple(params), fetch=True)

def get_product_by_id(product_id):
    """Get product by ID"""
    query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s
    """
    return execute_one(query, (product_id,))

def get_featured_products(limit=6):
    """Get featured products"""
    query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_featured = TRUE
        ORDER BY p.created_at DESC
        LIMIT %s
    """
    return execute_query(query, (limit,), fetch=True)

def create_product(name, brand, category_id, price, discount_price, description, specifications, image_url, stock_quantity, is_featured=False):
    """Create a new product"""
    query = """
        INSERT INTO products (name, brand, category_id, price, discount_price, description, specifications, image_url, stock_quantity, is_featured)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    specs_json = json.dumps(specifications) if isinstance(specifications, dict) else specifications
    return execute_query(query, (name, brand, category_id, price, discount_price, description, specs_json, image_url, stock_quantity, is_featured))

def update_product(product_id, **kwargs):
    """Update a product"""
    allowed_fields = ['name', 'brand', 'category_id', 'price', 'discount_price', 'description', 'specifications', 'image_url', 'stock_quantity', 'is_featured']
    updates = []
    params = []
    
    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            updates.append(f"{key} = %s")
            if key == 'specifications' and isinstance(value, dict):
                value = json.dumps(value)
            params.append(value)
    
    if not updates:
        return False
    
    params.append(product_id)
    query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
    execute_query(query, tuple(params))
    return True

def delete_product(product_id):
    """Delete a product"""
    query = "DELETE FROM products WHERE id = %s"
    execute_query(query, (product_id,))
    return True

# Cart Models
def get_user_cart(user_id):
    """Get user's cart items"""
    query = """
        SELECT c.*, p.name, p.price, p.discount_price, p.image_url, p.brand, p.stock_quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """
    return execute_query(query, (user_id,), fetch=True)

def add_to_cart(user_id, product_id, quantity=1):
    """Add item to cart or update quantity if exists"""
    query = """
        INSERT INTO cart (user_id, product_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity + %s
    """
    return execute_query(query, (user_id, product_id, quantity, quantity))

def update_cart_item(cart_id, quantity):
    """Update cart item quantity"""
    query = "UPDATE cart SET quantity = %s WHERE id = %s"
    execute_query(query, (quantity, cart_id))
    return True

def remove_from_cart(cart_id, user_id):
    """Remove item from cart"""
    query = "DELETE FROM cart WHERE id = %s AND user_id = %s"
    execute_query(query, (cart_id, user_id))
    return True

def clear_user_cart(user_id):
    """Clear all items from user's cart"""
    query = "DELETE FROM cart WHERE user_id = %s"
    execute_query(query, (user_id,))
    return True

# Order Models
def create_order(user_id, total_amount, shipping_address, payment_method='cod'):
    """Create a new order"""
    query = """
        INSERT INTO orders (user_id, total_amount, shipping_address, payment_method)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (user_id, total_amount, shipping_address, payment_method))

def add_order_item(order_id, product_id, quantity, price):
    """Add item to order"""
    query = """
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (order_id, product_id, quantity, price))

def get_user_orders(user_id):
    """Get user's orders"""
    query = """
        SELECT * FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
    """
    return execute_query(query, (user_id,), fetch=True)

def get_order_by_id(order_id, user_id=None):
    """Get order details"""
    if user_id:
        query = "SELECT * FROM orders WHERE id = %s AND user_id = %s"
        return execute_one(query, (order_id, user_id))
    else:
        query = "SELECT * FROM orders WHERE id = %s"
        return execute_one(query, (order_id,))

def get_order_items(order_id):
    """Get order items"""
    query = """
        SELECT oi.*, p.name, p.brand, p.image_url
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    """
    return execute_query(query, (order_id,), fetch=True)

def get_all_orders(limit=50, offset=0):
    """Get all orders (admin)"""
    query = """
        SELECT o.*, u.email, u.full_name
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
        LIMIT %s OFFSET %s
    """
    return execute_query(query, (limit, offset), fetch=True)

def update_order_status(order_id, status=None, payment_status=None):
    """Update order status"""
    updates = []
    params = []
    
    if status:
        updates.append("status = %s")
        params.append(status)
    
    if payment_status:
        updates.append("payment_status = %s")
        params.append(payment_status)
    
    if not updates:
        return False
    
    params.append(order_id)
    query = f"UPDATE orders SET {', '.join(updates)} WHERE id = %s"
    execute_query(query, tuple(params))
    return True

# Category Models
def get_all_categories():
    """Get all categories"""
    query = "SELECT * FROM categories ORDER BY name"
    return execute_query(query, fetch=True)
