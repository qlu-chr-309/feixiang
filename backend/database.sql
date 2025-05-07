-- Drop database if exists and create a new one
DROP DATABASE IF EXISTS drone_shop;
CREATE DATABASE drone_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE drone_shop;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    role ENUM('customer', 'admin') DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create product categories table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    category_id INT,
    image VARCHAR(255),
    specs JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Create orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('pending', 'paid', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address TEXT NOT NULL,
    payment_method VARCHAR(50),
    tracking_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create order items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create addresses table
CREATE TABLE addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipient_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    detailed_address TEXT NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create product reviews table
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    order_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Insert sample data for categories
INSERT INTO categories (name, description, image) VALUES
('消费级无人机', '适合个人娱乐和简单航拍的无人机', '/static/categories/consumer.jpg'),
('专业级无人机', '适合专业航拍和工作使用的高性能无人机', '/static/categories/professional.jpg'),
('农业植保无人机', '专为农业植保作业设计的高效无人机', '/static/categories/agriculture.jpg'),
('配件与附件', '各类无人机配件、电池和附件', '/static/categories/accessories.jpg'),
('培训服务', '无人机操作培训和认证课程', '/static/categories/training.jpg');

-- Insert sample products
INSERT INTO products (name, description, price, stock, category_id, image, specs) VALUES
('大疆 Mini 3 Pro', '轻量级便携无人机，适合初学者和休闲拍摄', 4788.00, 100, 1, '/static/products/mini3pro.jpg', 
'{"weight": "249g", "max_flight_time": "34分钟", "camera": "4K/60fps", "max_transmission": "12km", "sensors": "三向避障"}'),

('大疆 Air 2S', '强大的便携航拍无人机，1英寸CMOS传感器', 7499.00, 80, 1, '/static/products/air2s.jpg', 
'{"weight": "595g", "max_flight_time": "31分钟", "camera": "5.4K/30fps", "max_transmission": "12km", "sensors": "四向避障"}'),

('大疆 Mavic 3', '旗舰级航拍无人机，哈苏相机', 13999.00, 50, 2, '/static/products/mavic3.jpg', 
'{"weight": "895g", "max_flight_time": "46分钟", "camera": "5.1K/50fps", "max_transmission": "15km", "sensors": "全向避障"}'),

('大疆 经纬 M30', '工业级无人机，适合专业巡检和测绘', 45999.00, 20, 2, '/static/products/m30.jpg', 
'{"weight": "3.77kg", "max_flight_time": "41分钟", "camera": "4K/30fps + 热成像", "max_transmission": "15km", "sensors": "全向避障"}'),

('大疆 T30 植保无人机', '高效农业植保无人机，30L喷洒容量', 29999.00, 15, 3, '/static/products/t30.jpg', 
'{"weight": "24.8kg(空载)", "max_flight_time": "10分钟(满载)", "tank_capacity": "30L", "spray_width": "9m", "coverage": "16公顷/小时"}'),

('大疆 Mavic 3 智能飞行电池', '高容量智能飞行电池，适用于Mavic 3系列', 949.00, 200, 4, '/static/products/mavic3_battery.jpg', 
'{"capacity": "5000mAh", "voltage": "15.4V", "battery_type": "LiPo 4S", "charging_time": "96分钟", "weight": "335.5g"}'),

('大疆无人机飞行技术培训课程', '专业无人机操作技能培训，包含理论和实践', 3999.00, 30, 5, '/static/products/training.jpg', 
'{"duration": "5天", "certificate": "AOPA无人机驾驶员证", "includes": "理论培训,实操训练,模拟考试", "location": "线下培训中心"}');

-- Insert a test admin user (password is 'admin123')
INSERT INTO users (username, password, email, role) VALUES
('admin', '$2b$10$rPvX0Bt9k2WcJt/KFdEKDuUiNBT4Bhwr9Mv82W/K9/7cJxhWgO1tq', 'admin@droneservice.com', 'admin');

-- Insert test customers (password is 'password123')
INSERT INTO users (username, password, email, phone, role) VALUES
('user1', '$2b$10$j8nnwV5rUQvCOiGptyYEZu.y0A8.wgGdgisn.bPbfypNcIQIrXDtW', 'user1@example.com', '13800138001', 'customer'),
('user2', '$2b$10$j8nnwV5rUQvCOiGptyYEZu.y0A8.wgGdgisn.bPbfypNcIQIrXDtW', 'user2@example.com', '13800138002', 'customer'); 