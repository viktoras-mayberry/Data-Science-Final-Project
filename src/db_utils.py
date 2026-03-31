"""
Database Utilities
==================
Helper functions for connecting to PostgreSQL and loading data.

Usage:
    from src.db_utils import get_engine, run_query, load_table
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_engine():
    """
    Create and return a SQLAlchemy engine for PostgreSQL.

    The connection details are read from the .env file:
        DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

    Returns:
        sqlalchemy.engine.Engine: Database engine instance.

    Example:
        engine = get_engine()
        df = pd.read_sql("SELECT * FROM customers LIMIT 5", engine)
    """
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "telco_churn")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    engine = create_engine(connection_string)

    return engine


def run_query(query, engine=None):
    """
    Execute a SQL query and return the results as a DataFrame.

    Args:
        query (str): SQL query to execute.
        engine: SQLAlchemy engine. If None, creates one automatically.

    Returns:
        pd.DataFrame: Query results.

    Example:
        df = run_query("SELECT * FROM customers WHERE tenure > 12")
    """
    if engine is None:
        engine = get_engine()

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return df


def load_table(table_name, engine=None):
    """
    Load an entire table into a DataFrame.

    Args:
        table_name (str): Name of the PostgreSQL table.
        engine: SQLAlchemy engine. If None, creates one automatically.

    Returns:
        pd.DataFrame: All rows from the table.

    Example:
        customers_df = load_table("customers")
    """
    return run_query(f"SELECT * FROM {table_name}", engine)


def load_full_dataset(engine=None):
    """
    Load the full dataset by joining all three tables.

    This performs a SQL JOIN across customers, services, and billing
    to reconstruct the original dataset.

    Args:
        engine: SQLAlchemy engine. If None, creates one automatically.

    Returns:
        pd.DataFrame: Complete dataset with all columns.

    Example:
        df = load_full_dataset()
        print(df.shape)
    """
    query = """
        SELECT
            c.customer_id,
            c.gender,
            c.senior_citizen,
            c.partner,
            c.dependents,
            c.tenure,
            s.phone_service,
            s.multiple_lines,
            s.internet_service,
            s.online_security,
            s.online_backup,
            s.device_protection,
            s.tech_support,
            s.streaming_tv,
            s.streaming_movies,
            b.contract,
            b.paperless_billing,
            b.payment_method,
            b.monthly_charges,
            b.total_charges,
            b.churn
        FROM customers c
        JOIN services s ON c.customer_id = s.customer_id
        JOIN billing b ON c.customer_id = b.customer_id
    """
    return run_query(query, engine)


def test_connection():
    """
    Test the PostgreSQL connection and print status.

    Returns:
        bool: True if connection is successful, False otherwise.

    Example:
        if test_connection():
            print("Ready to go!")
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        print("✅ PostgreSQL connection successful!")
        print(f"   Database: {os.getenv('DB_NAME', 'telco_churn')}")
        print(f"   Host: {os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
