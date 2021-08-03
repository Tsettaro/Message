# Пароль от админки – 1234

from flask import Flask as flk, request, abort, render_template
import time, json
from datetime import datetime
app = flk(__name__)

@app.route("/")
def index_page():
    return "IT'S A TEST"

db = []
db_file = "./data/db.json"
json_db = open(db_file, "rb")
data = json.load(json_db)
db = data["messages"]

def saveMessages():
    data = {
        "messages": db
    }
    json_db = open(db_file, "w")
    json.dump(data, json_db)

# 5 пункт
# @app.route("/admin_delete_everything")
# def delete():
#     data = {
#         "messages": []
#     }
#     json_db = open(db_file, "w")
#     json.dump(data, json_db)
#     db.clear()
#     return "CLEAR"

# 6 пункт
@app.route("/admin_delete_everything")
def delete():
    password = request.args["password"]
    if password != '1234':
        return 'WRONG PASSWORD!'
    else:
        data = {
            "messages": []
        }
        json_db = open(db_file, "w")
        json.dump(data, json_db)
        db.clear()
        return "CLEAR"

@app.route("/form")
def form():
    return render_template("index.html")

@app.route("/sendmessage")
def chat():
    name = request.args["name"]
    text = request.args["text"]

    if len(name) > 100 or len(name) < 3:
        return "ERROR"

    if len(text) < 1 or len(text) > 3000:
        return "ERROR"

    message = {
        "name": name,
        "text": text,
        "time": time.time()
    }
    db.append(message)
    saveMessages()
    return "OK"



def print_messages(messages):
    for message in messages:
        name = message["name"]
        text = message["text"]
        message_time = message["time"]
        time_pretty = datetime.fromtimestamp(message_time)

        print(f"[{name}] / {time_pretty}")
        print(text)
        print()



@app.route("/messages")
def get_messages():
    after_timestamp = float(request.args["after_timestamp"])
    result = []
    for message in db:
        if message["time"] > after_timestamp:
            result.append(message)

    return {"messages" : result}

# 2,3 и 4 пункты ТЗ
@app.route("/status")
def status():
    return "Добро пожаловать на сервер Антона версии 1.0. Текущее время – " + str(datetime.now().time()) + '. Количество сообщений в базе данных – ' + str(len(db)) + '.'


app.run()
