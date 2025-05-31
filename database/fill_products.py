import pymysql
from pymysql import Error
from faker import Faker
import random
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image
import os

fake = Faker()

# Product categories and their corresponding image search terms
CATEGORY_IMAGES = {
    'Smartphones': ['smartphone', 'mobile phone', 'iphone', 'android phone', 'smart device'],
    'Laptops': ['laptop', 'notebook', 'macbook', 'ultrabook', 'gaming laptop'],
    'Tablets': ['tablet', 'ipad', 'android tablet', 'digital tablet', 'touchscreen'],
    'Headphones': ['headphones', 'earphones', 'wireless headphones', 'bluetooth headphones', 'gaming headset'],
    'Cameras': ['camera', 'digital camera', 'dslr', 'mirrorless camera', 'action camera'],
    'Clothing': ['clothing', 'fashion', 'apparel', 'outfit', 'dress'],
    'Shoes': ['shoes', 'footwear', 'sneakers', 'boots', 'sandals'],
    'Accessories': ['accessories', 'jewelry', 'watch', 'bag', 'wallet'],
    'Furniture': ['furniture', 'chair', 'table', 'sofa', 'bed'],
    'Decor': ['home decor', 'decoration', 'art', 'vase', 'cushion'],
    'Kitchen': ['kitchen', 'cookware', 'appliances', 'utensils', 'gadgets'],
    'Bedding': ['bedding', 'pillow', 'blanket', 'duvet', 'mattress'],
    'Lighting': ['lighting', 'lamp', 'chandelier', 'light fixture', 'sconce'],
    'Cosmetics': ['cosmetics', 'makeup', 'beauty products', 'skincare', 'perfume'],
    'Skincare': ['skincare', 'face cream', 'serum', 'moisturizer', 'cleanser'],
    'Makeup': ['makeup', 'cosmetics', 'lipstick', 'foundation', 'eyeshadow'],
    'Perfume': ['perfume', 'fragrance', 'cologne', 'scent', 'eau de toilette'],
    'Haircare': ['haircare', 'shampoo', 'conditioner', 'hair products', 'styling'],
    'Sports Equipment': ['sports equipment', 'fitness gear', 'exercise equipment', 'gym equipment', 'training gear'],
    'Fitness': ['fitness', 'workout', 'exercise', 'training', 'gym'],
    'Yoga': ['yoga', 'yoga mat', 'yoga equipment', 'meditation', 'wellness'],
    'Running': ['running', 'running shoes', 'jogging', 'athletic wear', 'sports'],
    'Gym': ['gym', 'fitness', 'workout', 'exercise', 'training']
}

def get_random_image_url(category):
    """Get a random image URL from Unsplash based on category"""
    # Try to get category-specific search terms
    search_terms = CATEGORY_IMAGES.get(category, [category.lower()])
    search_term = random.choice(search_terms)
    return f"https://source.unsplash.com/400x400/?{search_term}"

def generate_product_data(category_id, category_name):
    """Generate realistic product data"""
    name = fake.catch_phrase()
    slug = name.lower().replace(' ', '-').replace('.', '')
    price = round(random.uniform(10.99, 999.99), 2)
    sale_price = round(price * random.uniform(0.7, 0.9), 2) if random.random() > 0.5 else None
    stock = random.randint(0, 100)
    rating = round(random.uniform(3.5, 5.0), 1)
    review_count = random.randint(10, 500)
    is_featured = random.random() > 0.7
    
    return {
        'name': name,
        'slug': slug,
        'description': fake.text(max_nb_chars=200),
        'price': price,
        'sale_price': sale_price,
        'stock_quantity': stock,
        'category_id': category_id,
        'image_url': get_random_image_url(category_name),
        'rating': rating,
        'review_count': review_count,
        'is_featured': is_featured
    }

def generate_product_attributes(product_id):
    """Generate random product attributes"""
    attributes = []
    
    # Common attributes for all products
    attributes.append({
        'product_id': product_id,
        'attribute_name': 'Brand',
        'attribute_value': fake.company()
    })
    
    # Random additional attributes
    possible_attributes = [
        ('Color', ['Black', 'White', 'Silver', 'Gold', 'Blue', 'Red']),
        ('Size', ['S', 'M', 'L', 'XL', 'XXL']),
        ('Material', ['Cotton', 'Polyester', 'Leather', 'Metal', 'Plastic']),
        ('Weight', ['Light', 'Medium', 'Heavy']),
        ('Style', ['Modern', 'Classic', 'Vintage', 'Contemporary'])
    ]
    
    # Add 2-4 random attributes
    for _ in range(random.randint(2, 4)):
        attr_name, possible_values = random.choice(possible_attributes)
        attributes.append({
            'product_id': product_id,
            'attribute_name': attr_name,
            'attribute_value': random.choice(possible_values)
        })
    
    return attributes

def fill_database():
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='LAGLEG123',
            database='ecommerce_ai',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Get all categories
            cursor.execute("SELECT id, name FROM categories WHERE parent_id IS NOT NULL")
            categories = cursor.fetchall()
            
            # Generate 10 products for each category
            for category in categories:
                print(f"Generating products for {category['name']}...")
                
                for _ in range(10):
                    # Generate product data
                    product_data = generate_product_data(category['id'], category['name'])
                    
                    # Insert product
                    cursor.execute("""
                        INSERT INTO products 
                        (name, slug, description, price, sale_price, stock_quantity, 
                         category_id, image_url, rating, review_count, is_featured)
                        VALUES 
                        (%(name)s, %(slug)s, %(description)s, %(price)s, %(sale_price)s, 
                         %(stock_quantity)s, %(category_id)s, %(image_url)s, %(rating)s, 
                         %(review_count)s, %(is_featured)s)
                    """, product_data)
                    
                    product_id = cursor.lastrowid
                    
                    # Generate and insert product attributes
                    attributes = generate_product_attributes(product_id)
                    for attr in attributes:
                        cursor.execute("""
                            INSERT INTO product_attributes 
                            (product_id, attribute_name, attribute_value)
                            VALUES (%(product_id)s, %(attribute_name)s, %(attribute_value)s)
                        """, attr)
                    
                    # Add 2-4 product images
                    num_images = random.randint(2, 4)
                    for i in range(num_images):
                        cursor.execute("""
                            INSERT INTO product_images 
                            (product_id, image_url, is_primary)
                            VALUES (%s, %s, %s)
                        """, (product_id, get_random_image_url(category['name']), i == 0))
                
                connection.commit()
                print(f"Completed {category['name']}")
            
            print("Database filled successfully!")
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    fill_database() 