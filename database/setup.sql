-- Create database
CREATE DATABASE IF NOT EXISTS ecommerce_ai;
USE ecommerce_ai;

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    sale_price DECIMAL(10,2),
    stock_quantity INT NOT NULL DEFAULT 0,
    category_id INT,
    image_url VARCHAR(255),
    rating DECIMAL(3,2) DEFAULT 0,
    review_count INT DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Create product_images table
CREATE TABLE IF NOT EXISTS product_images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Create product_attributes table
CREATE TABLE IF NOT EXISTS product_attributes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    attribute_name VARCHAR(50) NOT NULL,
    attribute_value VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Insert sample categories
INSERT INTO categories (name, slug, description) VALUES
('Electronics', 'electronics', 'Electronic devices and accessories'),
('Fashion', 'fashion', 'Clothing, shoes, and accessories'),
('Home & Living', 'home-living', 'Furniture and home decor'),
('Beauty', 'beauty', 'Beauty and personal care products'),
('Sports', 'sports', 'Sports equipment and accessories');

-- Insert subcategories
INSERT INTO categories (name, slug, description, parent_id) VALUES
('Smartphones', 'smartphones', 'Mobile phones and accessories', 1),
('Laptops', 'laptops', 'Notebooks and accessories', 1),
('Men\'s Clothing', 'mens-clothing', 'Clothing for men', 2),
('Women\'s Clothing', 'womens-clothing', 'Clothing for women', 2),
('Furniture', 'furniture', 'Home and office furniture', 3),
('Decor', 'decor', 'Home decoration items', 3);

-- Insert sample products
INSERT INTO products (name, slug, description, price, sale_price, stock_quantity, category_id, image_url, rating, review_count, is_featured) VALUES
('iPhone 13 Pro', 'iphone-13-pro', 'Latest Apple iPhone with pro camera system', 999.99, 899.99, 50, 6, 'https://images.unsplash.com/photo-1632661674596-79b3d5d1b5c0', 4.8, 120, TRUE),
('MacBook Pro M1', 'macbook-pro-m1', 'Powerful laptop with M1 chip', 1299.99, NULL, 30, 7, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8', 4.9, 85, TRUE),
('Nike Air Max', 'nike-air-max', 'Classic running shoes', 129.99, 99.99, 100, 8, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff', 4.5, 200, FALSE),
('Leather Jacket', 'leather-jacket', 'Premium leather jacket', 299.99, 249.99, 25, 9, 'https://images.unsplash.com/photo-1551028719-00167b16eac5', 4.7, 45, TRUE),
('Modern Sofa', 'modern-sofa', 'Comfortable 3-seater sofa', 799.99, 699.99, 15, 10, 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc', 4.6, 60, FALSE),
('Wall Art Set', 'wall-art-set', 'Set of 3 modern wall paintings', 199.99, 149.99, 40, 11, 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5', 4.4, 30, FALSE);

-- Insert product images
INSERT INTO product_images (product_id, image_url, is_primary) VALUES
(1, 'https://images.unsplash.com/photo-1632661674596-79b3d5d1b5c0', TRUE),
(1, 'https://images.unsplash.com/photo-1632661674596-79b3d5d1b5c1', FALSE),
(2, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8', TRUE),
(2, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca9', FALSE),
(3, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff', TRUE),
(3, 'https://images.unsplash.com/photo-1542291026-7eec264c27fe', FALSE),
(4, 'https://images.unsplash.com/photo-1551028719-00167b16eac5', TRUE),
(4, 'https://images.unsplash.com/photo-1551028719-00167b16eac6', FALSE),
(5, 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc', TRUE),
(5, 'https://images.unsplash.com/photo-1555041469-a586c61ea9bd', FALSE),
(6, 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5', TRUE),
(6, 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a6', FALSE);

-- Insert product attributes
INSERT INTO product_attributes (product_id, attribute_name, attribute_value) VALUES
(1, 'Color', 'Graphite'),
(1, 'Storage', '256GB'),
(1, 'Screen Size', '6.1 inch'),
(2, 'Processor', 'M1 Pro'),
(2, 'RAM', '16GB'),
(2, 'Storage', '512GB SSD'),
(3, 'Size', 'US 10'),
(3, 'Color', 'Black/White'),
(4, 'Size', 'M'),
(4, 'Color', 'Black'),
(5, 'Material', 'Fabric'),
(5, 'Color', 'Gray'),
(6, 'Size', 'Set of 3'),
(6, 'Style', 'Modern Abstract');

-- Create indexes for better performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_featured ON products(is_featured);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_product_images_product ON product_images(product_id);
CREATE INDEX idx_product_attributes_product ON product_attributes(product_id); 