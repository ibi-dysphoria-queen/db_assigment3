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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ticket (
        ticket_no     INTEGER PRIMARY KEY AUTOINCREMENT,
        deposit FLOAT    NOT NULL,
        problem      TEXT    NOT NULL,
        speed_estimate       TEXT    NOT NULL
        manufacturer           TEXT    NOT NULL,
        passocde TEXT
        additional_repair TEXT
        diagnostic_fee FLOAT
        status TEXT NOT NULL
    );
""")

conn.commit()
print("ticket table created.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS CompletedOrderForm (
        ticket_no     INTEGER PRIMARY KEY ,
        final_cost FLOAT    NOT NULl
        completion_date DATE NOT NULL,
        warrany_coverage      TEXT    NOT NULL,
        speed_estimate       TEXT    NOT NULL
        manufacturer           TEXT    NOT NULL,
        passocde TEXT
        additional_repair TEXT
        diagnostic_fee FLOAT
        extra_notes TEXT
    );
""")

conn.commit()
print("CompletedOrderForm table created.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Device (
        serial_number     TEXT PRIMARY KEY ,
        quality TEXT    NOT NULL,
        supplier      TEXT    NOT NULL,
        part_type       TEXT    NOT NULL,
        manufacturer           TEXT    NOT NULL,
    );
""")
conn.commit()
print("part table created.")


num_customers = 50

for i in range(num_customers):
    # 80% private customers, 20% corporate.
    d_type = random.choices(['private', 'corporate'], weights=[0.8, 0.2])[0]
    phone_moder =random.choices([
    ('Apple',   'iPhone 12'),
    ('Apple',   'iPhone 13'),
    ('Apple',   'iPhone 14'),
    ('Samsung', 'Galaxy S21'),
    ('Samsung', 'Galaxy S22'),
    ('Samsung', 'Galaxy A53'),
    ('Google',  'Pixel 7'),
    ('Xiaomi',  'Redmi Note 11'),
])
    last_name = fake.last_name()
    phone = fake.unique.phone_number()
    # Around 70% of customers give an email address; the rest do not.
    email = fake.email() if random.random() < 0.7 else None
    # Companies have a company name and an Austrian tax number; private customers do not.
    company = fake.company() if c_type == 'corporate' else None
    tax_nr = f"ATU{random.randint(10000000, 99999999)}" if c_type == 'corporate' else None

    cursor.execute("""
                   INSERT INTO Customer
                   (first_name, last_name, phone, email, customer_type, company_name, tax_number)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (first_name, last_name, phone, email, c_type, company, tax_nr))

conn.commit()
print(f"Inserted {num_customers} customers.")

num_devices = 50

for i in range(num_devices):
    c_type = random.choices(['phone', 'tablet'], weights=[0.8, 0.2])[0]

    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.unique.phone_number()
    # Around 70% of customers give an email address; the rest do not.
    email = fake.email() if random.random() < 0.7 else None
    # Companies have a company name and an Austrian tax number; private customers do not.
    company = fake.company() if c_type == 'corporate' else None
    tax_nr = f"ATU{random.randint(10000000, 99999999)}" if c_type == 'corporate' else None

    cursor.execute("""
                   INSERT INTO Customer
                   (first_name, last_name, phone, email, customer_type, company_name, tax_number)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (first_name, last_name, phone, email, c_type, company, tax_nr))

conn.commit()
print(f"Inserted {num_customers} customers.")