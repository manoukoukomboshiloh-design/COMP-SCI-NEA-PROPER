import sqlite3
import hashlib          
import socket             
import threading          #for multiple users at the same time
import logging            # debugging and audit trail

# Setup for login showing monitoring of the system - detailed runtime - for debugging and maintenance
logging.basicConfig(
    filename='server_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)
logging.debug('Server started and logging initialized.')

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

def handle_connection(client_socket):              #handles one user per session
    try:
        client_socket.send("Username: ".encode())           #Requests user name
        username = client_socket.recv(1024).decode().strip() #.strip() removing extra spaces 
        logging.debug(f'Received username: {username}')
        # Request password
        client_socket.send("Password: ".encode())
        password = client_socket.recv(1024).decode().strip()
        logging.debug('Received password from client.')            # Hash password for secure comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect("../database/userdata.db")              # Check against database
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM userdata WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        if cur.fetchone():           #login validation here
            client_socket.send("Login successful!".encode())
            logging.info(f'Login successful for user: {username}')
        else:
            client_socket.send("Login failed!".encode())
            logging.warning(f'Login failed for user: {username}')
            
        conn.close()

    except Exception as e:
        logging.error(f'Error in handle_connection: {e}')
    finally:
        client_socket.close()

# Accept multiple clients
while True:
    client, addr = server.accept()
    logging.info(f'Accepted connection from {addr}')
    threading.Thread(target=handle_connection, args=(client,)).start()
