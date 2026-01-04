# LLM mostly

import os
import random
from datetime import datetime, timedelta
import mysql.connector

PEOPLE_COUNT = 1000
DAYS_BACK = 365
MADE_CUPS_COUNT = 500000
DRANK_CUPS_COUNT = 800000
INSERT_BATCH_SIZE = 100000

# ---- DB CONFIG ----
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# ---- DATA ----
tea_types = ["black", "green", "herbal", "oolong", "chai", "earl_grey"]
people = list(range(1, PEOPLE_COUNT+1))  
now = datetime.now()

def random_time(days_back=DAYS_BACK):
    return now - timedelta(
        days=random.randint(0, days_back),
        minutes=random.randint(0, 1440),
        seconds=random.randint(0, 60),
        milliseconds=random.randint(0, 1000)
    )

def batch_insert(conn, table, columns, data, batch_size=INSERT_BATCH_SIZE):
    cursor = conn.cursor()
    col_str = ', '.join(columns)
    placeholder = ', '.join(['%s'] * len(columns))
    sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholder})"

    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cursor.executemany(sql, batch)
        conn.commit()

    cursor.close()

# ---- INSERT MADE CUPS ----
print("Creating made cups")
made_rows = []
for _ in range(MADE_CUPS_COUNT):
    made_rows.append((
        random.choice(tea_types),
        random.choice(people),
        random_time()
    ))

print("Inserting made cups")
batch_insert(conn,
             table='made_cups_of_tea',
             columns=['tea_type', 'person_id', 'made_at'],
             data=made_rows)


# ---- INSERT DRANK CUPS ----
drank_rows = []
print("Creating drank cups")
for _ in range(DRANK_CUPS_COUNT):
    drank_rows.append((
        random.choice(tea_types),
        random.choice(people),
        random_time()
    ))

print("Inserting drank cups")
batch_insert(conn,
             table='drank_cups_of_tea',
             columns=['tea_type', 'person_id', 'drank_at'],
             data=drank_rows)

conn.close()

print("Tea data successfully poured ☕")
