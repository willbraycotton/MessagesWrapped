import sqlite3
import datetime
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


ENGLISH_STOP_WORDS = set(ENGLISH_STOP_WORDS)
custom_stopwords = ENGLISH_STOP_WORDS.union(
    {"lol", "omg", "bruh", "lmao", "idk", "u", "ur","i'm","like","get","got","im","dont","cant","thats","hes","shes","ive","ya","ya'll","yall",
     "aint","wan","gonna","wanna","na","oh","hey","hi","hello","the","and","but","for","are","you","your","yours",
     "all","any","can","had","her","his","its","not","she","him","they","them","this","that","what",
     "with","was","from","there's","there", "at", "by", "an", "be", "if", "in", "is", "it", "of", "on", "or", "as",
     "my", "we", "so", "to", "too", "we're", "weve", "we'll", "he'll", "she'll", "they'll", "you'll","laughed", "emphasized","questioned","loved","i’m"
     ,"it’s","i’ll","image"
    }
    )

groupchat_name = ''
my_phone_number = ''
this_year = '2025-00-00 00:00:00'

# Connect to database
conn = sqlite3.connect("chat.db")


## METRICS
# Messages Sent by you 
# Top 10 most sent messages and Top 10 most received messages
# Top 10 most used words
# Most messages in a day
# Most reacted to messages in a groupchat 
# Top Texters in each groupchat
# Top 10 most used words in a groupchat

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
LIMIT 10;
"""
print("Top 10 most reacted to messages:")
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

print("Top texters in the groupchat:")
df = pd.read_sql_query(query, conn, params=(groupchat_name,))

print(df)

# Most Common words used in a groupchat
query = """
SELECT 
    m.text
FROM message m
JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
JOIN chat c ON cmj.chat_id = c.ROWID
WHERE c.display_name = ?
AND text is NOT NULL
"""

'''df = pd.read_sql_query(query, conn, params=(groupchat_name,))

words = {}
for message in df['text']:
    for word in message.split():
        word = word.lower().strip('.,!?;"\'()[]{}')
        if word and word not in custom_stopwords and len(word) > 1: 
            words[word] = words.get(word, 0) + 1
sorted_words = sorted(words.items(), key=lambda item: item[1], reverse=True)[:10]

print("Top 10 most used words:")
for word, count in sorted_words:
    print(f"{word}: {count}")'''


#Number of messages you sent

query = """
SELECT
    COUNT(text) as message_count
FROM message 
WHERE is_from_me = 1
AND datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') >= ?
LIMIT 10;
"""


print('Numbber of messages you sent this year:')
df = pd.read_sql_query(query, conn, params=(this_year,))
print(df)
