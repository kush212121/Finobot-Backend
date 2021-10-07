
from flask import Flask, request
import components.model.model as model
import components.core.database_handler as database
import components.utils.error_handler as error_handler

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def chat_bot():
    if request.method == 'GET':
        return 'Send The Chatbot Post Request Here'
    try:
        message = request.json
        message = ' '.join(map(str, message))
    except TypeError:
        error_res = error_handler.type_error()
        return error_res
    message = message.lower()
    response = model.model_predict(message)
    # print(response)
    result = database.chatbot_res(response, message)
    return result, 200


if __name__ == '__main__':
    app.run(debug=False)
