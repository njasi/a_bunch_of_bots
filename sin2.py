import botbase
import time

TARGET = -1
BOT = botbase.BotBase()

def main(): 
    last_update_id = None
    while True:
        updates = BOT.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = BOT.get_last_update_id(updates) + 1
            forward(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()

def forward(updates):
    for update in updates:
        BOT.send_forward(update["message"]["message_id"], update["message"]["message_id"],TARGET)