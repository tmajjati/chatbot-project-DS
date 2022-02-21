from flask import Flask, jsonify, request
import requests 

from config import *
from utils import *
from db import DBHelper

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s,%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


app = Flask("TelegramBot")
db = DBHelper()
db.setup()
cnn = db.conn
cur=cnn.cursor()
codes = [2,3,11,13,42,69,666]
for i, e in enumerate(codes) :
    cur.execute("insert into track_table values (?, ?)",(i, e))
cur.close()


@app.route("/",methods=["POST", "GET"])
def index():

    if request.method == "POST":
       
        message = request.get_json()
        chat_id, msg_txt = parse_message(message)

        f=open('track.json','r')
        track=json.load(f)
        resp_msg = message_response(msg_txt)
        logger.debug(f"message recived : {msg_txt}, response : {resp_msg}")
        if track['track']:
            code = message["message"]["text"]
            mask = db.check(code)
            #cnn.close()
            logger.debug("checking the database")
            if mask[0]==1:
                resp_msg = "your code is on the system! try another code? /track . /menu to return to main menu or /end to end conversation "
                send_message(chat_id, resp_msg)
                logger.debug(f"message sent : {resp_msg}")

            else :
                resp_msg = "this code does not exist in the system! try another code : /track . /menu to return to main menu or /end to end conversation " 
                send_message(chat_id, resp_msg)
            track["track"] = False
            f=open('track.json','w')
            json.dump(track, f)


        elif msg_txt == '/track':
            code = message["message"]["text"]
            send_message(chat_id, resp_msg)
            track["track"] = True
            f=open('track.json','w')
            json.dump(track, f)

        else :
            send_message(chat_id, resp_msg)
            logger.debug(f"message sent : {resp_msg}")
        

        return jsonify({'job_done' : 'ok','status' : 200})

    else:
        return jsonify({"status" : "idle"})
    


@app.route("/setwebhook/")
def setwebhook():
    resp = requests.get(f"{API_URL}/bot{TOKEN}/setWebhook?url={URL}")

  
    if resp.status_code == 200:
        return jsonify({'status' : 'ok'})
    else:
        return jsonify({'status' : 'error'})


if __name__ == '__main__':
    app.run(debug=True)