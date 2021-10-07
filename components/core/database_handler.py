import os
import json
import random
from dotenv.main import load_dotenv
from flask_pymongo import MongoClient
import components.utils.error_handler as error_handler

load_dotenv()
# MongoDb Details

emoji_list = ['👩🏻‍🦰', '👱🏻‍♂️', '😃', '🙂', '👩🏻‍🚀',
              '🧙🏻‍♂️', '👱🏻‍♂️', '🧐', '👻', '😺', '😋']

MONGO_DB_CREDENTIAL = os.getenv('MONGO_DB_CREDENTIAL')


client = MongoClient(MONGO_DB_CREDENTIAL)
db = client.get_database('chatbot')
records = db.intents

client2 = MongoClient(MONGO_DB_CREDENTIAL)
db2 = client2.get_database('chatbot')
# records = db.intend_response
intends_res = db2.multiintents
# print(intends_res)


# Get The Responses From  Mongodb and Analyze Them
def connect_fib(responses):
    res = records.find({'intentName': responses})
    return res

# When a user want's to modify the intent its corresponding reponses will be find in reponse_editor therefore a different fucntion is used here


def editor_connect(message):
    # print(message)
    editor_res = intends_res.find({'intentName': message})
    return editor_res


def editor_reponse(message):
    editor_res = list(editor_connect(message))
    if len(editor_res) == 0:
        editor_res = list(connect_fib('unknown_token'))
        editor_res = editor_res[0]
        # print(editor_res)
        return editor_res
    else:
        editor_res = editor_res[0]
        return editor_res

# Main Response Analyzer


def chatbot_res(responses, message):
    try:
        gen_res = list(connect_fib(responses))
        gen_res = gen_res[0]
        print (gen_res)
    except IndexError:
        error_res = error_handler.index_error()
        return error_res
    respon_fetch = gen_res['responses']
    intent = gen_res['intentName']
    select_res = random.randint(0, len(respon_fetch)-1)

    if intent == 'greeting':
        select_emoji = random.randint(0, 10)
        chat_res = {
            'reply': respon_fetch[select_res] + emoji_list[select_emoji], 'tag': 'false', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'fintract':
        chat_res = {'reply': respon_fetch,
                    'tag': 'false', 'is_multi': 'true'}
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'insurance':
        chat_res = {'reply': respon_fetch[select_res] + ' 👩‍🏭',
                    'tag': 'false', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'invoices':
        chat_res = {'reply': respon_fetch[select_res] + ' 📃',
                    'tag': 'false', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'card_details':
        chat_res = {'reply': respon_fetch[select_res] + ' 💳',
                    'tag': 'false', 'is_multi': 'false'}
        # print(chat_res)
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'contact_human_agent':
        chat_res = {'reply': respon_fetch[select_res] + ' 👨‍💻',
                    'tag': 'true', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'goodbye':
        chat_res = {'reply': respon_fetch[select_res] + ' 👋🙋‍♂️',
                    'tag': 'false', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'internet banking':
        chat_res = {'reply': respon_fetch[select_res] + ' 🏧',
                    'tag': 'false', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'thanks':
        chat_res = {'reply': respon_fetch[select_res] + ' 🙏🏻',
                    'tag': 'false', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res
# MULTIPLE
    elif intent == 'loan':
        chat_res = {'reply': "Select The Option's From Below 🏠",
                    'options': respon_fetch,
                    'tag': 'false', 'is_multi': 'true'}
        # print(chat_res)
        chat_res = json.dumps(chat_res)
        return chat_res


# MULTIPLE
    elif intent == 'payment_issue':
        chat_res = {'reply': "Select The Option's From Below" + ' 💰',
                    'options': respon_fetch,
                    'tag': 'false', 'is_multi': 'true'}
        # print(chat_res)
        chat_res = json.dumps(chat_res)
        return chat_res

    elif intent == 'query_raised':
        chat_res = {'reply': respon_fetch[select_res] + ' 🙋🏻‍♂️',
                    'tag': 'false', 'is_multi': 'false'}
        chat_res = json.dumps(chat_res)
        return chat_res

# Multiple
    else:
        # editor_reponse(message)
        editor_res = editor_reponse(message)
        editor_response = editor_res['intentName']
        editor_respon_fetch = editor_res['responses']
        select_res = random.randint(0, len(editor_respon_fetch)-1)
        # print(editor_response)

        if editor_response == message:
            chat_res = {'reply': editor_respon_fetch[select_res],
                        'tag': 'false', 'is_multi': 'false'}
            chat_res = json.dumps(chat_res)
            return chat_res

        elif editor_response == 'unknown_token':
            chat_res = {'reply': "Sorry I Can't Understand You , Please. Select The Option's From Below" + ' 🙇🏻‍♀🙇🏻‍🙇',
                        'options': editor_respon_fetch,
                        'tag': 'false', 'is_multi': 'true'}
            chat_res = json.dumps(chat_res)
            return chat_res
