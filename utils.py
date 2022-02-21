"""
this file contains a set of helper functions that will will be called 
insisde functions of app.py (main app file)

"""

import requests
import json
from config import *

def parse_message(message):
    """
    a function that parses message objects and return correspondent info : text message and chat id 
    """
    msg_text = message["message"]["text"]
    #sender_name = resp["message"]["from"]["first_name"]
    chat_id = message["message"]["chat"]["id"]

    return chat_id, msg_text

def message_response(msg_txt):
    """
    a helper function that returns correspondent message for a user command
    """
    commands = {"/start":"Hello! I am CHATBOT-DS-42, I am here to help \n/track : if you want to track your code \n/end to end conversation.",
    "/track" : "please type your code, or  /menu to return to main menu", 
    "/menu" : "/track : to track your code \n /end : to end conversation.", 
    "/end" : "good bye!"}
    if msg_txt in commands.keys():
        return commands[msg_txt]
    else:
        return "did you mean track my code?\n /track : to track the code.\n /end : to end conversation."

def send_message(chat_id, msg):
    """
    a function that sends messages to user through telegram api using a post request
    """
    url = "{}/bot{}/sendMessage".format(API_URL,TOKEN)
    payload = {
        "text":msg,
        "chat_id":chat_id
        }
    
    resp = requests.post(url, json=payload)
    return resp

def write_json(data, filename="response.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=True)

