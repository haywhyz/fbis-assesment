from flask import Flask, request
import psycopg2
from psycopg2 import Error
import os

app = Flask(__name__)

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'db'),
            database=os.getenv('POSTGRES_DB', 'reverse_ip_db'),
            user=os.getenv('POSTGRES_USER', 'user'),
            password=os.getenv('POSTGRES_PASSWORD', 'password')
        )
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def reverse_ip(ip):
    return '.'.join(ip.split('.')[::-1])

@app.route('/')
def get_reverse_ip():
    client_ip = request.remote_addr
    reversed_ip = reverse_ip(client_ip)
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create table if not exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS ips
                              (id SERIAL PRIMARY KEY,
                               original VARCHAR(15),
                               reversed VARCHAR(15))''')
            
            # Insert IP addresses
            cursor.execute("INSERT INTO ips (original, reversed) VALUES (%s, %s)",
                           (client_ip, reversed_ip))
            connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    return f"Your IP in reverse: {reversed_ip}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)