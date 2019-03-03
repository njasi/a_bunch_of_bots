import json 
import requests
import time
import urllib
import string
import random
import botbase

TOKEN = "739099604:AAH-RhkNrZ_P5KO_0KXtfTGbR28QI9QXxIE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
BOT = botbase(URL)

def main():
    last_update_id = None
    while True:
        updates = BOT.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = BOT.get_last_update_id(updates) + 1
            respond(updates)
        time.sleep(0.5)

def respond(updates):
    for update in updates["result"]:
        try:
            is_statements(update)
        except Exception as e:
            pass

def is_statements(update):
    triggers = []
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]

    def addtextafter(target,text):
        things = []
        while target in text.split():
            text = text[text.find(target)+len(target):len(text)]
            things += [text]
        return things
    triggers+=addtextafter('Is',text)
    triggers+=addtextafter('is',text)
    triggers+=addtextafter('iS',text)
    triggers+=addtextafter('IS',text)
    for response in triggers:
        if len(response) != 0:
            BOT.send_message("Your face is {}! *Furiously Dabs*".format(response.strip(" ")),chat)

if __name__ == '__main__':
    main()