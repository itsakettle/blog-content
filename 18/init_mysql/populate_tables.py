# LLM

import random
from datetime import datetime, timedelta
import mysql.connector

# ---- DB CONFIG ----
conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="your_db"
)
cursor = conn.cursor()

# ---- DATA ----
tea_types = ["black", "green", "herbal", "oolong", "chai", "earl_grey"]
people = list(range(1, 21))  # 20 people
now = datetime.now()

def random_time(days_back=30):
    return now - timedelta(
        days=random.randint(0, days_back),
        minutes=random.randint(0, 1440)
    )

# ---- INSERT MADE CUPS ----
made_rows = []
for _ in range(500):
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
for _ in range(800):
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
