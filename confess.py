import json 
import requests
import time
import urllib
import string
import smtplib

from random import random

# Sorry

reader = open('token.txt','r')
TOKEN = reader.readline()
reader.close()
waiting = []
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
confession_number = 276 # !!!!! Change this if the script has to restart !!!!! (put it at the number you want)
confession_messages = ['Thank you for your sins.','...','[insert appropriate response here]']
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

def send_time_options(chat_id,message_id):
    text = urllib.parse.quote_plus('How long from now would you like your message to be sent?')
    keys = json.dumps({'inline_keyboard': [[{'text' : '10 - 15 mins', 'callback_data':0},{'text' : '30 - 45 mins', 'callback_data':1},{'text' : '1 - 2 hrs', 'callback_data':2}]]})
    keys = urllib.parse.quote_plus(keys)
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}&reply_to_message_id={}".format(text,chat_id,keys,message_id)
    get_url(url)

def delete_message(chat_id,message_id):
    url = URL + 'deleteMessage?chat_id={}&message_id={}'.format(chat_id,message_id)
    get_url(url)

def url_message_from_update(data):
    global confession_number
    if not should_message_be_sent(data):
        return None
    caption = ''
    try:
        caption = data['message']['caption']
    except Exception as e:
        pass
    caption = 'Confession #{}:\n'.format(confession_number) + caption
    confession_number += 1
    caption = urllib.parse.quote_plus(caption)
    try:
        text = data['message']['text']
        text = 'Confession #{}:\n'.format(confession_number-1) + text
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
        confession_number -= 1
        return URL + 'sendSticker?sticker={}'.format(file_id)
    except Exception as e:
        pass
    confession_number -= 1
     
def main():
    global waiting
    waiting = []
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            add_to_buffer(updates['result'])
            respond()
        time.sleep(0.5)

# for me to remotely stop it if i need to
'''
def lockdown(updates):
    for update in updates:
        try:
            if update['message']['text'] == '!!!LOCKDOWN!!!' and update['message']['from']['id'] == 569239019:
                quit()
        except Exception as e:
            pass
'''

def add_to_buffer(updates):
    global waiting
    for update in updates:
        try:
            if is_button_response(update):
                check_waiting(update['callback_query'])
                raise Exception('added_message')
            data = {}
            data['url'] = url_message_from_update(update)
            data['id'] = update['message']['message_id']  #only stored temporarliy while the bot waits for a time option
            data['from'] = update['message']['from']['id']

            if data['url'] is not None:
                send_time_options(update['message']['from']['id'],update['message']['message_id'])
                waiting += [data]
        except Exception as e:
            if not str(e) == 'added_message':
                send_error(e,update)
                returner = False
            
def check_waiting(query):
    global waiting
    for message in waiting:
        if query['from']['id'] == message['from'] and message['id'] == query['message']['reply_to_message']['message_id']:
            waiting.remove(message)
            messages = open('messages.txt','a')
            data = {}
            data['url'] = message['url']
            if(query['data'] == '0'):
                data['send_time'] = int(random() * 300) + 600   # 10 - 15 min
            elif query['data'] == '1':
                data['send_time'] = int(random() * 900) + 1800  # 30 - 45 min
            elif query['data'] == '2':
                data['send_time'] = int(random() * 3600) + 3600 # 1 - 2 hrs
            data['send_time'] += int(time.time())
            messages.write(json.dumps(data) + '\n') 
            messages.close()
            send_message(confession_messages[int(random() * len(confession_messages))],message['from'])

def is_button_response(update):
    try:
        update['callback_query']
    except Exception:
        return False
    return True
    
def send_error(e,update):
    send_message('Dabney Confessions was unable to process your message.\nError message: ' + str(e),update['message']['from']['id'])
    send_message('/bigoofletjaSINskiknow', update['message']['from']['id'])

def send_data(data):
    for chat in chats:
        try:
            if not data['url'] is None:
                get_url(data['url'] + "&chat_id={}".format(chat))
        except Exception as e:
            pass

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
