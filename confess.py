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
    keys = json.dumps({'inline_keyboard': [[{'text' : 'Instant', 'callback_data':3},{'text' : 'Cancel', 'callback_data':4}],[{'text' : '10 - 15 mins', 'callback_data':0},{'text' : '30 - 45 mins', 'callback_data':1},{'text' : '1 - 2 hrs', 'callback_data':2}]]})
    keys = urllib.parse.quote_plus(keys)
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}&reply_to_message_id={}".format(text,chat_id,keys,message_id)
    get_url(url)

def url_message_from_data(data):
    type = data['type']
    number = get_confession_number() + 1
    update_confession_number(number)
    if(type == 'text'):
        text = urllib.parse.quote_plus('Confession #{}:\n'.format(number) + data['text'])
        return URL + 'sendMessage?text={}'.format(text)

    elif(type == 'sticker'):
    update_confession_number(number - 1)
        return URL + 'sendSticker?sticker={}'.format(data['file_id'])

    elif(type == 'photo'):
        caption = 'Confession #{}:\n'.format(number) + data['caption']
        caption = urllib.parse.quote_plus(caption)
        return URL + 'sendPhoto?photo={}&caption={}'.format(data['file_id'],caption)

    elif(type == 'audio'):
        caption = 'Confession #{}:\n'.format(number) + data['caption']
        caption = urllib.parse.quote_plus(caption)
        return URL + 'sendAudio?audio={}&caption={}'.format(data['file_id'],caption)

    elif(type == 'document'):
        caption = 'Confession #{}:\n'.format(number) + data['caption']
        caption = urllib.parse.quote_plus(caption)
        return URL + 'sendDocument?document={}&caption={}'.format(data['file_id'],caption)

    elif(type == 'video'):
        caption = 'Confession #{}:\n'.format(number) + data['caption']
        caption = urllib.parse.quote_plus(caption)
        return URL + 'sendVideo?video={}&caption={}'.format(data['file_id'],caption)

    elif(type == 'animation'):
        caption = 'Confession #{}:\n'.format(number) + data['caption']
        caption = urllib.parse.quote_plus(caption)
        return URL + 'sendAnimation?animation={}&caption={}'.format(data['file_id'],caption)

    elif(type == 'voice'):
        caption = 'Confession #{}:\n'.format(number) + data['caption']
        caption = urllib.parse.quote_plus(caption)
        return URL + 'sendVoice?voice={}&caption={}'.format(data['file_id'],caption)
    
    

def data_from_update(update):
    data = {}
    if not should_message_be_sent(update):
        return None
    try: # normal text message
        text = update['message']['text']
        data['type'] = 'text'
        data['text'] = text
        return data
    except Exception:
        pass
        
    try: # stickers 
        file_id = update['message']['sticker']['file_id']
        data['type'] = 'sticker'
        data['file_id'] = file_id
        return data
    except Exception:
        pass

    try: # captions for documents and such
        caption = update['message']['caption']
    except Exception:
        caption = ''
    
    data['caption'] = caption # all of the types after this have captions

    try: # photo
        file_id = update['message']['caption'][len(sizes)-1]['file_id']
        data['type'] = 'photo'
        data['file_id'] = file_id
        return data
    except Exception:
        pass
        
    try: # audio
        file_id = update['message']['audio']['file_id']
        data['type'] = 'audio'
        data['file_id'] = file_id
        return data
    except Exception:
        pass
        
    try: # document
        file_id = update['message']['document']['file_id']
        data['type'] = 'document'
        data['file_id'] = file_id
        return data
    except Exception:
        pass

    try: # video
        file_id = update['message']['video']['file_id']
        data['type'] = 'video'
        data['file_id'] = file_id
        return data
    except Exception:
        pass

    try: # animation
        file_id = update['message']['animation']['file_id']
        data['type'] = 'animation'
        data['file_id'] = file_id
        return data
    except Exception:
        pass

    try: # voice
        file_id = update['message']['voice']['file_id']
        data['type'] = 'voice'
        data['file_id'] = file_id
        return data
    except Exception:
        pass

    return None # to detect that a message that is not sendable was recived
     
def update_confession_number(number):
    num = open('num.txt','w+')
    num.write(str(number))
    num.close()

def get_confession_number():
    num = open('num.txt','r')
    hold = int(num.readline())
    num.close()
    return hold

     
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

def add_to_buffer(updates):
    global waiting
    for update in updates:
        try:
            if is_button_response(update):
                check_waiting(update['callback_query'])
                raise Exception('added_message')
            data = {}
            data['data'] = data_from_update(update)

            if data['data'] is not None:
                data['id'] = update['message']['message_id']  #only stored temporarliy while the bot waits for a time option
                data['from'] = update['message']['from']['id']
                data['data'] = json.dumps(data['data'])
                send_time_options(update['message']['from']['id'],update['message']['message_id'])
                waiting += [data]
        except Exception as e:
            if not str(e) == 'added_message':
                raise(e)
                send_error(e,update)
                returner = False
            
def check_waiting(query):
    global waiting
    for message in waiting:
        if query['from']['id'] == message['from'] and message['id'] == query['message']['reply_to_message']['message_id']:
            waiting.remove(message)
            messages = open('messages.txt','a')
            data = {}
            if(query['data'] == '0'):
                data['send_time'] = int(random() * 300) + 600   # 10 - 15 min
            elif query['data'] == '1':
                data['send_time'] = int(random() * 900) + 1800  # 30 - 45 min
            elif query['data'] == '2':
                data['send_time'] = int(random() * 3600) + 3600 # 1 - 2 hrs
            elif query['data'] == '3':
                data['send_time'] = 0                           # Instant
            elif query['data'] == '4':
                send_message('Okay, your confession was canceled.', message['from'])
                return   
            data['data'] = message['data']
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
    pass
    # if str(e) != 'message':
        # send_message('Dabney Confessions was unable to process your message.\nError message: ' + str(e),update['message']['from']['id'])
        # send_message('/bigoofletjaSINskiknow', update['message']['from']['id'])

def send_data(data):
    for chat in chats:
        try:
            if not data['data'] is None:
                get_url(url_message_from_data(json.loads(data['data'])) + "&chat_id={}".format(chat))
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
