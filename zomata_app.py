import streamlit as st
import pandas as pd
import sys
import os
import logging

# Add project root to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from oop_database.database_manager import DatabaseManager
from insights_visualization.data_insights import DataInsights

# Database Configuration
DB_PATH = "database_scripts/zomata_database.db"

# Initialize Database Manager and Data Insights
db_manager = DatabaseManager(DB_PATH)
data_insights = DataInsights(DB_PATH)

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Streamlit App
def main():
    st.title("Zomato - Food Delivery Management Tool")

    # Fetch dynamic menu
    existing_tables = db_manager.fetch_all(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    menu = ["Home"] + [f"Manage {table[0]}" for table in existing_tables] + ["Add/Modify Tables", "Insights"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        show_home()

    elif choice.startswith("Manage "):
        # Extract the table name from the menu choice
        table_name = choice.replace("Manage ", "")
        manage_table(table_name)

    elif choice == "Add/Modify Tables":
        add_or_modify_tables()

    elif choice == "Insights":
        show_insights()


def show_home():
    """Display the home page."""
    st.subheader("Welcome to Zomato Management Tool")
    st.write("Use the sidebar to navigate through different functionalities.")

def manage_table(table_name):
    """Handle CRUD operations for a given table."""
    st.subheader(f"Manage {table_name}")

    if not db_manager.table_exists(table_name):
        st.error(f"Table '{table_name}' does not exist.")
        return

    # Fetch current data and columns
    data, columns = fetch_table_data(table_name)

    # Display Table Data
    if data:
        st.dataframe(pd.DataFrame(data, columns=columns))
    else:
        st.info(f"No data available in {table_name}.")

    # CRUD Operations
    add_record(table_name, columns)
    update_or_delete_record(table_name, columns)

def fetch_table_data(table_name):
    """Fetch data and column names for a table."""
    data = db_manager.get_table_data(table_name)
    columns = db_manager.fetch_column_names(table_name)
    return data, columns

def add_record(table_name, columns):
    """Add a new record to the table."""
    with st.expander(f"Add New {table_name[:-1]}"):
        new_record = [st.text_input(f"Enter {col}") for col in columns]
        if st.button(f"Add {table_name[:-1]}"):
            try:
                db_manager.insert_record(table_name, ", ".join(columns), tuple(new_record))
                st.success(f"New {table_name[:-1]} added successfully!")
                st.rerun()  # Trigger a rerun to update the table view
            except Exception as e:
                st.error(f"Error adding new record: {e}")

def update_or_delete_record(table_name, columns):
    """Handle updating or deleting a record."""
    with st.expander(f"Update/Delete {table_name[:-1]}"):
        selected_id = st.text_input(f"Enter {columns[0]} to Update/Delete")
        action = st.radio("Select Action", ["Update", "Delete"], horizontal=True)

        if action == "Delete" and st.button("Delete"):
            delete_record(table_name, columns[0], selected_id)

        elif action == "Update":
            update_record(table_name, columns, selected_id)

def delete_record(table_name, id_column, record_id):
    """Delete a record from the table."""
    try:
        db_manager.delete_record(table_name, f"{id_column} = ?", (record_id,))
        st.success(f"Record deleted successfully!")
        st.rerun()  # Trigger a rerun to update the table view
    except Exception as e:
        st.error(f"Error deleting record: {e}")

def update_record(table_name, columns, record_id):
    """Update a record in the table."""
    updated_values = [st.text_input(f"Update {col}") for col in columns[1:]]
    if st.button("Update"):
        try:
            set_clause = ", ".join([f"{col} = ?" for col in columns[1:]])
            db_manager.update_record(
                table_name, set_clause, f"{columns[0]} = ?", tuple(updated_values) + (record_id,)
            )
            st.success(f"Record updated successfully!")
            st.rerun()  # Trigger a rerun to update the table view
        except Exception as e:
            st.error(f"Error updating record: {e}")

def add_or_modify_tables():
    """Allow users to add new tables, modify existing ones, or delete tables/columns."""
    st.subheader("Add, Modify, or Delete Tables")

    # Create a New Table
    with st.expander("Create New Table"):
        new_table_name = st.text_input("Enter New Table Name")
        schema = st.text_area("Define Table Schema (e.g., column_name column_type, ...)")
        if st.button("Create Table"):
            try:
                db_manager.create_table(new_table_name, schema)
                st.success(f"Table '{new_table_name}' created successfully!")
                st.rerun()  # Trigger a rerun to refresh the tables list
            except Exception as e:
                st.error(f"Error creating table: {e}")

    # Add Column to Existing Table
    with st.expander("Add Column to Table"):
        table_name = st.text_input("Enter Table Name to Add Column")
        column_name = st.text_input("New Column Name")
        column_type = st.selectbox("Column Type", ["TEXT", "INTEGER", "REAL", "BOOLEAN"])
        if st.button("Add Column"):
            try:
                db_manager.add_column(table_name, f"{column_name} {column_type}")
                st.success(f"Column '{column_name}' added to '{table_name}' successfully!")
                st.rerun()  # Trigger a rerun to refresh the table
            except Exception as e:
                st.error(f"Error adding column: {e}")

    # Delete a Table
    with st.expander("Delete Table"):
        delete_table_name = st.text_input("Enter Table Name to Delete")
        if st.button("Delete Table"):
            try:
                db_manager.drop_table(delete_table_name)
                st.success(f"Table '{delete_table_name}' deleted successfully!")
                st.rerun()  # Trigger a rerun to refresh the tables list
            except Exception as e:
                st.error(f"Error deleting table: {e}")

    # Delete a Column
    with st.expander("Delete Column from Table"):
        modify_table_name = st.text_input("Enter Table Name to Modify")
        if modify_table_name:
            column_names = db_manager.fetch_column_names(modify_table_name)
            if column_names:
                column_to_delete = st.selectbox("Select Column to Delete", column_names)
                if st.button("Delete Column"):
                    try:
                        db_manager.execute_query(
                            f"ALTER TABLE {modify_table_name} DROP COLUMN {column_to_delete};"
                        )
                        st.success(f"Column '{column_to_delete}' deleted successfully from '{modify_table_name}'!")
                        st.rerun()  # Trigger a rerun to refresh the table
                    except Exception as e:
                        st.error(f"Error deleting column: {e}")
            else:
                st.warning(f"No columns found in table '{modify_table_name}'!")

def show_insights():
    """Display data insights and visualizations dynamically."""
    st.subheader("Data Insights and Visualization")

    # Dropdown for selecting insights
    insights_options = [
        "Peak Ordering Times",
        "Top Customers",
        "Top Restaurants",
        "Popular Cuisines",
        "Average Delivery Times",
        "Top Feedback Summary",
        "Bottom Feedback Summary",
        "Orders by Day",
        "Orders by Month",
        "Most Ordered Items",
        "Order Value by Restaurant",
        "Average Feedback by Restaurant",
        "Order Distribution by Feedback",
        "Most Active Delivery Persons",
        "Top Customer Locations",
        "Most Ordered Cuisine by Customer",
        "Order Count by Hour",
        "Top Restaurants by Rating",
        "Peak Ordering Days",
        "Highest Rated Customers",
        "Top Rated Restaurants",
    ]
    selected_insights = st.multiselect("Select Insights to View:", insights_options)

    if not selected_insights:
        st.info("Please select insights from the dropdown above to display visualizations.")
        return

    # Mapping insights to corresponding methods in DataInsights
    insight_methods = {
        "Peak Ordering Times": data_insights.fetch_and_visualize_peak_ordering_times,
        "Top Customers": data_insights.fetch_and_visualize_top_customers,
        "Top Restaurants": data_insights.fetch_and_visualize_top_restaurants,
        "Popular Cuisines": data_insights.fetch_and_visualize_popular_cuisines,
        "Average Delivery Times": data_insights.fetch_and_visualize_average_delivery_times,
        "Top Feedback Summary": lambda: data_insights.fetch_and_visualize_feedback_summary(top=True),
        "Bottom Feedback Summary": lambda: data_insights.fetch_and_visualize_feedback_summary(top=False),
        "Orders by Day": data_insights.fetch_and_visualize_orders_by_day,
        "Orders by Month": data_insights.fetch_and_visualize_orders_by_month,
        "Most Ordered Items": data_insights.fetch_and_visualize_most_ordered_items,
        "Order Value by Restaurant": data_insights.fetch_and_visualize_order_value_by_restaurant,
        "Average Feedback by Restaurant": data_insights.fetch_and_visualize_avg_feedback_by_restaurant,
        "Order Distribution by Feedback": data_insights.fetch_and_visualize_order_distribution_by_feedback,
        "Most Active Delivery Persons": data_insights.fetch_and_visualize_most_active_delivery_persons,
        "Top Customer Locations": data_insights.fetch_and_visualize_top_customer_locations,
        "Most Ordered Cuisine by Customer": data_insights.fetch_and_visualize_most_ordered_cuisine_by_customer,
        "Order Count by Hour": data_insights.fetch_and_visualize_order_count_by_hour,
        "Top Restaurants by Rating": data_insights.fetch_and_visualize_top_restaurants_by_rating,
        "Peak Ordering Days": data_insights.fetch_and_visualize_peak_ordering_days,
        "Highest Rated Customers": data_insights.fetch_and_visualize_highest_rated_customers,
        "Top Rated Restaurants": data_insights.fetch_and_visualize_top_rated_restaurants,
    }

    for selected_insight in selected_insights:
        st.write(f"### {selected_insight}")
        fetch_visualize_method = insight_methods.get(selected_insight)

        if fetch_visualize_method:
            try:
                # Fetch data and visualization
                data, fig = fetch_visualize_method()

                # Display data
                if not data.empty:
                    st.table(data)
                else:
                    st.warning(f"No data available for {selected_insight}.")

                # Display visualization if available
                if fig:
                    st.plotly_chart(fig)
            except Exception as e:
                st.error(f"An error occurred while processing {selected_insight}: {e}")

if __name__ == "__main__":
    main()
