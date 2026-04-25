"""
Logistics Portfolio - Insert Shipment data directly into Azure SQL DB
=====================================================================
Install required libraries:
    pip install pyodbc pandas

How to run:
    python insert_shipment.py

Requirements:
    - ODBC Driver 17 or 18 for SQL Server must be installed
    - Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
"""

import pyodbc
import pandas as pd

# ============================================================
# Configuration - fill in your values
# ============================================================
SERVER   = "sql-logistics-portfolio.database.windows.net"
DATABASE = "logistics-db"
USERNAME = "sqladmin"
PASSWORD = os.environ.get("AZURE_SQL_PASSWORD")
CSV_PATH = "data/Shipment.csv"

# ============================================================
# Connect to Azure SQL Database
# ============================================================
def get_connection():
    drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
    if not drivers:
        raise RuntimeError(
            "No ODBC Driver for SQL Server found.\n"
            "Please install from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server"
        )
    driver = drivers[-1]
    print(f"Using driver: {driver}")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_str)

# ============================================================
# Insert Shipment data
# ============================================================
def insert_shipment():
    print("Reading Shipment.csv...")
    df = pd.read_csv(CSV_PATH)

    # Convert date columns to proper format
    df['scheduled_date'] = pd.to_datetime(df['scheduled_date']).dt.date
    df['actual_date']    = pd.to_datetime(df['actual_date']).dt.date
    df['created_at']     = pd.to_datetime(df['created_at']).dt.date

    print(f"Rows to insert: {len(df)}")

    conn   = get_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM dbo.Shipment")
    conn.commit()
    print("Cleared existing Shipment data.")

    # Enable IDENTITY_INSERT to allow explicit shipment_id values
    cursor.execute("SET IDENTITY_INSERT dbo.Shipment ON")
    conn.commit()

    # Insert rows in batches
    batch_size = 500
    total      = len(df)
    inserted   = 0

    sql = """
        INSERT INTO dbo.Shipment
            (shipment_id, so_id, warehouse_id, scheduled_date,
             actual_date, carrier, tracking_no, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for i in range(0, total, batch_size):
        batch = df.iloc[i:i + batch_size]
        rows  = [
            (
                int(row.shipment_id),
                int(row.so_id),
                int(row.warehouse_id),
                row.scheduled_date,
                row.actual_date,
                str(row.carrier),
                str(row.tracking_no),
                str(row.status),
                row.created_at,
            )
            for row in batch.itertuples(index=False)
        ]
        cursor.executemany(sql, rows)
        conn.commit()
        inserted += len(rows)
        print(f"  Inserted {inserted}/{total} rows...")

    # Disable IDENTITY_INSERT
    cursor.execute("SET IDENTITY_INSERT dbo.Shipment OFF")
    conn.commit()

    cursor.close()
    conn.close()

    print(f"\n=== Complete ===")
    print(f"Successfully inserted {inserted} rows into dbo.Shipment")

if __name__ == "__main__":
    insert_shipment()