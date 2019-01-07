import json 
import requests
import time
import urllib
import string
import random
#https://api.telegram.org/bot747219156:AAGjhBS5K5zdSkVX-tBRWyWFB6LwcUUK3ZY/
TOKEN = "747219156:AAGjhBS5K5zdSkVX-tBRWyWFB6LwcUUK3ZY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

TRIGGER_STICKERS = [
    ('CAADAwADsAAD3zLTBKfU4jQkFBUNAg',['Consider it done.']), # dispose of me daddy
    ('CAADAwADuAAD3zLTBEV5-LhZIiJkAg',['Buck up.']), # my soul hurts
    ('CAADAwADwAAD3zLTBAABl0ACYJXbeQI',['This is an uwu free zone.']), # uwu
    ('CAADAwADxgAD3zLTBB8m_S3gDUW3Ag',['How about no.','Sounds a bit painful.']), # shove a lightbulb inside my dickhole daddy
    ('CAADAwADyAAD3zLTBP5Y0z4p9JMoAg',['Insest is illegal']), # now fuck me daddy
    ('CAADAwADygAD3zLTBO_CGtaM2LrRAg',['yes']), # did i stutter daddy
    ('CAADAwADzAAD3zLTBAl7XLD9oFBjAg',['No problem.']), # ok thanks daddy <3
    ('CAADAwAD1gAD3zLTBNdMSWtxaA1rAg',['MMMMMMMMMMMMMMMMMMMMM']), # mmmmmmmmmmmmmMMMMmmMMMMMAAAAAAAAA
    ('CAADAwAD2gAD3zLTBA2OObFB0orZAg',['This is an owo free zone.']), # OwO
    ('CAADAwAD3gAD3zLTBG7BGyns-Q-rAg',['Thanks... I guess.']), # you're welcome daddy ;3
    ('CAADAwAD8gAD3zLTBBltgX3F7Tg_Ag',['Shh... your mother will hear.','Don\'t tell  you mother about that.]), # OH YES DADDY ;3c
    ('CAADAwAD9AAD3zLTBFITV1FEQlAPAg',['Thank you ;)','Thank you for that']), # sleep tight daddy
    ('CAADAwAD-AAD3zLTBBAcdoi5daPPAg',['Daddy is always right']), # true daddy, true X3
    ('CAADAwADEQEAAt8y0wQH4L_Joq0qrQI',['This is an owo free zone.']), # u know it daddy uwu
    ('CAADAwADEwEAAt8y0wSO2HneIaTiQwI',['That\'s right do as daddy says']), # ok dad uwu
    ('CAADAwADFQEAAt8y0wQNW8xC5uBCNwI',['Do you though?']), # we know dad uwu
    ('CAADAwADFwEAAt8y0wTKYycSRm6JVgI',['That\'s right do as daddy says']), # yes dad
    ('CAADAwADGQEAAt8y0wS1GPsnzrFOcwI',["You're grounded.",'You can\'t say no to me.']), # no dad
    ('CAADAwADHQEAAt8y0wR2OKokZR20HQI',['You better not tell the police']), # what the fuck daddy uwu
    ('CAADAwADHwEAAt8y0wQjvZG9HLIgHAI',['This is an owo free zone.']), # anything you want daddy uwu
    ('CAADAwADIQEAAt8y0wRg94L_15iYDwI',['Ok']), # have fun daddy uwu
    ('CAADAwADIwEAAt8y0wSBdYX9PBGsgwI',['Since you asked so nicely...']), # oh boy yes please daddy
    ('CAADAwADJQEAAt8y0wRaGpQJWgUBJQI',['Of what exactly?']) # i need pics daddy
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
            respond_trigger_words_user(update,True,[["heck","anus","arse","arsehole","ass","bitch","inappropriate","inappropriate","inappropriate","cocksucking","coochie","coddamnit","coochy","cooter","cum","cumbubble","cumdumpster","cummer","cumming","cumshot","cumslut","cuntface","cunthole","cuntlick","cuntlicker","inappropriate","dickbag","dickbeaters","dickface","dickfuck","dickhead","dickhole","dickjuice","dickmilk","dickslap","dickwad","dickweasel","dickweed","dickwod","dildo","dink","inappropriate","inappropriate","inappropriate","inappropriate","inappropriate","hayward","fag","freaking","faggot","fuck","fuckersucker","fuckface","fuckhead","fuckhole","fuckin","fucking","fuckme","fucknut","fucknutt","fuckoff","fuckstick","fucktard","fuckup","fuckwad","fuckwit","fuckwitt","fudgepacker","fuk","gangbang","gangbanged","goddamn","blasphemy","inappropriate","gooch","gook","gringo","guido","handjob","hardcoresex","heeb","hell","ho","hoe","homo","homodumbshit","honkey","horniest","horny","hotsex","humping","jackass","jap","jigaboo","jism","jiz","jizm","jizz","jungle bunny","junglebunny","kike","kock","kondum","kooch","kootch","kum","kumer","kummer","kumming","kums","kunilingus","kunt","kyke","lezzie","lust","lusting","mcfagget","mick","minge","mothafuck","mothafucka","mothafuckin","mothafucking","mothafucks","motherfuck","motherfucked","motherfucker","munging","nut","nutt","negro","nigga","nigger","niglet","nut sack","nutsack","orgasim","orgasm","paki","panooch","pecker","peckerhead","penis","penisfucker","penispuffer","phonesex","phuk","phuked","phuking","phukked","phukking","phuks","phuq","pis","pises","pisin","pising","pisof","piss","pissed","pisser","pisses","pissflaps","pissin","pissing","pissoff","polesmoker","pollock","poon","poonani","poonany","poontang","porch monkey","porchmonkey","porn","porno","pornography","pornos","prick","punanny","punta","pusies","pussy","shitass","shitbag","shitbagger","shitbrain","shitbreath","shitcunt","shitdick","shited","shitface","shitfaced","inappropriate","inappropriate","shitted","shitter","shittiest","shitting","shitty","shity","shiz","shiznit","skank","sex","skeet","skullfuck","slut","slutbag","sluts","smeg","smut","snatch","spic","spick","splooge","spunk","tard","testicle","thundercunt","tit","tits","titfuck","tittyfuck","twat","twatlips","twatwaffle","unclefucker","va-j-j","vag","vagina","vjayjay","wank","wetback","whore","whorebag","whoreface","jew","jews","anal","anus","arse","ass","ass fuck","ass hole","assfucker","asshole","assshole","bastard","bitch","black cock","bloody hell","boong","cock","cockfucker","cocksuck","cocksucker","coon","coonnass","crap","cunt","cyberfuck","damn","darn","dick","dirty","douche","dummy","erect","erection","erotic","escort","fag","faggot","fuck","Fuck off","fuck you","fuckass","fuckhole","god damn","gook","hardcore","hardcore","homoerotic","hore","lesbian","lesbians","mother fucker","motherfuck","motherfucker","negro","nigger","orgasim","orgasm","penis","penisfucker","piss","piss off","porn","porno","pornography","pussy","retard","sadist","sex","sexy","shit","slut","son of a bitch","suck","tits","viagra","whore","xxx"]],["Watch your language!","Watch your language you stupid bitch!","Watch your language young lady!","Watch yourself brown man!"],[689166454,696039268,496220023])
            im_statements(update)
            respond_trigger_words(update,False,[["dad","dadbot","daddy"],["joke"]],["Did you hear about the restaurant on the moon? Great food, no atmosphere.","What do you call a fake noodle? An Impasta.","How many apples grow on a tree? All of them.","Want to hear a joke about paper? Nevermind it's tearable.","I just watched a program about beavers. It was the best dam program I've ever seen.","Why did the coffee file a police report? It got mugged.","How does a penguin build its house? Igloos it together.","Dad, did you get a haircut? No I got them all cut.","What do you call a Mexican who has lost his car? Carlos.","Dad, can you put my shoes on? No, I don't think they'll fit me.","Why did the scarecrow win an award? Because he was outstanding in his field.","Why don't skeletons ever go trick or treating? Because they have no body to go with.","I'll call you later. Don't call me later, call me Dad.","What do you call an elephant that doesn't matter? An irrelephant","Want to hear a joke about construction? I'm still working on it.","What do you call cheese that isn't yours? Nacho Cheese.","Why couldn't the bicycle stand up by itself? It was two tired.","What did the grape do when he got stepped on? He let out a little wine.","I wouldn't buy anything with velcro. It's a total rip-off.","The shovel was a ground-breaking invention.","Dad, can you put the cat out? I didn't know it was on fire.","This graveyard looks overcrowded. People must be dying to get in there.","Whenever the cashier at the grocery store asks my dad if he would like the milk in a bag he replies, No, just leave it in the carton!","5/4 of people admit that they’re bad with fractions.","Two goldfish are in a tank. One says to the other, \"do you know how to drive this thing?\"","What do you call a man with a rubber toe? Roberto.","What do you call a fat psychic? A four-chin teller.","I would avoid the sushi if I was you. It’s a little fishy.","To the man in the wheelchair that stole my camouflage jacket... You can hide but you can't run.","The rotation of earth really makes my day.","I thought about going on an all-almond diet. But that's just nuts.","What's brown and sticky? A stick.","I’ve never gone to a gun range before. I decided to give it a shot!","Why do you never see elephants hiding in trees? Because they're so good at it.","Did you hear about the kidnapping at school? It's fine, he woke up.","A furniture store keeps calling me. All I wanted was one night stand.","I used to work in a shoe recycling shop. It was sole destroying.","Did I tell you the time I fell in love during a backflip? I was heels over head.","I don’t play soccer because I enjoy the sport. I’m just doing it for kicks."])
            respond_trigger_words(update,False,[["dinner","lunch","breakfast","dessert","supper"],"what"],["I don't know, ask your mother.","How would I know?","You know I can't cook."])
            respond_trigger_words(update,False,[["daddy"]],["You called for me?"])
        except Exception as e:
            print(e)
            return



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

def respond_trigger_stickers(update, responses, stickerid = -1, packid = -1):
    try:
        sticker = update['message']['sticker']['file_id']
        pack = update['message']['sticker']['set_name']
        chat = update["message"]["chat"]["id"]
        # print(f'{sticker}')
        if stickerid == sticker:
            send_message(responses[random.randint(0,len(responses)-1)],chat)
    except Exception as e:
        pass
        #print(e)

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
