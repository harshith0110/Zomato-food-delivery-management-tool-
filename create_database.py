import sqlite3
import os

# Define the output folder and database file
output_folder = "database_scripts"
os.makedirs(output_folder, exist_ok=True)
database_file = os.path.join(output_folder, "zomata_database.db")

# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Define table schemas
schemas = {
    "Customers": """
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            signup_date DATE NOT NULL,
            is_premium BOOLEAN NOT NULL,
            preferred_cuisine TEXT,
            total_orders INTEGER DEFAULT 0,
            average_rating REAL DEFAULT 0.0
        );
    """,
    "Restaurants": """
        CREATE TABLE IF NOT EXISTS Restaurants (
            restaurant_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            cuisine_type TEXT NOT NULL,
            location TEXT NOT NULL,
            owner_name TEXT NOT NULL,
            average_delivery_time INTEGER DEFAULT 0,
            contact_number TEXT NOT NULL,
            rating REAL DEFAULT 0.0,
            total_orders INTEGER DEFAULT 0,
            is_active BOOLEAN NOT NULL
        );
    """,
    "Orders": """
        CREATE TABLE IF NOT EXISTS Orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            restaurant_id TEXT NOT NULL,
            order_date DATETIME NOT NULL,
            delivery_time DATETIME,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_mode TEXT NOT NULL,
            discount_applied REAL DEFAULT 0.0,
            feedback_rating REAL DEFAULT 0.0,
            FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants (restaurant_id)
        );
    """,
    "Deliveries": """
        CREATE TABLE IF NOT EXISTS Deliveries (
            delivery_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            delivery_status TEXT NOT NULL,
            distance REAL NOT NULL,
            delivery_time INTEGER NOT NULL,
            estimated_time INTEGER NOT NULL,
            delivery_fee REAL NOT NULL,
            vehicle_type TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders (order_id)
        );
    """
    
}

# Create tables in the database
for table_name, schema in schemas.items():
    cursor.execute(schema)
    print(f"Table '{table_name}' created successfully.")
    
    # Add new columns if not already present
    if table_name == "Customers":
        # Check if column exists before adding it
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "new_column_name" not in columns:
            try:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN new_column_name TEXT;")
                print(f"New column added to '{table_name}'")
            except sqlite3.OperationalError:
                # If there was any issue (e.g., column already exists), catch and print error
                print(f"Failed to add column to '{table_name}'.")
    
    # Prevent duplicate entries by using INSERT OR IGNORE when inserting data
    # Example: cursor.execute("INSERT OR IGNORE INTO Customers VALUES (...);")
    # This ensures that duplicate records will not be inserted.

# Commit and close the connection
conn.commit()
conn.close()

print(f"Database created and tables initialized in '{database_file}'")
