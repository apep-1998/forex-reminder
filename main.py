#! /usr/bin/python
"""
    @Author_name : Arsham mohammadi nesyshabori
    @Author_email : arshammoh1998@gmail.com
    @Author_nickname : apep
    @date : 
    @version : 
"""

# start telegram bot import
from telepot.loop import MessageLoop
import telepot
import time
from datetime import datetime
from datetime import timedelta
import json
# end telegram bot import


bot = telepot.Bot("1299872997:AAGST7kJMFZWyspoNECORAR-je-QxXukt9s")

with open("data.json", "r") as data:
    remides_list = json.load(data)
user_save = {}

def chat_message_handel(message):
    text = message["text"]
    user_id = message['from']["id"]
    
    if text == "/start":
        bot.sendMessage(user_id, "با دستور /new میتوانید یادآوری جدید ایجاد کنید")
        
    
    if text == "/new":
        user_save[user_id] = []
        bot.sendMessage(user_id, "نام نماد را وارد کنید")

    elif len(user_save.get(user_id)) == 0:
        user_save[user_id].append(text)
        bot.sendMessage(user_id, "چه مدت دیگر یادآوری شود؟ hh:mm")
    
    elif len(user_save.get(user_id)) == 1:
        t = text.split(":")
        if len(t) == 2 and t[0].isdigit() and t[1].isdigit():
            h, m = t
            re_time = datetime.now()+ timedelta(hours=int(h), minutes=int(m))
            user_save[user_id].append(datetime.timestamp(re_time))
            user_save[user_id].append(user_id)
            remides_list.append(user_save[user_id])
            del user_save[user_id]
            bot.sendMessage(user_id, "ثبت شد")
            with open("data.json", "w") as data:
                json.dump(remides_list, data)
        else:
            bot.sendMessage(user_id, "لطفا عدد وارد کنید")
        

def button_message_handel(message):
    pass

MessageLoop(bot,{'chat': chat_message_handel,
                 'callback_query': button_message_handel}).run_as_thread()

while True:
    i = 0
    while i < len(remides_list):
        if datetime.timestamp(datetime.now()) > remides_list[i][-2]:
            try:
                bot.sendMessage(remides_list[i][-1], "یادآوری جهت برسی {}".format(remides_list[i][0]))
            except Exception as e:
                print(e)
            del remides_list[i]
            with open("data.json", "w") as data:
                json.dump(remides_list, data)
        else:
            i+=1
    time.sleep(10)
    
