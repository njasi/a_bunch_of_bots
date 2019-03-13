import botbase
import time
# lrt = open("LRT","r")
# token = lrt.readline().strip()
token = "688427290:AAGDtkCK6KVQnY4DXED8sy5zG5imojkOpQI"
BOT = botbase.BotBase("https://api.telegram.org/bot{}/".format(token))

def main():
    last_update_id = None
    while True:
        updates = BOT.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = BOT.get_last_update_id(updates) + 1
            respond(updates)
        time.sleep(0.5)

def respond(updates):
    print("Responding")
    for update in updates["result"]:
        try:
            message = update["message"]
            print(message)
            # BOT.send_forward(message["message_id"], message["chat"]["id"], )
        except Exception as e:
            print("Error: {}".format(e))
            pass
            # BOT.send_message("There was an error ({}) forwarding this message: {}".format(e, message), -286832243)

if __name__ == "__main__":
    main()
