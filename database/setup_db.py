import pymysql
from pymysql import Error
import os

def setup_database():
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='LAGLEG123',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Read and execute the SQL file
            sql_file_path = os.path.join(os.path.dirname(__file__), 'setup.sql')
            with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
                sql_commands = sql_file.read()
                
                # Split the file into individual commands
                commands = sql_commands.split(';')
                
                # Execute each command
                for command in commands:
                    if command.strip():
                        try:
                            cursor.execute(command)
                            connection.commit()
                        except Error as e:
                            print(f"Error executing command: {command[:100]}...")
                            print(f"Error details: {e}")
                            continue
            
            print("Database setup completed successfully!")
            
    except Error as e:
        print(f"Connection Error: {e}")
        
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    setup_database() 