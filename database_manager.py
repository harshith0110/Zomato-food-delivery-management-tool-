import sqlite3
import logging
from typing import List, Tuple, Union


class DatabaseManager:
    """Encapsulates database operations in a reusable and scalable manner."""

    def __init__(self, db_path="database_scripts/zomata_database.db"):
        """
        Initialize the database connection.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)

    def _connect(self):
        """Establish a connection to the SQLite database."""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise

    def execute_query(self, query: str, params: Tuple = ()) -> None:
        """
        Execute an SQL query (for INSERT, UPDATE, DELETE).
        :param query: SQL query string.
        :param params: Tuple of parameters for the query.
        """
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                self.logger.info(f"Query executed successfully: {query} | Params: {params}")
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e} | Query: {query} | Params: {params}")
            raise

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """
        Fetch all rows for a given query.
        :param query: SQL query string.
        :param params: Tuple of parameters for the query.
        :return: List of rows.
        """
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                self.logger.info(f"Fetched {len(rows)} rows for query: {query} | Params: {params}")
                return rows
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e} | Query: {query} | Params: {params}")
            raise

    def create_table(self, table_name: str, columns: str) -> None:
        """
        Dynamically create a table.
        :param table_name: Name of the table.
        :param columns: Column definitions (e.g., "id INTEGER PRIMARY KEY, name TEXT").
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        self.execute_query(query)

    def add_column(self, table_name: str, column_definition: str) -> None:
        """
        Add a new column to an existing table.
        :param table_name: Name of the table.
        :param column_definition: Column definition (e.g., "new_column TEXT").
        """
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_definition};"
        self.execute_query(query)

    def insert_record(self, table_name: str, columns: str, values: Tuple) -> None:
        """
        Insert a record into a table.
        :param table_name: Name of the table.
        :param columns: Comma-separated column names.
        :param values: Tuple of values to insert.
        """
        placeholders = ", ".join("?" for _ in values)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        self.execute_query(query, values)

    def update_record(self, table_name: str, set_clause: str, where_clause: str, params: Tuple) -> None:
        """
        Update a record in a table.
        :param table_name: Name of the table.
        :param set_clause: SET clause for the query (e.g., "name = ?").
        :param where_clause: WHERE clause for the query (e.g., "id = ?").
        :param params: Tuple of parameters for the query.
        """
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
        self.execute_query(query, params)

    def delete_record(self, table_name: str, where_clause: str, params: Tuple) -> None:
        """
        Delete a record from a table.
        :param table_name: Name of the table.
        :param where_clause: WHERE clause for the query (e.g., "id = ?").
        :param params: Tuple of parameters for the query.
        """
        query = f"DELETE FROM {table_name} WHERE {where_clause};"
        self.execute_query(query, params)

    def get_table_data(self, table_name: str) -> List[Tuple]:
        """
        Fetch all data from a table.
        :param table_name: Name of the table.
        :return: List of rows.
        """
        query = f"SELECT * FROM {table_name};"
        return self.fetch_all(query)

    def drop_table(self, table_name: str) -> None:
        """
        Drop a table from the database.
        :param table_name: Name of the table.
        """
        query = f"DROP TABLE IF EXISTS {table_name};"
        self.execute_query(query)

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        :param table_name: Name of the table.
        :return: Boolean indicating existence.
        """
        query = """
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name=?;
        """
        result = self.fetch_all(query, (table_name,))
        exists = len(result) > 0
        self.logger.info(f"Table '{table_name}' exists: {exists}")
        return exists

    def fetch_column_names(self, table_name: str) -> Union[List[str], None]:
        """
        Fetch column names for a given table.
        :param table_name: Name of the table.
        :return: List of column names or None if the table doesn't exist.
        """
        if not self.table_exists(table_name):
            self.logger.warning(f"Table '{table_name}' does not exist.")
            return None
        query = f"PRAGMA table_info({table_name});"
        columns_info = self.fetch_all(query)
        column_names = [col_info[1] for col_info in columns_info]
        self.logger.info(f"Columns in table '{table_name}': {column_names}")
        return column_names
