import sqlite3

import SVGConfig
import SQLQueries 

GROUPCHATNAME = "test"

if __name__ == "__main__":
    conn = sqlite3.connect("chat.db")

    #Overall Section

    replacements_personal = {
        "{{ms}}": str(SQLQueries.get_number_of_messages_sent(conn)[0][0])
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
    most_used_words_groupchat = SQLQueries.get_most_common_words_in_groupchat(conn, GROUPCHATNAME)

    replacements_GroupChat = {
        "{{word_1}}": most_used_words_groupchat[0][0]
        , "{{word_2}}": most_used_words_groupchat[1][0]
        , "{{word_3}}": most_used_words_groupchat[2][0]
        , "{{word_4}}": most_used_words_groupchat[3][0]
        , "{{word_5}}": most_used_words_groupchat[4][0]
        , "{{chat_1}}": "test"
    }



    SVGConfig.update_svg("overall_original.svg", "overall.svg", replacements_personal)
    SVGConfig.update_svg("personal_original.svg", "personal.svg", replacements_personal)
    SVGConfig.update_svg("groupchat_original.svg", "groupchat.svg", replacements_GroupChat)

