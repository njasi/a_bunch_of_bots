import json 
import requests
import time
import urllib
import string
import random
TOKEN = "607870320:AAHM64JdBsWIZhtfYpw-o8kNjGnwI-UC7dw"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

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
            for response in TRIGGER_STICKERS:
                respond_trigger_stickers(update, response[1], stickerid = response[0])
            #respond_trigger_words_user(update,True,[["heck","anus","arse","arsehole","ass","bitch","inappropriate","inappropriate","inappropriate","cocksucking","coochie","coddamnit","coochy","cooter","cum","cumbubble","cumdumpster","cummer","cumming","cumshot","cumslut","cuntface","cunthole","cuntlick","cuntlicker","inappropriate","dickbag","dickbeaters","dickface","dickfuck","dickhead","dickhole","dickjuice","dickmilk","dickslap","dickwad","dickweasel","dickweed","dickwod","dildo","dink","inappropriate","inappropriate","inappropriate","inappropriate","inappropriate","hayward","fag","freaking","faggot","fuck","fuckersucker","fuckface","fuckhead","fuckhole","fuckin","fucking","fuckme","fucknut","fucknutt","fuckoff","fuckstick","fucktard","fuckup","fuckwad","fuckwit","fuckwitt","fudgepacker","fuk","gangbang","gangbanged","goddamn","blasphemy","inappropriate","gooch","gook","gringo","guido","handjob","hardcoresex","heeb","hell","ho","hoe","homo","homodumbshit","honkey","horniest","horny","hotsex","humping","jackass","jap","jigaboo","jism","jiz","jizm","jizz","jungle bunny","junglebunny","kike","kock","kondum","kooch","kootch","kum","kumer","kummer","kumming","kums","kunilingus","kunt","kyke","lezzie","lust","lusting","mcfagget","mick","minge","mothafuck","mothafucka","mothafuckin","mothafucking","mothafucks","motherfuck","motherfucked","motherfucker","munging","nut","nutt","negro","nigga","nigger","niglet","nut sack","nutsack","orgasim","orgasm","paki","panooch","pecker","peckerhead","penis","penisfucker","penispuffer","phonesex","phuk","phuked","phuking","phukked","phukking","phuks","phuq","pis","pises","pisin","pising","pisof","piss","pissed","pisser","pisses","pissflaps","pissin","pissing","pissoff","polesmoker","pollock","poon","poonani","poonany","poontang","porch monkey","porchmonkey","porn","porno","pornography","pornos","prick","punanny","punta","pusies","pussy","shitass","shitbag","shitbagger","shitbrain","shitbreath","shitcunt","shitdick","shited","shitface","shitfaced","inappropriate","inappropriate","shitted","shitter","shittiest","shitting","shitty","shity","shiz","shiznit","skank","sex","skeet","skullfuck","slut","slutbag","sluts","smeg","smut","snatch","spic","spick","splooge","spunk","tard","testicle","thundercunt","tit","tits","titfuck","tittyfuck","twat","twatlips","twatwaffle","unclefucker","va-j-j","vag","vagina","vjayjay","wank","wetback","whore","whorebag","whoreface","jew","jews","anal","anus","arse","ass","ass fuck","ass hole","assfucker","asshole","assshole","bastard","bitch","black cock","bloody hell","boong","cock","cockfucker","cocksuck","cocksucker","coon","coonnass","crap","cunt","cyberfuck","damn","darn","dick","dirty","douche","dummy","erect","erection","erotic","escort","fag","faggot","fuck","Fuck off","fuck you","fuckass","fuckhole","god damn","gook","hardcore","hardcore","homoerotic","hore","lesbian","lesbians","mother fucker","motherfuck","motherfucker","negro","nigger","orgasim","orgasm","penis","penisfucker","piss","piss off","porn","porno","pornography","pussy","retard","sadist","sex","sexy","shit","slut","son of a bitch","suck","tits","viagra","whore","xxx"]],["Watch your language!","Watch your language you stupid bitch!","Watch your language young lady!","Watch yourself brown man!"],[689166454,696039268,496220023])
            #respond_trigger_words(update,False,[["dinner","lunch","breakfast","dessert","supper"],"what",["I don't know, ask your mother.","How would I know?","You know I can't cook."])
            respond_trigger_words(update,False,[["daddy"]],["You called for me?"])
        except Exception as e:
            # print(e)
            return


'''
def im_statements(update):
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
    triggers+=addtextafter('im',text)
    triggers+=addtextafter('IM',text)
    triggers+=addtextafter('iM',text)
    triggers+=addtextafter('Im',text)
    # weird ’
    triggers+=addtextafter('i’m',text)
    triggers+=addtextafter('I’M',text)
    triggers+=addtextafter('i’M',text)
    triggers+=addtextafter('I’m',text)
    # normal '
    triggers+=addtextafter("i'm",text)
    triggers+=addtextafter("I'M",text)
    triggers+=addtextafter("i'M",text)
    triggers+=addtextafter("I'm",text)
    for response in triggers:
        if len(response) != 0:
            send_message("Hi {}, I'm dad.".format(response.strip(" ")),chat)
'''
def respond_trigger_stickers(update, responses, stickerid = -1, packid = -1):
    try:
        sticker = update['message']['sticker']['file_id']
        pack = update['message']['sticker']['set_name']
        chat = update["message"]["chat"]["id"]
        # print(f'Sticker: {sticker}\tId Needed:{stickerid}')
        if stickerid == sticker:
            send_message(responses[random.randint(0,len(responses)-1)],chat)
        if packid == pack:
            # do somthing here
            pass
    except Exception as e:
        pass
        # print(e)

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
