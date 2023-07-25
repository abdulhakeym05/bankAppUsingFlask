import sqlite3

# Import and setup
connection = sqlite3.connect("bankdata.db")
cursor = connection.cursor()

# -------------------------
# My queries
'''

commands = [
    """CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone_number TEXT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        account_type VARCHAR(50),
        balance DECIMAL(10, 2),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );"""
]

for command in commands:
    cursor.execute(command)

connection.commit()

# Add customer and account data
customers = [
    ('John', '123 Main St', '555-1234', 'password123', 'john@example.com'),
    ('Abdulhakim', '456 Elm St', '555-5678', 'password456', 'jane@example.com'),
    ('Naveen', '789 Oak St', '555-9012', 'password789', 'mike@example.com')
]

accounts = [
    (101, 1, 'Savings', 1000.00),
    (102, 2, 'Checking', 500.00),
    (103, 3, 'Savings', 2000.00
]

# Add customers to the database
cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)", customers)

# Add accounts to the database
cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?)", accounts)

# Commit the changes and close the connection
connection.commit()
connection.close()



command = """
CREATE TABLE IF NOT EXISTS data (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price INT,
    Quantity INT
);
"""
cursor.execute(command)

'''

