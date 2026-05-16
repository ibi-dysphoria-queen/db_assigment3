# Import all libraries we will use in this notebook.
import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

# Create a Faker instance localised to Austrian German for realistic names.
fake = Faker('de_AT')

# Fix the random seed so the "random" data is reproducible;
# when the grader runs your notebook, the same values appear.
random.seed(42)
Faker.seed(42)

print("Setup complete. Libraries are ready.")
# Open (or create) the database file and connect to it.
conn = sqlite3.connect('kremsfix.db')

# Create a cursor; we use it to execute SQL statements.
cursor = conn.cursor()

# SQLite does not enforce foreign keys by default; turn it on.
cursor.execute("PRAGMA foreign_keys = ON;")

print("Connected to kremsfix.db.")
# Add every table you create to this list, in reverse dependency order.
tables_to_drop = [
    # 'UsedPart',
    # 'Repair',
    # 'Ticket',
    # 'Part',
    # 'Supplier',
    # 'Employee',
    'Customer',
    # ... add the rest of your tables here
]

for table_name in tables_to_drop:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

conn.commit()
print(f"Checked {len(tables_to_drop)} tables for drop.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name      TEXT    NOT NULL,
        last_name       TEXT    NOT NULL,
        phone           TEXT    NOT NULL UNIQUE,
        email           TEXT,
        customer_type   TEXT    NOT NULL CHECK(customer_type IN ('private', 'corporate')),
        company_name    TEXT,
        tax_number      TEXT
    );
""")

conn.commit()
print("Customer table created.")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Device (
        device_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        device_type TEXT    NOT NULL,
        customized_version_number      TEXT    NOT NULL,
        model       TEXT    NOT NULL,
        manufacturer           TEXT    NOT NULL,
        passocde TEXT
    );
""")

conn.commit()
print("device table created.")
