# M&C E-Commerce - Complete Setup Guide

## Overview
This is a full-stack e-commerce website with:
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL

## Prerequisites
- Python 3.8+
- MySQL Server
- Modern web browser

## Installation Steps

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup MySQL Database
1. Start your MySQL server
2. Create the database and tables:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. Load sample data:
   ```bash
   mysql -u root -p < seed_data.sql
   ```

### 3. Configure Database Connection
Edit `backend/database.py` if needed to update:
- DB_HOST (default: localhost)
- DB_USER (default: root)
- DB_PASSWORD (default: empty)
- DB_NAME (default: ecommerce_db)

### 4. Start the Backend Server
```bash
cd backend
python server.py
```
The API will be running at `http://localhost:5000`

### 5. Open the Frontend
Simply open `frontend/index.html` in your web browser, or use a local server:
```bash
cd frontend
python -m http.server 8000
```
Then visit `http://localhost:8000`

## Default Credentials

### Admin Panel
- **URL**: `frontend/admin/admin-login.html`
- **Username**: admin
- **Password**: admin123

### Sample User
- **Email**: john.doe@example.com
- **Password**: password123

## Features

### User Features
✅ Product browsing with search and filters
✅ Product details with specifications
✅ Shopping cart management
✅ User authentication (login/signup)
✅ Checkout and order placement
✅ Order history and tracking
✅ Responsive design

### Admin Features
✅ Product management (Add, Delete)
✅ Order management (Status updates)
✅ View all orders
✅ Secure admin authentication

## Project Structure
```
M&C e-commerce/
├── backend/
│   ├── server.py           # Main Flask application
│   ├── database.py         # Database connection
│   ├── auth.py             # Authentication logic
│   ├── models.py           # Database models
│   ├── schema.sql          # Database schema
│   ├── seed_data.sql       # Sample data
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Homepage
│   ├── products.html       # Products listing
│   ├── product-detail.html # Product details
│   ├── cart.html           # Shopping cart
│   ├── checkout.html       # Checkout page
│   ├── login.html          # User login
│   ├── signup.html         # User registration
│   ├── profile.html        # User profile
│   ├── admin/
│   │   ├── admin-login.html     # Admin login
│   │   └── admin-dashboard.html # Admin panel
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── app.js          # Main JavaScript
└── src/
    └── phone images/       # Product images
```

## API Endpoints

### Authentication
- POST `/api/auth/signup` - User registration
- POST `/api/auth/login` - User login
- GET `/api/auth/me` - Get current user

### Products
- GET `/api/products` - List products
- GET `/api/products/:id` - Get product details
- GET `/api/products/featured` - Get featured products

### Cart
- GET `/api/cart` - Get user cart
- POST `/api/cart` - Add to cart
- PUT `/api/cart/:id` - Update cart item
- DELETE `/api/cart/:id` - Remove from cart

### Orders
- POST `/api/orders` - Create order
- GET `/api/orders` - Get user orders
- GET `/api/orders/:id` - Get order details

### Admin
- POST `/api/admin/login` - Admin login
- POST `/api/admin/products` - Add product
- DELETE `/api/admin/products/:id` - Delete product
- GET `/api/admin/orders` - Get all orders
- PUT `/api/admin/orders/:id` - Update order status

## Troubleshooting

### Database Connection Issues
- Ensure MySQL server is running
- Check database credentials in `database.py`
- Verify database exists: `SHOW DATABASES;`

### CORS Errors
- Make sure backend server is running
- Check that API_BASE_URL in frontend matches backend URL

### Product Images Not Showing
- Image paths are relative to `src/phone images/`
- Ensure images exist in the correct directory

## Notes
- Password hashing uses bcrypt
- JWT tokens expire after 7 days
- All product images are stored in `src/phone images/`
- Tax is calculated at 18%
- Default payment method is Cash on Delivery

Enjoy your M&C E-Commerce platform! 🚀
