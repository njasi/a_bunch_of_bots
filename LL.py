import botbase
import time

BOT = botbase.BotBase("https://api.telegram.org/bot672157411:AAFdc-pkC-K2QGLwOIPVhpIoWZxKbx4eQ9g/")

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
            message = update["message"]
            if(message["chat"]["id"] == -1001290963588):
                BOT.send_forward(message["message_id"], message["chat"]["id"], -1001290963588)
        except Exception as e:
            BOT.send_message("There was an error ({}) forwarding this message: {}".format(e, message), -1001290963588)
        pass

if __name__ == "__main__":
    main()