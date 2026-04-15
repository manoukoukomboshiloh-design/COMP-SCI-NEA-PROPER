import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()


def get_user(username):
    con = sqlite3.connect("../database/userdata.db")
    cur  = con.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    return result



def handle_connection(client_socket):
    client_socket.send("Username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    client_socket.send("Password: ".encode())
    password = client_socket.recv(1024).decode().strip()
    password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect("../database/userdata.db")
    cur = conn.cursor() 
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    if cur.fetchall():
        client_socket.send("Login successful!".encode())    
        # Display user dashboard with progress bars and stats
    else:
        client_socket.send("Login failed!".encode())

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()
import sqlite3
import hashlib
import socket
import threading
import logging

# Debugging/logging setup for NEA evidence
logging.basicConfig(
    filename='server_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)
logging.debug('Server started and logging initialized.')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

def get_user(username):
    con = sqlite3.connect("../database/userdata.db")
    cur  = con.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    return result

def handle_connection(client_socket):
    try:
        client_socket.send("Username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        logging.debug(f'Received username: {username}')
        client_socket.send("Password: ".encode())
        password = client_socket.recv(1024).decode().strip()
        logging.debug('Received password from client.')
        password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect("../database/userdata.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
        if cur.fetchall():
            client_socket.send("Login successful!".encode())
            logging.info(f'Login successful for user: {username}')
        else:
            client_socket.send("Login failed!".encode())
            logging.warning(f'Login failed for user: {username}')
    except Exception as e:
        logging.error(f'Error in handle_connection: {e}')
    finally:
        client_socket.close()

while True:
    client, addr = server.accept()
    logging.info(f'Accepted connection from {addr}')
    threading.Thread(target=handle_connection, args=(client,)).start()