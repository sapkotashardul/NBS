# import telepot
# token = '491905862:AAFLeZ9-H56wumXpGN0LoyUN_1Dmm751nH8'
# TelegramBot = telepot.Bot(token)
# print (TelegramBot.getMe())
#
# # alternatively
# # https://api.telegram.org/bot<your-bot-token>/getme
#
#
# # In[5]:
#
#
# # Getting text details
#     # update_id is tied to the message id (increases in chronological order)
# TelegramBot.getUpdates()
#
#
# # In[69]:
#
#
# # Helper code
# import sqlite3
#
# # To-do list code
# class DBHelper:
#     def __init__(self, dbname="todo.sqlite"): #takes a database name and creates a database connection
#         self.dbname = dbname
#         self.conn = sqlite3.connect(dbname)
#
#     def setup(self): #creates a new table
#         stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
#         self.conn.execute(stmt)
#         self.conn.commit()
#
#     def add_item(self, item_text): #takes the text for the item and inserts it into our database
#         stmt = "INSERT INTO items (description) VALUES (?)"
#         args = (item_text, )
#         self.conn.execute(stmt, args)
#         self.conn.commit()
#
#     def delete_item(self, item_text): #takes the text for an item and removes it
#         stmt = "DELETE FROM items WHERE description = (?)"
#         args = (item_text, )
#         self.conn.execute(stmt, args)
#         self.conn.commit()
#
#     def get_items(self): #returns a list of all the items in our database
#         stmt = "SELECT description FROM items"
#         return [x[0] for x in self.conn.execute(stmt)]
#
#
#
# # In[74]:
#
#
# # 1. Initialize
#
# import json
# import requests
# import time
# import urllib
#
# import configparser
#
# import io, os, sys, types
# from IPython import get_ipython
# from nbformat import read
# from IPython.core.interactiveshell import InteractiveShell
#
#
# # In[66]:
#
#
# db = DBHelper()
# TOKEN = '491905862:AAFLeZ9-H56wumXpGN0LoyUN_1Dmm751nH8'
# URL = "https://api.telegram.org/bot{}/".format(TOKEN)
#
#
# # downloads from url and returns a string
# # no exceptions used for simplicity
# def get_url(url):
#     response = requests.get(url)
#     content = response.content.decode("utf8")
#     return content
#
#
# # parses string response into a python dictionary
# def get_json_from_url(url):
#     content = get_url(url)
#     js = json.loads(content)
#     return js
#
#
# # calls api command to retrieve list of updates
#     # offset parameter to indicate the bot will reject messages with lower ids
#     # timeout argument added
# def get_updates(offset=None):
#     url = URL + "getUpdates?timeout=100"
#     if offset:
#         url += "&offset={}".format(offset)
#     js = get_json_from_url(url)
#     return js
#
#
# # loops through each update to return the largest id
# def get_last_update_id(updates):
#     update_ids = []
#     for update in updates["result"]:
#         update_ids.append(int(update["update_id"]))
#     return max(update_ids)
#
#
# # get chat id and message text
# def get_last_chat_id_and_text(updates):
#     num_updates = len(updates["result"])
#     last_update = num_updates - 1
#     text = updates["result"][last_update]["message"]["text"]
#     chat_id = updates["result"][last_update]["message"]["chat"]["id"]
#     return (text, chat_id)
#
#
# # Function 1: Echo reply for each message received
# # use another notebook for this
# # def echo_all(updates):
# #     for update in updates["result"]:
# #         try:
# #             text = update["message"]["text"]
# #             chat = update["message"]["chat"]["id"]
# #             send_message(text, chat)
# #         except Exception as e:
# #             print(e)
#
#
# # In[67]:
#
#
# # Function 2: To-Do List
# def handle_updates(updates):
#     for update in updates["result"]:
#         try:
#             text = update["message"]["text"]
#             chat = update["message"]["chat"]["id"]
#             items = DBHelper().get_items()
#             if text in items:
#                 DBHelper().delete_item(text)
#                 items = DBHelper().get_items()
#             else:
#                 DBHelper().add_item(text)
#                 items = DBHelper().get_items()
#             message = "\n".join(items)
#             send_message(message, chat)
#         except KeyError:
#             pass
#
# # modified to read intervals
# def send_message(text, chat_id):
#     text = urllib.parse.quote_plus(text)
#     url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
#     get_url(url)
#
#
# # manual reply
# # text, chat = get_last_chat_id_and_text(get_updates())
# # send_message(text, chat)
#
#
# # In[68]:
#
#
# # Update with instant response
#
# db.setup()
#
# def main():
#     last_update_id = None
#     while True:
#         updates = get_updates(last_update_id)
#         if len(updates["result"]) > 0:
#             last_update_id = get_last_update_id(updates) + 1
#             echo_all(updates)
#         time.sleep(0.5)
#
#
# if __name__ == '__main__':
#     main()
#
#
# # In[32]:
#
#
# rude = ["Oi", "hey bitch", "Fuck you"]
# nice = ["hello", "hi", "hey beautiful"]
#
#
# # In[35]:
#
#
# text, chat = get_last_chat_id_and_text(get_updates())
# if text in rude:
#     send_message("Eh fuck u", chat)
# elif text in nice:
#     send_message("hey sweetheart", chat)
# elif text not in rude or nice:
#     send_message("sorry repeat", chat)
#
