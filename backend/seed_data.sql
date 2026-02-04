-- Seed Data for E-Commerce Database
USE ecommerce_db;

-- Insert Categories
INSERT INTO categories (name, slug) VALUES
('Smartphones', 'smartphones'),
('Laptops', 'laptops'),
('Accessories', 'accessories');

-- Insert Default Admin (password: admin123)
INSERT INTO admin_users (username, password_hash, email) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEiXzu', 'admin@ecommerce.com');

-- Insert Products from images
INSERT INTO products (name, brand, category_id, price, discount_price, description, specifications, image_url, stock_quantity, is_featured) VALUES
('Galaxy S25', 'Samsung', 1, 89999.00, 84999.00, 'Premium flagship smartphone with Ultra 200MP Camera and cutting-edge features', 
JSON_OBJECT(
    'camera', 'Ultra 200MP Camera with 1x, Tele, Ultra Wide, Creator & 10MP Telephoto',
    'refresh_rate', '120Hz Refresh Rate',
    'processor', 'Snapdragon 8 Gen 4',
    'storage', '256GB or 512GB Storage',
    'front_camera', '32MP Front Camera',
    'battery', '4700mAh Fast Charging',
    'water_resistance', 'IP68 Water & Dust Resistant'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.18.22 PM.jpeg', 50, TRUE),

('Honor i7 17 Pro', 'Honor', 1, 74999.00, 69999.00, 'High-performance smartphone with Ultra 200MP Camera and MagicOS 8.0', 
JSON_OBJECT(
    'camera', 'Ultra 200MP Camera - 200MP Main, Wide & Ultra Wide Close-Up Camera',
    'ram', '12GB LPDDR5X RAM',
    'battery', 'Battery 5000mAh Fast Charging',
    'os', 'MagicOS 8.0 Powered by Android',
    'front_camera', '32MP Front Camera',
    'display', 'i7 FHD+ OLED 120Hz',
    'water_resistance', 'IP68 Water & Dust Resistant'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.18.58 PM.jpeg', 45, TRUE),

('Pixel 10 Pro (Pine)', 'Google', 1, 94999.00, 89999.00, 'Google flagship with advanced AI features and Tensor Pro X Chip', 
JSON_OBJECT(
    'camera', 'Cutting-Edge Camera System - Tensor Pro X Chip for Advanced AI Photography, Triple Lens Camera (48P 5x Telephoto), Optical Image Stabilization on All Lenses, Enhanced Night Sight & Astrophotography 2.0',
    'performance', 'Tensor Pro X Processor with Integrated AI, 16GB RAM for Seamless Multitasking, 22GB/512X Storage Options, Real-time (Live Translate, Call Screen Pro)',
    'display', '6.7inch QHD+ LTPO OLED Display, 120Hz Adaptive Refresh Rate, Ultra-thin Bezels & Durable Gorilla Glass, IP68 Water & Dust Resistance',
    'battery', '5,500mAh All-Day Battery, 65W Fast Wired Charging, 30W Fast Wireless Charging, WiFi 7 & 5G Connectivity'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.19.26 PM.jpeg', 30, TRUE),

('Pixel 10 Pro (Black)', 'Google', 1, 94999.00, NULL, 'Google flagship with advanced AI features and Tensor Pro X Chip in elegant black', 
JSON_OBJECT(
    'camera', 'Cutting-Edge Camera System - Tensor Pro X Chip for Advanced AI Photography, Triple Lens Camera (48P 5x Telephoto), Optical Image Stabilization on All Lenses, Enhanced Night Sight & Astrophotography 2.0',
    'performance', 'Tensor Pro X Processor with Integrated AI, 16GB RAM for Seamless Multitasking, 22GB/512X Storage Options, Real-time (Live Translate, Call Screen Pro)',
    'display', '6.7inch QHD+ LTPO OLED Display, 120Hz Adaptive Refresh Rate, Ultra-thin Bezels & Durable Gorilla Glass, IP68 Water & Dust Resistance',
    'battery', '5,500mAh All-Day Battery, 65W Fast Wired Charging, 30W Fast Wireless Charging, WiFi 7 & 5G Connectivity'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.19.44 PM.jpeg', 35, FALSE),

('OnePlus 13R (5x Telephoto)', 'OnePlus', 1, 64999.00, 59999.00, 'High-performance smartphone with exceptional camera and blazing fast charging', 
JSON_OBJECT(
    'camera', 'Cutting-Edge Camera System - 50MP Main Sensor, 16MP Ultra-Wide Lens, 5x Optical Telephoto Lens (64MP), Advanced ProX Imaging Engine, Ultra-Nightscape Mode 3.0',
    'performance', 'Snapdragon 8 Gen 4 Processor, 16GB LPDDR6X RAM, 512B UFS 4.1 Storage, 120W SuperVOOC Charging, OxygenOS 15 (Android 15), WiFi 7 & 5G Connectivity'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.20.21 PM.jpeg', 40, TRUE),

('Vivo X200 Pro', 'Vivo', 1, 79999.00, 74999.00, 'Premium camera phone with cutting-edge imaging technology and ultimate performance', 
JSON_OBJECT(
    'camera', 'Cutting-Edge Camera System - 50MP Primary Sensor, 12MP Periscope Telephoto (xx), Micro Gimbal Stabilization, Zeiss Optics & Imaging Suite',
    'performance', 'Dimensity 9300+ Chipset, 16GB LPDDR5T RAM 1TB UFS 4.0 Storage, 6.8-inch QHD+ 144Hz OLED Display, 120W Fast Charging'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.21.03 PM.jpeg', 35, TRUE),

('iQOO Neo 10R (184Hz QItodiaz)', 'iQOO', 1, 54999.00, 49999.00, 'Gaming-focused smartphone with ultra-high refresh rate display', 
JSON_OBJECT(
    'display', '184Hz QItodiaz Display',
    'category', 'Gaming Smartphone',
    'features', 'High-performance gaming with ultra-smooth display'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.24.28 PM.jpeg', 50, FALSE),

('Pixel X Ultra', 'Google', 1, 109999.00, 104999.00, 'Ultra-premium flagship with AI-powered camera and ultimate performance', 
JSON_OBJECT(
    'camera', 'AI-Powered Camera System - 1-inch 50MP Main Sensor, 3x Optical Folded Telephoto, Advanced Generative AI Features, Pixel Vision Processor',
    'performance', 'Tensor G6 Pro Chip, 18GB LPDDR6 RAM, 144Hz Quantum-Dot OLED Display, 120W HyperCharge'
), 'src/phone images/WhatsApp Image 2026-01-24 at 11.31.16 PM.jpeg', 20, TRUE);

-- Insert some sample users (password: password123)
INSERT INTO users (email, password_hash, full_name, phone, address) VALUES
('john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEiXzu', 'John Doe', '+91 9876543210', '123 Main St, Mumbai, Maharashtra 400001'),
('jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEiXzu', 'Jane Smith', '+91 9876543211', '456 Park Ave, Delhi, Delhi 110001');
