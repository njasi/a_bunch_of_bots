import json 
import requests
import time
import urllib
import string
import random
import smtplib
import sys

from random import random

###########################################
#TODO: remove token when upload to github #
###########################################

reader = open('token.txt','r')
TOKEN = reader.readline()
reader.close()
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def load_chats():
    holder = []
    reader = open('chats.txt')
    for line in reader.readlines():
        holder += [int(line.strip())]
    reader.close()
    return holder

chats = load_chats()

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

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def should_message_be_sent(update):
    try:
        return ((update['message']['chat']['id'] is not None) and update['message']['chat']['id'] == update['message']['from']['id']) and update['message']['text'] != '/start'
    except:
        return True

def url_message_from_update(data):
    if not should_message_be_sent(data):
        return None
    caption = ''
    try:
        caption = data['message']['caption']
    except Exception as e:
        pass
    caption = urllib.parse.quote_plus(caption)
    try:
        text = data['message']['text']
        text = urllib.parse.quote_plus(text)
        return URL + 'sendMessage?text={}'.format(text)
    except Exception as e:
        pass
    try:
        sizes = data['message']['photo']
        file_id = sizes[len(sizes)-1]['file_id']
        return URL + 'sendPhoto?photo={}&caption={}'.format(file_id,caption)
    except Exception as e:
        pass
    try:
        file_id = data['message']['audio']['file_id']
        return URL + 'sendAudio?audio={}&caption={}'.format(file_id,caption)
    except Exception as e:
        pass
    try:
        file_id = data['message']['document']['file_id']
        return URL + 'sendDocument?document={}&caption={}'.format(file_id,caption)
    except Exception as e:
        pass
    try:
        file_id = data['message']['video']['file_id']
        return URL + 'sendVideo?video={}&caption={}'.format(file_id,caption)
    except Exception as e:
        pass
    try:
        file_id = data['message']['animation']['file_id']
        return URL + 'sendAnimation?animation={}&caption={}'.format(file_id,caption)
    except Exception as e:
        pass
    try:
        file_id = data['message']['voice']['file_id']
        return URL + 'sendVoice?voice={}&caption={}'.format(file_id,caption)
    except Exception as e:
        pass
    try:
        file_id = data['message']['sticker']['file_id']
        return URL + 'sendSticker?sticker={}'.format(file_id)
    except Exception as e:
        pass
     
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            add_to_buffer(updates['result'])
            respond()
        time.sleep(0.5)

# for me to remotely stop it if i need to
def lockdown(updates):
    for update in updates:
        try:
            if update['message']['text'] == '!!!LOCKDOWN!!!' and update['message']['from']['id'] == 569239019:
                quit()
        except Exception as e:
            pass

def add_to_buffer(updates):
    for update in updates: 
        try:
            data = {}
            data['send_time'] = int(time.time() + random() * 360 + 600)
            data['url'] = url_message_from_update(update)

            if data['url'] is not None:
                messages = open('messages.txt','a')
                messages.write(json.dumps(data) + '\n')
                messages.close()
        except Exception as e:
            send_error(e,update)
            returner = False
            
    
def send_error(e,update):
    send_message('Dabney Confessions was unable to process your message.\nError message: ' + str(e),update['message']['from']['id'])
    send_message('/bigoofletjaSINskiknow', update['message']['from']['id'])

def send_data(data):
    for chat in chats:
        try:
            if not data['url'] is None:
                get_url(data['url'] + "&chat_id={}".format(chat))
        except Exception as e:
            print(str(e))

def respond():
    file = open('messages.txt','r')
    to_remove = []
    while True:
        line = file.readline()
        line = line.rstrip()
        if not line: break
        data = json.loads(line)
        if int(time.time()) > data['send_time']:
            send_data(data)
            to_remove += [data]
    file.close()
    file = open('messages.txt','r')
    old_lines = file.readlines()
    file.close()
    file = open('messages.txt','w')
    for line in old_lines:
        if not json.loads(line.strip()) in to_remove:
            file.write(line)

if __name__ == '__main__':
    main()
