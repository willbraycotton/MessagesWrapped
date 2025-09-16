import sqlite3
import pandas as pd

groupchat_name = ''
# Connect to database
conn = sqlite3.connect("chat.db")


# Returns Top 10 most reacted messages in a specific group chat
query = """
SELECT 
    original.text AS original_message,
    COUNT(m.associated_message_guid) AS reaction_count,
    datetime(original.date/1000000000 + 978307200, 'unixepoch', 'localtime') AS original_message_date
    , c.display_name 
FROM chat c
JOIN chat_message_join cmj ON c.ROWID = cmj.chat_id
JOIN message m ON cmj.message_id = m.ROWID
LEFT JOIN message original ON SUBSTR(m.associated_message_guid, 5) = original.guid -- Match trimmed GUID
WHERE c.display_name = ?
AND m.associated_message_guid IS NOT NULL
GROUP BY original.guid
ORDER BY reaction_count DESC
LIMIT 15;
"""

df = pd.read_sql_query(query, conn, params=(groupchat_name,))

print(df)

# Who sent the most messages in a groupchat
query = """
SELECT 
    CASE 
        WHEN m.handle_id IS NULL OR m.handle_id = 0 THEN 'You' 
        ELSE h.id 
    END AS sender,
    COUNT(m.text) AS message_count,
    c.display_name
FROM chat c
JOIN chat_message_join cmj ON c.ROWID = cmj.chat_id
JOIN message m ON cmj.message_id = m.ROWID
LEFT JOIN handle h ON m.handle_id = h.ROWID
WHERE c.display_name = ?
GROUP BY sender
ORDER BY message_count DESC;
"""

# Most Common words used in a groupchat







df = pd.read_sql_query(query, conn, params=(groupchat_name,))

print(df)