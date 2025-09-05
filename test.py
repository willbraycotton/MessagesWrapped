import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("chat.db")

# Read a table into pandas
'''tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)

print("Tables in the database:")
print(tables)'''

df = pd.read_sql_query("SELECT * FROM message LIMIT 10;", conn)

print(df.head())