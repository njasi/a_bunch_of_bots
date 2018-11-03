import json 
import requests
import time
import urllib
import string
import random

TOKEN = "739099604:AAH-RhkNrZ_P5KO_0KXtfTGbR28QI9QXxIE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#
# Code dealing with sending and reciving messages
#

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            respond(updates)
        time.sleep(0.5)

#
# Does all of the responding
#

def respond(updates):
    for update in updates["result"]:
        try:
            is_statements(update)
        except Exception as e:
            pass

def is_statements(update):
    triggers=[]
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]

    def addtextafter(target,text):
        things = []
        while target in text.split():
            text = text[text.find(target)+len(target):len(text)]
            things += [text]
        return things
    # no '
    triggers+=addtextafter('Is',text)
    triggers+=addtextafter('is',text)
    triggers+=addtextafter('iS',text)
    triggers+=addtextafter('IS',text)
    for response in triggers:
        if len(response) != 0:
            send_message("Your face is {}! *Furiously Dabs*".format(response.strip(" ")),chat)
    
def respond_trigger_words(update,tokenize,triggers,responses):
    text = strip_punct(update["message"]["text"])
    if tokenize:
        text=text.split()
    chat = update["message"]["chat"]["id"]
    b = True
    for ands in triggers:
        a = False
        for ors in ands:
            if tokenize:
                a = a or ors in text
            else:
                a = a or text.find(ors)!=-1
        b = b and a
    if b:
        send_message(responses[random.randint(0,len(responses)-1)],chat)
        raise Exception('a response was triggered')
            
def respond_trigger_words_user(update,tokenize,triggers,responses,userid):
    text = strip_punct(update["message"]["text"])
    if tokenize:
        text=text.split()
    chat = update["message"]["chat"]["id"]
    b = True
    for ands in triggers:
        a = False
        for ors in ands:
            if tokenize:
                a = a or ors in text
            else:
                a = a or text.find(ors)!=-1
        b = b and a
    if b:
        try:
            send_message(responses[userid.index(update["message"]["from"]["id"])+1],chat)
        except Exception as e:
            send_message(responses[0],chat)
        raise Exception('a response was triggered')
        
def strip_punct(text):
    exclude=set(string.punctuation)
    exclude.add('’')

    return (''.join(ch for ch in text if ch not in exclude)).lower()


if __name__ == '__main__':
    main()