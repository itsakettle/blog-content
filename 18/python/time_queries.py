# LLM mostly

import os
import mysql.connector
import time

# --- DB CONFIG ---
conn = mysql.connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"]
)

cursor = conn.cursor()

# --- QUERIES ---
queries = [
    ("Count green tea made",  "SELECT COUNT(*) FROM made_cups_of_tea WHERE tea_type = 'green';"),
    ("Count black tea drank", "SELECT COUNT(*) FROM drank_cups_of_tea WHERE tea_type = 'black';")
]

results = []

# --- RUN QUERIES ---
for description, query in queries:
    print(f"Running query: {description} ...")
    start = time.perf_counter()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    end = time.perf_counter()
    elapsed = end - start
    results.append((description, result, elapsed))
    print(f"Query finished: {description}, result={result}, time={elapsed:.6f} seconds\n")

# --- FINAL REPORT ---
print("=== QUERY TIMING SUMMARY ===")
for description, result, elapsed in results:
    print(f"{description}: result={result}, time={elapsed:.3f} seconds")

cursor.close()
conn.close()
