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
     ,"it’s","i’ll","image", "None", " "
    }
    )

groupchat_name = ''
my_phone_number = ''
this_year = '2025-00-00 00:00:00'

# Connect to database


# Helper function to get sorted words from a dataframe
def get_sorted_words(df, top_n=10):
    words = {}
    for message in df['text']:
        for word in message.split():
            word = word.lower().strip('.,!?;"\'()[]{}')
            if word and word not in custom_stopwords and len(word) > 1: 
                words[word] = words.get(word, 0) + 1
    sorted_words = sorted(words.items(), key=lambda item: item[1], reverse=True)[:top_n]
    return sorted_words

# Returns Top 10 most reacted messages in a specific group chat
def get_most_reacted_messages(conn, groupchat_name):

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
    AND original.text IS NOT NULL
    AND LENGTH(original.text) > 1
    GROUP BY original.guid
    ORDER BY reaction_count DESC
    LIMIT 10;
    """

    df = pd.read_sql_query(query, conn, params=(groupchat_name,))
    return df

# Who sent the most messages in a groupchat
def get_top_texters(conn, groupchat_name):

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

    df = pd.read_sql_query(query, conn, params=(groupchat_name,))
    return df



# Your most common words used
def get_your_most_common_words(conn):

    query = """
    SELECT 
        m.text
    FROM message m
    WHERE m.is_from_me = 1
    AND m.text IS NOT NULL
    AND LENGTH(m.text) > 1
    """

    df = pd.read_sql_query(query, conn)
    return get_sorted_words(df, top_n=10)


# Most Common words used in a groupchat
def get_most_common_words_in_groupchat(conn, groupchat_name):

    query = """
    SELECT 
        m.text
    FROM message m
    JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
    JOIN chat c ON cmj.chat_id = c.ROWID
    WHERE c.display_name = ?
    AND text is NOT NULL
    """

    df = pd.read_sql_query(query, conn, params=(groupchat_name,))
    return get_sorted_words(df, top_n=20)

#Number of messages you sent
def get_number_of_messages_sent(conn):

    query = """
    SELECT
        COUNT(text) as message_count
    FROM message
    WHERE is_from_me = 1
    AND datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') >= ?
    LIMIT 10;
    """
    
    df = pd.read_sql_query(query, conn, params=(this_year,))
    return df

#Number of messages you recieved 
def get_number_of_messages_received(conn):

    query = """
    SELECT 
        COUNT(text) as message_count
    FROM message
    WHERE is_from_me = 0
    AND datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') >= ?
    LIMIT 10;"""

    df = pd.read_sql_query(query, conn, params=(this_year,))
    return df

# Most messages in a day
def get_most_messages_in_a_day(conn):

    query = """
    SELECT 
        COUNT(text) AS message_count
        , DATE(datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime')) AS message_date
    FROM message
    WHERE is_from_me = 1
    AND datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') >= ?
    GROUP BY message_date
    ORDER BY message_count DESC
    LIMIT 10;
    """

    df = pd.read_sql_query(query, conn, params=(this_year,))
    return df




if __name__ == "__main__":
    
    conn = sqlite3.connect("chat.db")

    print("Most Reacted Messages:")
    print(get_most_reacted_messages(conn, groupchat_name))
    print("\nTop Texters:")
    print(get_top_texters(conn, groupchat_name))
    print("\nYour Most Common Words:")
    print(get_your_most_common_words(conn))
    print("\nMost Common Words in Groupchat:")
    print(get_most_common_words_in_groupchat(conn, groupchat_name))
    print("\nNumber of Messages Sent This Year:")
    print(get_number_of_messages_sent(conn))
    print("\nNumber of Messages Received This Year:")
    print(get_number_of_messages_received(conn))
    print("\nMost Messages Sent in a Day This Year:")
    print(get_most_messages_in_a_day(conn))

    conn.close()