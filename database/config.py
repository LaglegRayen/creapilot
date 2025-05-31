DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': 'LAGLEG123',  # Change this to your MySQL password
    'database': 'ecommerce_ai',
    'charset': 'utf8mb4',
    'cursorclass': 'DictCursor'
}

def get_db_config():
    return DB_CONFIG 