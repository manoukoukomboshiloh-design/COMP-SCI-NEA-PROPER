import sqlite3
import hashlib           #I hash the password for protection during transmission between the client and server

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
id INTEGER PRIMARY KEY,
username VARCHAR(255) NOT NULL, UNIQUE
password VARCHAR(255) NOT NULL
)
""")
#making a sql table for the user credentials so I know whos who
# random guys in here
users = [
    ("SHILOHHH123", "SHILOOHHSSpassword"),
    ("buggs", "bunny123"),
    ("bob", "bobpass")
]
for username, password in users:
    hashed_password = hashlib.sha256(password.encode()).hexdigest() #hashing algorithm used to make my hashed password
    cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
    # putting the hashed password into the table instead of the actual password, obvioulsy with the username
conn.commit()  # gotta save my changes
conn.close()

