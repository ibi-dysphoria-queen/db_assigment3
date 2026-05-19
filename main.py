# Import all libraries we will use in this notebook.
import sqlite3
import random
from datetime import datetime, timedelta
from random import randint, randrange


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
    'UsedPart',
    'Repair',
    'Ticket',
    'Part',
    'Supplier',
    'Employee',
    'Customer',
    'Payment',
    'ContactEvent'
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
        tax_number      TEXT,
        discount_eligibility TEXT    NOT NULL DEFAULT 'None',


    );
""")

conn.commit()
print("Customer table created.")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee (
        employee_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name      TEXT    NOT NULL,
        last_name       TEXT    NOT NULL,
        phone           TEXT    NOT NULL UNIQUE,
        email           TEXT, NOT NULL UNIQUE,
        occupation      TEXT NOT NULL
    );
""")

conn.commit()
print("Employee table created.")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Supplier (
        name TEXT  PRIMARY kEY NOT NULL,
        location    TEXT    NOT NULL

    );
""")

conn.commit()
print("supplier table created.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ticket (
        ticket_no     INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
        problem      TEXT    NOT NULL,
        speed_estimate       TEXT    NOT NULL
        device_name           TEXT    NOT NULL,
        passcode TEXT,
        status TEXT NOT NULL
    );
""")

conn.commit()
print("ticket table created.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Repair (
        repair_id INTEGER PRIMARY KET AUTOINCREMENT,
        repair_type TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
        FOREIGN KEY (ticket_no) REFERENCES Ticket(ticket_no)),
    );
""")
conn.commit()
print("repair table created.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Part (
        part_id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_number     INTEGER ,
        FOREIGN KEY (name) REFERENCES Supplier(name)),
        quality TEXT    NOT NULL,
        manufacturer      TEXT    NOT NULL,
        part_type       TEXT    NOT NULL,
    );
""")
conn.commit()
print("part table created.")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS UsedPart (
        FOREIGN KEY (part_id) REFERENCES Part(part_id)),
        FOREIGN KEY (repair_id) REFERENCES Repair(repair_id)),
        PRIMARY KEY(repair_id, part_id)
    );
""")
conn.commit()
print("usedpart table created.")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        FOREIGN KEY (ticket_no) REFERENCES Ticket(ticket_no)),
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_ammount FLOAT, NOT NULL,
        payment_method    TEXT    NOT NULL CHECK(payment_method IN ('check', 'card','cash'))
    );
""")
conn.commit()
print("Payment table created.")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ContactEvent (
        FOREIGN KEY (ticket_no) REFERENCES Ticket(ticket_no)),
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT, NOT NULL,
        contact_type    TEXT    NOT NULL CHECK(contact_type IN ('call', 'sms','email')),
        contact_adress TEXT NOT NULL
    );
""")
conn.commit()
print("ContactEvent table created.")



#random data start
num_customers = 50

for i in range(num_customers):
    # 80% private customers, 20% corporate.
    c_type = random.choices(['private', 'corporate'], weights=[0.8, 0.2])[0]

    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.unique.phone_number()
    # Around 70% of customers give an email address; the rest do not.
    email = fake.email() if random.random() < 0.7 else None
    # Companies have a company name and an Austrian tax number; private customers do not.
    company = fake.company() if c_type == 'corporate' else None
    tax_nr = f"ATU{random.randint(10000000, 99999999)}" if c_type == 'corporate' else None
    discount_eligibility = random.choices([.25,30,10,100,40]) if random.random() < 0.5 else None
    cursor.execute("""
        INSERT INTO Customer
            (first_name, last_name, phone, email, customer_type, company_name, tax_number)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (first_name, last_name, phone, email, c_type, company, tax_nr))

conn.commit()
print(f"Inserted {num_customers} customers.")
#ticket
num_tickets = 250
for i in range(num_tickets):
    cursor.execute("SELECT customer_id FROM Customer;")
    customer_ids = [row[0] for row in cursor.fetchall()]
    chosen_id = random.choice(customer_ids)
    problem = fake.text()
    speed_estimate = fake.text()
    device_name = random.choices([
    ('Apple',   'iPhone 12'),
    ('Apple',   'iPhone 13'),
    ('Apple',   'iPhone 14'),
    ('Samsung', 'Galaxy S21'),
    ('Samsung', 'Galaxy S22'),
    ('Samsung', 'Galaxy A53'),
    ('Google',  'Pixel 7'),
    ('Xiaomi',  'Redmi Note 11'),
])
    password = fake.password(randint(3,20)) if random.random() < 0.7 else None
    status = random.choices(['ready for pickup', 'waiting for appraisal','in our partners hand', 'undergoing repair'])
    cursor.execute("""
                   INSERT INTO Ticket
                   ( customer_id,deposit, problem, speed_estimate, device_name, password, diagnostic_fee, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (chosen_id, problem, speed_estimate, device_name, password, status))

conn.commit()
print(f"Inserted {num_tickets} tickets.")
#supplier
num_suppliers = 5
for i in range(num_suppliers):
    name = fake.company()
    location = fake.city()
    cursor.execute("""
                   INSERT INTO Supplier
                   (name,location)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (name, location))

conn.commit()
print(f"Inserted {num_suppliers} suppliers.")
#employees
num_employees = 5
for i in range(num_employees):
    name_f = fake.first_name
    name_l = fake.last_name()
    phone = fake.unique.phone_number()
    email = fake.email()
    occupation = random.choices(['repair tech','front desk','accountant'])
    cursor.execute("""
                   INSERT INTO Supplier
                   (first_name,last_name,phone,email,occupation)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (first_name, last_name, phone, email, occupation))

conn.commit()
print(f"Inserted {num_employees} employees.")

#parts
num_parts = 30
for i in range(num_parts):
    serial_number = random.randint(10000000, 99999999)
    cursor.execute("SELECT name FROM Supplier;")
    customer_ids = [row[0] for row in cursor.fetchall()]
    chosen_id = random.choice(customer_ids)
    quality = random.choices(['good', 'bad','mid'])
    manufacturer = fake.company()
    part_type = random.choices(['screen','battery','camera','motherboard','housing','port','fingerprint reader'])
    cursor.execute("""
                   INSERT INTO Supplier
                   (serial_number,chosen_id,quality,manufacturer,part_type)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (serial_number, chosen_id, quality, manufacturer, part_type))

conn.commit()
print(f"Inserted {num_parts} parts.")

#repair
num_repair = 250
for i in range(num_repair):
    repair_type = random.choices([
    ('Screen replacement',     randrange(120,250)),
    ('Battery replacement',    randrange( 60, 120)),
    ('Charging port repair',   randrange( 70, 140)),
    ('Back glass replacement',  randrange(80, 180)),
    ('Water damage diagnosis', randrange( 25,  25)),
    ('Data recovery',          randrange( 40, 150)),
])
    cursor.execute("SELECT employee_id FROM Employee;")
    employee_ids = [row[0] for row in cursor.fetchall()]
    chosen_employee_id = random.choice(employee_ids)
    cursor.execute("SELECT ticket_no FROM Ticket;")
    ticket_ids = [row[0] for row in cursor.fetchall()]
    chosen_ticket_id = random.choice(ticket_ids)


    cursor.execute("""
                   INSERT INTO Supplier
                   (repair_type,employee_id,ticket_no)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (repair_type, chosen_employee_id, chosen_ticket_id))

conn.commit()
print(f"Inserted {num_repair} repairs.")

#usedparts
num_used_parts = 400
for i in range(num_used_parts):
    cursor.execute("SELECT part_id FROM Part;")
    part_ids = [row[0] for row in cursor.fetchall()]
    chosen_part_id = random.choice(part_ids)
    cursor.execute("SELECT repair_id FROM Repair;")
    repair_ids = [row[0] for row in cursor.fetchall()]
    chosen_repair_id = random.choice(repair_ids)

    cursor.execute("""
                   INSERT INTO UsedPart
                   (part_id,repair_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (chosen_part_id, chosen_repair_id))
conn.commit()
print(f"Inserted {num_used_parts} used parts.")
#Payment
num_payment = 200
for i in range(num_payment):
    cursor.execute("SELECT ticket_no FROM Ticket;")
    ticket_ids = [row[0] for row in cursor.fetchall()]
    chosen_ticket_id = random.choice(ticket_ids)
    payment = randrange(1,200)
    payment_method = random.choices(['check', 'card','cash'])
    cursor.execute("""
                   INSERT INTO Payment
                   (ticket_no,payment_amount,payment_method)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (chosen_ticket_id, payment, payment_method))
conn.commit()
print(f"Inserted {num_payment} payments.")
#ContactEvent
num_contacts = 200
for i in range(num_contacts):
    cursor.execute("SELECT ticket_no FROM Ticket;")
    ticket_ids = [row[0] for row in cursor.fetchall()]
    chosen_ticket_id = random.choice(ticket_ids)
    message = fake.text()
    contact_type = random.choices(['call', 'SMS','Mail'])
    adress = fake.email() if random.random() < 0.6 else fake.unique.phone_number()
    cursor.execute("""
                   INSERT INTO ContactEvent
                   (ticket_no,payment_amount,payment_method)
                   VALUES (?, ?, ?, ?, ?, ?, ?);
                   """, (chosen_ticket_id, payment, payment_method))
conn.commit()
print(f"Inserted {num_contacts} contactevents.")
