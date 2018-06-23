# import sys
# import time
# import telepot
# from telepot.loop import MessageLoop
# import random
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# #import asyncio
#
# #token = '491905862:AAFLeZ9-H56wumXpGN0LoyUN_1Dmm751nH8'
# token = '570050014:AAGrqiHt0choAHLYANzc8-8bcUHI5VzbRFw'
# bot = telepot.Bot(token)
#
# message_with_inline_keyboard = None
#
#
# def on_chat_message(msg):
#     content_type, chat_type, chat_id = telepot.glance(msg)
#     print('Chat:', content_type, chat_type, chat_id, msg)
#
#     if content_type != 'text':
#         return
#
#     command = msg['text'].lower()
#
#     msg_id = msg['message_id']
#
#     if (command == 'schedule') or (command == '/start'):
#         first_message = 'Hi, {}! Who do you want to schedule the meeting with?'.format(msg['from']['first_name'])
#         bot.sendMessage(chat_id, first_message)
#
#     if msg_id != msg['message_id']:
#         second_message = 'How long do you want to meet {}?'.format(msg['text'])
#         bot.sendMessage(chat_id, second_message)
#
#     if msg_id != msg['message_id']:
#         third_message = 'Great!'
#         bot.sendMessage(chat_id, third_message)
#
#
#
#     # keyboard = InlineKeyboardMarkup(inline_keyboard=[
#     #                [InlineKeyboardButton(text='Press me', callback_data='press')],
#     #            ])
#
#     # if command == '/start':
#     #     markup = InlineKeyboardMarkup(inline_keyboard=[
#     #         # [dict(text='Telegram URL', url='https://core.telegram.org/')],
#     #         [InlineKeyboardButton(text='Schedule a Meeting', callback_data='schedule')],
#     #         # [dict(text='Callback - show alert', callback_data='alert')],
#     #         # [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
#     #         # [dict(text='Switch to using bot inline', switch_inline_query='initial query')],
#     #     ])
#     #
#     #     bot.sendMessage(chat_id, 'What do you want to do?', reply_markup=markup)
#
#
# def on_callback_query(msg):
#     query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
#     print('Callback Query:', query_id, from_id, data)
#
#     # bot.answerCallbackQuery(query_id, text='Got it')
#
#     if data == 'schedule':
#         bot.answerCallbackQuery(query_id, text='Scheduling a meeting.')
#     # if data == 'notification'
#     #     bot.answerCallbackQuery(query_id, text='Notification at top of screen')
#     # elif data == 'alert':
#     #     bot.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
#     # elif data == 'edit':
#     #     global message_with_inline_keyboard
#     #
#     #     if message_with_inline_keyboard:
#     #         msg_idf = telepot.message_identifier(message_with_inline_keyboard)
#     #         bot.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
#     #     else:
#     #         bot.answerCallbackQuery(query_id, text='No previous message to edit')
#
# MessageLoop(bot, {'chat': on_chat_message,
#                   'callback_query': on_callback_query},).run_as_thread()
#
# print('Listening ...')
#
# while 1:
#     time.sleep(10)