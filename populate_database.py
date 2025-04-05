import os
import sqlite3
import pandas as pd

# Define file paths
data_folder = "synthetic_datasets"
database_folder = "database_scripts"
database_file = os.path.join(database_folder, "zomata_database.db")

# Verify the database exists
if not os.path.exists(database_file):
    raise FileNotFoundError(f"Database file '{database_file}' not found. Please run the create_database.py script first.")

# Connect to the database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Load synthetic datasets
customers_file = os.path.join(data_folder, "customers.csv")
restaurants_file = os.path.join(data_folder, "restaurants.csv")
orders_file = os.path.join(data_folder, "orders.csv")
deliveries_file = os.path.join(data_folder, "deliveries.csv")

# Check if files exist
for file in [customers_file, restaurants_file, orders_file, deliveries_file]:
    if not os.path.exists(file):
        raise FileNotFoundError(f"Data file '{file}' not found. Please ensure datasets are generated in the synthetic_datasets folder.")

# Load data into DataFrames
customers_df = pd.read_csv(customers_file)
restaurants_df = pd.read_csv(restaurants_file)
orders_df = pd.read_csv(orders_file)
deliveries_df = pd.read_csv(deliveries_file)

# Insert data into tables
def insert_data(table_name, dataframe):
    """
    Inserts data from a DataFrame into the specified table.
    """
    columns = ", ".join(dataframe.columns)
    placeholders = ", ".join(["?"] * len(dataframe.columns))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
    
    for row in dataframe.itertuples(index=False):
        cursor.execute(query, tuple(row))

# Populate tables
try:
    # Insert into Customers table
    insert_data("Customers", customers_df)

    # Insert into Restaurants table
    insert_data("Restaurants", restaurants_df)

    # Insert into Orders table
    insert_data("Orders", orders_df)

    # Insert into Deliveries table
    insert_data("Deliveries", deliveries_df)

    # Commit the changes
    conn.commit()
    print("Data successfully inserted into the database.")

except sqlite3.IntegrityError as e:
    conn.rollback()
    print(f"Data insertion failed due to integrity error: {e}")

# Data Validation
def validate_data():
    """
    Performs basic validation to ensure data consistency.
    """
    issues = []
    
    # Check for missing data
    for table in ["Customers", "Restaurants", "Orders", "Deliveries"]:
        query = f"SELECT COUNT(*) AS missing_count FROM {table} WHERE ROWID IS NULL;"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        if result > 0:
            issues.append(f"Table '{table}' contains {result} rows with missing data.")
    
    # Check for foreign key inconsistencies
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Orders 
        WHERE customer_id NOT IN (SELECT customer_id FROM Customers)
        OR restaurant_id NOT IN (SELECT restaurant_id FROM Restaurants);
    """)
    invalid_orders = cursor.fetchone()[0]
    if invalid_orders > 0:
        issues.append(f"Orders table contains {invalid_orders} rows with invalid foreign key references.")
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Deliveries 
        WHERE order_id NOT IN (SELECT order_id FROM Orders);
    """)
    invalid_deliveries = cursor.fetchone()[0]
    if invalid_deliveries > 0:
        issues.append(f"Deliveries table contains {invalid_deliveries} rows with invalid foreign key references.")

    if not issues:
        print("Data validation passed: No issues found.")
    else:
        print("Data validation failed with the following issues:")
        for issue in issues:
            print(f" - {issue}")

# Perform validation
validate_data()

# Close the database connection
conn.close()
