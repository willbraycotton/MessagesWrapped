import sqlite3
from datetime import datetime

import SVGConfig
import SQLQueries 

GROUPCHATNAME = "test"

if __name__ == "__main__":
    conn = sqlite3.connect("chat.db")

    #Overall Section
    most_messages_in_a_day = SQLQueries.get_most_messages_in_a_day(conn)

    date_string = most_messages_in_a_day['message_date'][0]
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    formatted_date = date_object.strftime("%B %d")

    replacements_overall = {
        "{{ms}}": str(SQLQueries.get_number_of_messages_sent(conn)['message_count'][0])
        , "{{amount}}": str(most_messages_in_a_day['message_count'][0])
        , "{{date}}": formatted_date
    }




    # Personal Section
    most_used_words = SQLQueries.get_your_most_common_words(conn)

    replacements_personal = {
        "{{word_1}}": most_used_words[0][0]
        , "{{word_2}}": most_used_words[1][0]
        , "{{word_3}}": most_used_words[2][0]
        , "{{word_4}}": most_used_words[3][0]
        , "{{word_5}}": most_used_words[4][0]
        , "{{chat_1}}": "test"
    }

    #GroupChat Section
    # most_used_words_groupchat = SQLQueries.get_most_common_words_in_groupchat(conn, GROUPCHATNAME)
    # most_reacted_messages = SQLQueries.get_most_reacted_messages(conn, GROUPCHATNAME)
    # replacements_GroupChat = {
    #     "{{word_1}}": most_used_words_groupchat[0][0]
    #     , "{{word_2}}": most_used_words_groupchat[1][0]
    #     , "{{word_3}}": most_used_words_groupchat[2][0]
    #     , "{{word_4}}": most_used_words_groupchat[3][0]
    #     , "{{word_5}}": most_used_words_groupchat[4][0]
    #     , "{{chat_1}}": most_reacted_messages[0][0]
    #     , "{{chat_2}}": most_reacted_messages[1][0]
    #     , "{{chat_3}}": most_reacted_messages[2][0]
    #     , "{{chat_4}}": most_reacted_messages[3][0]
    #     , "{{chat_5}}": most_reacted_messages[4][0]
    #     , "{{tt}}": str(SQLQueries.get_top_texters(conn, GROUPCHATNAME)[0][0])
    # }



    SVGConfig.update_svg("overall_original.svg", "overall.svg", replacements_overall)
    #SVGConfig.update_svg("personal_original.svg", "personal.svg", replacements_personal)
    #SVGConfig.update_svg("groupchat_original.svg", "groupchat.svg", replacements_GroupChat)

