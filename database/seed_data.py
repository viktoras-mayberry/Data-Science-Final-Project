"""
Seed Script — Load Telco Customer Churn CSV into PostgreSQL

This script reads the Telco Customer Churn CSV file and populates
the three normalized tables (customers, services, billing) in
your PostgreSQL database.

Prerequisites:
    1. PostgreSQL is running and the 'telco_churn' database exists
    2. The schema has been created (run database/schema.sql first)
    3. The CSV file is at: data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
    4. A .env file exists in the project root with your DB credentials

Usage:
    python database/seed_data.py
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# ── Load environment variables ──────────────────────────────────
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "telco_churn")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# ── Path to the dataset ────────────────────────────────────────
CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)


def get_connection():
    """Create and return a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Could not connect to PostgreSQL: {e}")
        print("\nPlease check:")
        print("  1. PostgreSQL is running")
        print("  2. The 'telco_churn' database exists")
        print("  3. Your .env file has the correct credentials")
        sys.exit(1)


def load_csv():
    """Load and validate the CSV dataset."""
    if not os.path.exists(CSV_PATH):
        print(f"❌ CSV file not found at: {CSV_PATH}")
        print("\nPlease download the Telco Customer Churn dataset from:")
        print("  https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
        print(f"\nThen place it at: {CSV_PATH}")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)
    print(f"✅ Loaded CSV: {len(df)} rows, {len(df.columns)} columns")

    # Clean TotalCharges — convert empty strings to NaN, then to float
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    return df


def seed_customers(conn, df):
    """Insert data into the customers table."""
    cursor = conn.cursor()

    # Prepare customer data
    customers = df[["customerID", "gender", "SeniorCitizen", "Partner",
                     "Dependents", "tenure"]].values.tolist()

    query = """
        INSERT INTO customers (customer_id, gender, senior_citizen,
                               partner, dependents, tenure)
        VALUES %s
        ON CONFLICT (customer_id) DO NOTHING
    """
    execute_values(cursor, query, customers)
    conn.commit()
    print(f"  ✅ Inserted {len(customers)} rows into 'customers' table")


def seed_services(conn, df):
    """Insert data into the services table."""
    cursor = conn.cursor()

    services = df[["customerID", "PhoneService", "MultipleLines",
                    "InternetService", "OnlineSecurity", "OnlineBackup",
                    "DeviceProtection", "TechSupport", "StreamingTV",
                    "StreamingMovies"]].values.tolist()

    query = """
        INSERT INTO services (customer_id, phone_service, multiple_lines,
                              internet_service, online_security, online_backup,
                              device_protection, tech_support, streaming_tv,
                              streaming_movies)
        VALUES %s
    """
    execute_values(cursor, query, services)
    conn.commit()
    print(f"  ✅ Inserted {len(services)} rows into 'services' table")


def seed_billing(conn, df):
    """Insert data into the billing table."""
    cursor = conn.cursor()

    # Prepare billing data — handle NaN in TotalCharges
    billing_data = []
    for _, row in df.iterrows():
        total_charges = None if pd.isna(row["TotalCharges"]) else float(row["TotalCharges"])
        billing_data.append((
            row["customerID"],
            row["Contract"],
            row["PaperlessBilling"],
            row["PaymentMethod"],
            float(row["MonthlyCharges"]),
            total_charges,
            row["Churn"]
        ))

    query = """
        INSERT INTO billing (customer_id, contract, paperless_billing,
                             payment_method, monthly_charges, total_charges, churn)
        VALUES %s
    """
    execute_values(cursor, query, billing_data)
    conn.commit()
    print(f"  ✅ Inserted {len(billing_data)} rows into 'billing' table")


def verify_data(conn):
    """Run verification queries to check the seeded data."""
    cursor = conn.cursor()

    print("\n── Verification ─────────────────────────────────────")

    tables = ["customers", "services", "billing"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  📊 {table}: {count} rows")

    # Check churn distribution
    cursor.execute("SELECT churn, COUNT(*) FROM billing GROUP BY churn ORDER BY churn")
    print("\n  📊 Churn distribution:")
    for row in cursor.fetchall():
        print(f"     {row[0]}: {row[1]} customers")


def main():
    """Main execution flow."""
    print("=" * 55)
    print("  Telco Customer Churn — Database Seeder")
    print("=" * 55)

    # Load CSV
    print("\n📂 Loading CSV dataset...")
    df = load_csv()

    # Connect to PostgreSQL
    print(f"\n🔌 Connecting to PostgreSQL ({DB_HOST}:{DB_PORT}/{DB_NAME})...")
    conn = get_connection()
    print("✅ Connected successfully!")

    # Seed tables
    print("\n📥 Seeding database tables...")
    seed_customers(conn, df)
    seed_services(conn, df)
    seed_billing(conn, df)

    # Verify
    verify_data(conn)

    # Close connection
    conn.close()

    print("\n" + "=" * 55)
    print("  ✅ Database seeding complete!")
    print("=" * 55)
    print("\nYou can now verify the data in pgAdmin:")
    print("  1. Open pgAdmin → telco_churn database")
    print("  2. Tools → Query Tool")
    print("  3. Run: SELECT * FROM customers LIMIT 10;")


if __name__ == "__main__":
    main()
