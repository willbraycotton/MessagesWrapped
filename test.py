import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("chat.db")

# Handle Table contains all phone numbers
# Message Table contains all messages


# Read a table into pandas
'''tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)

print("Tables in the database:")
print(tables)'''

df = pd.read_sql_query("SELECT * FROM handle LIMIT 10;", conn)

print(df.columns)
print(df.head())


# Most recent Texts
'''query = """
SELECT 
    text, date, -- Convert Unix timestamp (seconds since 2001-01-01) to Unix epoch (1970)
    datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') as formatted_date
FROM message
ORDER BY date DESC
LIMIT 15;
"""'''


query = """
SELECT 
    text, date, -- Convert Unix timestamp (seconds since 2001-01-01) to Unix epoch (1970)
    datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') as formatted_date
FROM message
ORDER BY date DESC
LIMIT 15;
"""

df = pd.read_sql_query(query, conn)

print("\nMost reacted to messages:")
print(df)