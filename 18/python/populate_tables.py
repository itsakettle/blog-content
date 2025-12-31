# LLM mostly

import os
import random
from datetime import datetime, timedelta
import mysql.connector

PEOPLE_COUNT = 1000
DAYS_BACK = 30
MADE_CUPS_COUNT = 500000
DRANK_CUPS_COUNT = 800000

# ---- DB CONFIG ----
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# ---- DATA ----
tea_types = ["black", "green", "herbal", "oolong", "chai", "earl_grey"]
people = list(range(1, PEOPLE_COUNT+1))  
now = datetime.now()

def random_time(days_back=DAYS_BACK):
    return now - timedelta(
        days=random.randint(0, days_back),
        minutes=random.randint(0, 1440)
    )

# ---- INSERT MADE CUPS ----
made_rows = []
for _ in range(MADE_CUPS_COUNT):
    made_rows.append((
        random.choice(tea_types),
        random.choice(people),
        random_time()
    ))

cursor.executemany(
    """
    INSERT INTO made_cups_of_tea (tea_type, person_id, made_at)
    VALUES (%s, %s, %s)
    """,
    made_rows
)

# ---- INSERT DRANK CUPS ----
drank_rows = []
for _ in range(DRANK_CUPS_COUNT):
    drank_rows.append((
        random.choice(tea_types),
        random.choice(people),
        random_time()
    ))

cursor.executemany(
    """
    INSERT INTO drank_cups_of_tea (tea_type, person_id, drank_at)
    VALUES (%s, %s, %s)
    """,
    drank_rows
)

conn.commit()
cursor.close()
conn.close()

print("Tea data successfully poured ☕")
