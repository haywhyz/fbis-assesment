from flask import Flask, request
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
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
                              (id INT AUTO_INCREMENT PRIMARY KEY,
                               original VARCHAR(15),
                               reversed VARCHAR(15))''')
            
            # Insert IP addresses
            cursor.execute("INSERT INTO ips (original, reversed) VALUES (%s, %s)",
                           (client_ip, reversed_ip))
            connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return f"This is Your IP in reverse: {reversed_ip}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)