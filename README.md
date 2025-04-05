# Zomato Food Delivery Management Tool
This is a Streamlit-based web application designed to manage a Zomato-like food delivery database. It offers a range of functionalities to manage and visualize data, including dynamic CRUD operations, database schema management, and insightful data visualizations. The project is structured in a modular way to facilitate database interaction, insights extraction, and user-friendly management of food delivery operations.

Features
1. CRUD Operations
    Create: Add new records to tables such as customers, orders, and restaurants.
    Read: View existing records, including displaying all records in a table.
    Update: Modify existing records, allowing updates to customer, order, or restaurant details.
    Delete: Remove records from the database based on conditions such as the primary key.
2. Database Management
    Create new tables with customizable schemas.
    Modify the structure of existing tables by adding new columns.
    Delete tables or columns from the database.
    Ensure that all database operations are executed using safe SQL queries to prevent SQL injection.
3. Data Insights and Visualizations
    Generate insightful reports and visualizations for various business metrics, such as:
    Peak ordering times
    Top customers, restaurants, and feedback
    Most ordered items and popular cuisines
    Average delivery times and customer satisfaction
    Use dynamic filtering to allow users to customize reports by selecting specific insights to display.
4. Interactivity
    Real-time updates and visualizations using Streamlit interactive widgets.
    Dynamic fetching of tables and columns from the SQLite database to allow users to perform various actions on them.

📦 Project Structure

    ZOMATO_PROJECT/
    ├── database_scripts/
    │   ├── create_database.py         # Script for creating the SQLite database
    │   ├── populate_database.py       # Script for populating the database with initial data
    │   ├── zomata_database.db         # SQLite database file
    ├── env/                           # Virtual environment (optional, not usually included in repositories)
    ├── insights_visualization/
    │   ├── __init__.py                # Module initializer
    │   ├── data_insights.py           # Logic for generating insights and visualizations
    │   ├── queries.py                 # SQL queries for generating insights
    ├── oop_database/
    │   ├── __init__.py                # Module initializer
    │   ├── database_manager.py        # Manages all database-related operations (CRUD, schema management)
    ├── streamlit_app/
    │   ├── __init__.py                # Module initializer
    │   ├── zomato_app.py              # Streamlit app entry point
    ├── synthetic_datasets/
    │   ├── customers.csv              # Sample synthetic dataset for customers
    │   ├── deliveries.csv             # Sample synthetic dataset for deliveries
    │   ├── orders.csv                 # Sample synthetic dataset for orders
    │   ├── restaurants.csv            # Sample synthetic dataset for restaurants
    ├── generate_datasets.py           # Script to generate synthetic datasets for testing

Key Folders and Files

database_scripts/:
    create_database.py: Creates an SQLite database (zomata_database.db) and defines initial table schemas.
    populate_database.py: Populates the database with synthetic data to simulate a real-world food delivery environment.
    zomata_database.db: SQLite database file containing all the data, used by the Streamlit app.

insights_visualization/:
    data_insights.py: Contains methods for generating data insights and visualizations, such as orders by day, top customers, or peak ordering times.
    queries.py: Defines reusable SQL queries that fetch data for insights.

oop_database/:
    database_manager.py: Contains functions for interacting with the database, such as fetching data, executing SQL queries, and managing the database schema.

streamlit_app/:
    zomato_app.py: The main file that launches the Streamlit app and provides the user interface for managing the database and viewing insights.

synthetic_datasets/:
    Contains CSV files with synthetic data that mimics real-world customer, order, deliveries and restaurant data.

generate_datasets.py: 
    A script that generates synthetic datasets and saves them as CSV files. This allows you to create realistic, simulated data for testing or populating your database.

🔧 Setup Instructions
Prerequisites
Before setting up the project, ensure that you have:
    Python 3.x (preferably Python 3.8 or newer)
    Streamlit installed for running the web app
    SQLite (SQLite3 is integrated into Python, so it does not require separate installation)
    Installation Steps
    Clone the repository:

First, clone the repository to your local machine:

    git clone https://github.com/yourusername/zomato_project.git
    cd zomato_project
    
Create a Virtual Environment (Optional):

It is recommended to use a virtual environment to manage dependencies. Create one with the following command:

    python -m venv env
    
Activate the Virtual Environment:

On Windows:

    .\env\Scripts\activate

On macOS/Linux:

    source env/bin/activate


Run the App:
    To launch the Streamlit app, use the following command:

    streamlit run streamlit_app/zomato_app.py

This will start the web app on your local machine, which can be accessed at http://localhost:8501.

🛠️ Database Setup
    Creating and Populating the Database
    The SQLite database is created automatically by the script create_database.py. Here's how to initialize it:
    Run the script create_database.py to create the initial database structure (tables and schema).
    Run the script populate_database.py to populate the database with synthetic data. This will allow you to start interacting with the app right away.
    Both scripts interact with an SQLite database (zomata_database.db) located inside the database_scripts/ directory.

✨ Features and Usage
1. Managing Tables:
    In the Streamlit app, users can manage various database tables using the following functionalities:

    View Tables: The app dynamically fetches available tables in the database.
    Add Records: Add new records to existing tables via an interactive form.
    Update Records: Update records by selecting a specific record and modifying its values.
    Delete Records: Remove records from any table.
    The app supports all these CRUD operations in a user-friendly manner.

2. Data Insights & Visualizations:
    The insights section allows users to visualize trends and key business metrics:

    Peak Ordering Times: Shows the busiest times of day for orders.
    Top Customers: Lists the most frequent or highest spending customers.
    Most Ordered Items: Displays the most popular food items across the entire database.
    Order Value by Restaurant: Shows the total value of orders for each restaurant.
    Feedback Analysis: Visualizes customer feedback distribution and highlights top-rated restaurants and customers.
    
3. Interactive Insights:
    Users can select multiple insights to visualize and interact with:

    Choose from predefined insights such as "Top Customers" or "Most Ordered Items".
    Real-time visualizations using Plotly or Matplotlib.


🚀 Future Improvements
1. User Authentication:
    Implement a user login and role-based access control (e.g., Admin, User).
2. Advanced Data Validation:
    Add more robust validation for form inputs, especially for fields like email addresses, phone numbers, and dates.
3. Error Handling:
    Improve error handling to provide more meaningful error messages to users when something goes wrong.
4. Data Export:
    Add the ability to export tables or reports as CSV or PDF files.

generate_datasets.py Script
    The generate_datasets.py script is used to generate synthetic data for testing and populating the database. It simulates real-world customer, order, and restaurant data and saves them as CSV files. This is particularly useful for developers who want to populate their database with random but realistic data.

The script generates sample data for:
    Customers (names, email addresses, phone numbers, etc.)
    Orders (order IDs, customer IDs, restaurant IDs, etc.)
    Restaurants (restaurant names, cuisines, etc.)
    Deliveries (Delivery_id ,order_id, etc.)
    The generated data is saved in the synthetic_datasets/ folder, where you can use the CSV files to populate the database or for other testing purposes.
