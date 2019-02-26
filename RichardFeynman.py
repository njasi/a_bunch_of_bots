import json
import requests
import time
import urllib
import string
import random
import wolframalpha
import wikipedia
import warnings
import os

reader = open('ftoken.txt','r')
TOKEN = reader.readline().strip()
reader = open('wolfram.txt','r')
app_id = reader.readline().strip()
reader.close()
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
client = wolframalpha.Client(app_id)

TRIGGER_STICKERS = [
    ('CAADAwADxAAD3zLTBALNnvfeN-vcAg',['no u']),
    ('StickerId2Here',['list','of','possible','responses2'])
]

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

def respond(updates):
    for update in updates["result"]:
        try:
            respond_smart(update)
            os.remove('out.jpg')
        except Exception as e:
            throw(e)
            return

def respond_smart(update):
    text = update["message"]["text"]
    if not "Feynman: " in text:
        return
    text = text[9:]
    chat = update["message"]["chat"]["id"]
    r = search(text)
    print(text)
    if r[0] == None:  # unable to find anything
        send_message('That\'s a dumb question.', chat)
        return
    # send_message(r[0], chat)
    if r[1] != None:
        print(r[0])
        print()
        print(r[1])
        f = open('out.jpg','wb')
        f.write(urllib.request.urlopen(r[1]).read())
        f.close()
        url = URL + "/sendPhoto";
        files = {'photo': open('out.jpg', 'rb')}
        data = {'chat_id' : chat}
        r = requests.post(url, files=files, data=data)
        os.remove('out.jpg')

def search(text=''):
  res = client.query(text)
  if res['@success'] == 'false':
     return search_wiki(text), primaryImage(text)
  else:
    result = ''
    pod0 = res['pod'][0]
    pod1 = res['pod'][1]
    question = resolveListOrDict(pod0['subpod'])
    question = removeBrackets(question)
    if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
      result = resolveListOrDict(pod1['subpod'])
      return result, primaryImage(question)
    else:
      return search_wiki(question), primaryImage(question)

def search_wiki(query):
    result = wikipedia.search(query)
    if not result:
        return
    try:
        page = wikipedia.page(query)
        answer = wikipedia.summary(query, sentences=2)
        if '==' in answer:
            answer = wikipedia.summary(query, sentences=1)
    except wikipedia.DisambiguationError as err:
        page = wikipedia.page(err.options[0])
        answer = wikipedia.summary(err.options[0], sentences=2)
        if '==' in answer:
            answer = wikipedia.summary(query, sentences=1)
    except wikipedia.PageError as err:
        answer = None
    
    return answer

def removeBrackets(variable):
    return variable.split('(')[0]

def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']

def primaryImage(title=''):
    url = 'http://en.wikipedia.org/w/api.php'
    data = {'action':'query', 'prop':'pageimages','format':'json','piprop':'original','titles':title}
    try:
        res = requests.get(url, params=data)
        key = list(res.json()['query']['pages'].keys())[0]
        imageUrl = res.json()['query']['pages'][key]['original']['source']
        return imageUrl
    except Exception as err:
        return None

if __name__ == '__main__':
    main()
