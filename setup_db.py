import sqlite3
import datetime

# Create a connection to the SQLite database
conn = sqlite3.connect('users.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store user data
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    subscription_status TEXT NOT NULL,
    last_login_date TEXT NOT NULL,
    purchase_count INTEGER NOT NULL
)
''')

# Sample data to populate the database
users = [
    ('user1@example.com', 'premium', '2024-09-01', 3),
    ('user2@example.com', 'regular', '2024-08-15', 1),
    ('user3@example.com', 'premium', '2024-08-25', 5),
    ('user4@example.com', 'regular', '2024-07-20', 0)
]

# Insert sample data into the database
cursor.executemany('INSERT INTO users (email, subscription_status, last_login_date, purchase_count) VALUES (?, ?, ?, ?)', users)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete with sample users.")