// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// ==================== API Helper Functions ====================

async function apiCall(endpoint, method = 'GET', data = null, requiresAuth = false) {
    const headers = {
        'Content-Type': 'application/json',
    };

    if (requiresAuth) {
        const token = localStorage.getItem('token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }

    const config = {
        method,
        headers,
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'An error occurred');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ==================== Auth Functions ====================

function isLoggedIn() {
    return !!localStorage.getItem('token');
}

function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// ==================== Cart Management ====================

class CartManager {
    constructor() {
        this.cart = this.loadCart();
    }

    loadCart() {
        const cartStr = localStorage.getItem('cart');
        return cartStr ? JSON.parse(cartStr) : [];
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
        this.updateCartBadge();
    }

    addItem(product, quantity = 1) {
        const existingItem = this.cart.find(item => item.id === product.id);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.cart.push({
                ...product,
                quantity
            });
        }
        
        this.saveCart();
        showNotification('Product added to cart!', 'success');
        
        // Sync with backend if logged in
        if (isLoggedIn()) {
            this.syncWithBackend();
        }
    }

    removeItem(productId) {
        this.cart = this.cart.filter(item => item.id !== productId);
        this.saveCart();
    }

    updateQuantity(productId, quantity) {
        const item = this.cart.find(item => item.id === productId);
        if (item) {
            item.quantity = quantity;
            this.saveCart();
        }
    }

    clearCart() {
        this.cart = [];
        this.saveCart();
    }

    getTotal() {
        return this.cart.reduce((total, item) => {
            const price = item.discount_price || item.price;
            return total + (price * item.quantity);
        }, 0);
    }

    getItemCount() {
        return this.cart.reduce((count, item) => count + item.quantity, 0);
    }

    updateCartBadge() {
        const badge = document.querySelector('.cart-badge .badge');
        if (badge) {
            const count = this.getItemCount();
            badge.textContent = count;
            badge.style.display = count > 0 ? 'flex' : 'none';
        }
    }

    async syncWithBackend() {
        if (!isLoggedIn()) return;

        try {
            for (const item of this.cart) {
                await apiCall('/cart', 'POST', {
                    product_id: item.id,
                    quantity: item.quantity
                }, true);
            }
        } catch (error) {
            console.error('Failed to sync cart:', error);
        }
    }
}

// Global cart instance
const cart = new CartManager();

// ==================== UI Helper Functions ====================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div style="padding: 1rem; background: ${type === 'success' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}; 
             border: 1px solid ${type === 'success' ? '#10b981' : '#ef4444'}; 
             color: ${type === 'success' ? '#10b981' : '#ef4444'}; 
             border-radius: 0.5rem; position: fixed; top: 20px; right: 20px; z-index: 10000;
             backdrop-filter: blur(10px); animation: slideIn 0.3s ease;">
            ${message}
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function showLoading(element) {
    element.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
        </div>
    `;
}

function formatPrice(price) {
    return `₹${parseFloat(price).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function calculateDiscount(originalPrice, discountPrice) {
    if (!discountPrice) return 0;
    return Math.round(((originalPrice - discountPrice) / originalPrice) * 100);
}

function createProductCard(product) {
    const discount = calculateDiscount(product.price, product.discount_price);
    
    return `
        <div class="product-card" onclick="window.location.href='product-detail.html?id=${product.id}'">
            <div class="product-image-container">
                <img src="${product.image_url}" alt="${product.name}" class="product-image">
                ${discount > 0 ? `<div class="discount-badge" style="position: absolute; top: 10px; right: 10px;">${discount}% OFF</div>` : ''}
            </div>
            <div class="product-info">
                <div class="product-brand">${product.brand}</div>
                <h3 class="product-name">${product.name}</h3>
                <div class="product-price">
                    <span class="price-current">${formatPrice(product.discount_price || product.price)}</span>
                    ${product.discount_price ? `<span class="price-original">${formatPrice(product.price)}</span>` : ''}
                </div>
                <button class="btn btn-primary" style="width: 100%; margin-top: 1rem;" 
                        onclick="event.stopPropagation(); cart.addItem(${JSON.stringify(product).replace(/"/g, '&quot;')})">
                    Add to Cart
                </button>
            </div>
        </div>
    `;
}

// ==================== Initialize ====================

document.addEventListener('DOMContentLoaded', () => {
    // Update cart badge
    cart.updateCartBadge();
    
    // Update navigation based on auth status
    updateNavigation();
});

function updateNavigation() {
    const authLinks = document.querySelector('.auth-links');
    if (!authLinks) return;
    
    if (isLoggedIn()) {
        const user = getUser();
        authLinks.innerHTML = `
            <a href="profile.html">👤 ${user.full_name}</a>
            <a href="#" onclick="logout(); return false;">Logout</a>
        `;
    } else {
        authLinks.innerHTML = `
            <a href="login.html">Login</a>
            <a href="signup.html">Sign Up</a>
        `;
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
