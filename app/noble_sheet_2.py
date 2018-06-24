from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler, InlineQueryHandler)
import logging
import pandas as pd
from dbhelper import DBHelper
db = DBHelper()
import logging
from uuid import uuid4
from telegram.utils.helpers import escape_markdown
import pandas as pd 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PERSON, NAME, PERIOD, REQUEST, RESPONSE, AVAILABILITY = range(6)

CHAT_ID_Y = 441698305
CHAT_ID_X = 529025540
CHOSEN_PERIODS = []
LENGTH_OF_EVENT = 0

def start(bot, update):
    user = update.message.from_user
    update.message.reply_text(
        'Hi, {}! Who do you want to schedule a meeting with?'.format(user.first_name))
    return PERSON

def person(bot, update):
    user = update.message.from_user
    name_of_user = update.message.text
    update.message.reply_text("What's the name of the event?")
    return NAME

def name(bot, update):
    user = update.message.from_user
    name_of_event = update.message.text
    update.message.reply_text("How long do you want the event to be (in minutes)?")
    return PERIOD

# def typing(bot, update):
#     timing = ['Monday',"Wednesday","Friday"]
#     keyboard = [[InlineKeyboardButton(timing[0], callback_data='1'),
#                     InlineKeyboardButton(timing[1], callback_data='2')],
#                 [InlineKeyboardButton(timing[2], callback_data='3')]]
#
#     reply_markup = InlineKeyboardMarkup(keyboard)
#
#     update.message.reply_text('Please choose:', reply_markup=reply_markup)
#
# def button(bot, update):
#     query = update.callback_query
#
#     bot.edit_message_text(text="Selected option: {}".format(query.data),
#                           chat_id=query.message.chat_id,
#                           message_id=query.message.message_id)

def period(bot, update):
    user = update.message.from_user
    LENGTH_OF_EVENT = update.message.text
    update.message.reply_text("Great, here are your free times!")
    free_times = db.get_free_time('1')
    keyboard = []
    index = 0
    for i in range(len(free_times)):
        day = pd.Timestamp(free_times[i][0]).date()
        start = pd.Timestamp(free_times[i][0])
        end = pd.Timestamp(free_times[i][1])
        free_period = pd.Timedelta(end - start)
        if free_period > pd.Timedelta(str(LENGTH_OF_EVENT) + 'minutes'):
            response = str(day) + ", " + str(start.time()) + " => " + str(end.time())
            CHOSEN_PERIODS.append([start, end])
            #update.message.reply_text(str(day) + ", " + str(start.time()) + " => " + str(end.time()))
            keyboard.append([InlineKeyboardButton(response, callback_data='{}'.format(index))])
            index = index + 1
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose your most preferred time:', reply_markup=reply_markup)
    return REQUEST

def request(bot, update):
    query = update.callback_query
    print CHOSEN_PERIODS
    print query.data
    print query.message
    interval = CHOSEN_PERIODS[int(query.data)-1]
    # keyboard = [[InlineKeyboardButton("Request Meeting",
    #                                   switch_inline_query="{} wants to schedule a meeting with you".format(
    #                                       query.message['chat']['first_name']
    #                                       )),
    #              ]]


    #keyboard = [[InlineKeyboardButton("Request Meeting", callback_data='{}'.format(2))]]
    #reply_markup = InlineKeyboardMarkup(keyboard)
    free_times = db.get_free_time('2', interval[0], interval[1])
    print "FREE TIME ", free_times
    keyboard = []
    index = 0
    bot.send_message(chat_id=CHAT_ID_Y,
                     text='Hi! {} wants to schedule a meeting with you. You are free in the following timeslots. Please pick one.'.format('Shardul'))

    for i in range(len(free_times)):
        day = pd.Timestamp(free_times[i][0]).date()
        start = pd.Timestamp(free_times[i][0])
        end = pd.Timestamp(free_times[i][1])
        free_period = pd.Timedelta(abs(end - start))
        # print "Free_PERIOD ", free_period
        # print "THE TIMEDE:TA ", pd.Timedelta(str(LENGTH_OF_EVENT) + 'minutes')
        if free_period > pd.Timedelta(str(LENGTH_OF_EVENT) + 'minutes'):
            response = str(day) + ", " + " from " + str(start.time()) + " to " + str(end.time())
            print "response", response
            # update.message.reply_text(str(day) + ", " + str(start.time()) + " => " + str(end.time()))

    keyboard.append([InlineKeyboardButton(response, callback_data='{}'.format("index"))])        
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=CHAT_ID_Y, text='Option(s):',
                     reply_markup=reply_markup)
    
    #keyboard.append([InlineKeyboardButton("HERE HERE", callback_data="i")])
   
    #bot.send_message(chat_id=CHAT_ID_Y, text="YEAH", reply_markup=reply_markup)
    #update.message.reply_text('Please choose:', reply_markup=reply_markup)
#     bot.send_message(bot.send_message(chat_id=query.message.chat_id,
#                      text='Thanks! Scheduling as per request')
# )
    # if (len(free_times) == 0):
    #     bot.send_message(chat_id=CHAT_ID_Y,
    #                      text='Hi! {} wants to schedule a meeting with you. Unfortunately, your schedule is not free.'.format(
    #                          'Shardul'), reply_markup=reply_markup)
    # else:
    #     bot.send_message(chat_id=CHAT_ID_Y,
    #                  text='Hi! {} wants to schedule a meeting with you. You are free in the following timeslots. Please pick one.'.format('Shardul'), reply_markup=reply_markup)
    return RESPONSE

def response(bot,update):
    update.message.reply_text("Great, here are your free times!")
    bot.send_message(chat_id=CHAT_ID_X, text="Thanks! Scheduling as requested.")
    return AVAILABILITY

# def period2(bot, update):
#     interval = chosen_periods[choice_index]
#     user = update.message.from_user
#     length_of_event = update.message.text
#     update.message.reply_text("Hi! {}! wants to meet you for a 'select period here' between [select values of interval here]")
#     free_times = db.get_free_time('2', interval[0], interval[1])
#     chosen_periods = []
#     keyboard = []
#     index = 0
#     for i in range(len(free_times)):
#         day = pd.Timestamp(free_times[i][0]).date()
#         start = pd.Timestamp(free_times[i][0])
#         end = pd.Timestamp(free_times[i][1])
#         free_period = pd.Timedelta(end - start)
#         if free_period > pd.Timedelta(length_of_event + 'minutes'):
#             response = str(day) + ", " + str(start.time()) + " => " + str(end.time())
#             chosen_periods.append(response)
#             #update.message.reply_text(str(day) + ", " + str(start.time()) + " => " + str(end.time()))
#             keyboard.append([InlineKeyboardButton(response, callback_data='{}'.format(index))])
#             index = index + 1
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Please choose:', reply_markup=reply_markup)
#     return AVAILABILITY

def availability(bot, update):
    query = update.callback_query
    user = update.message.from_user
    print "added"
    bot.send_message(chat_id=CHAT_ID_X, text='Great! Your meeting has been added to the calendar :)'
                     )


    # keyboard = [[InlineKeyboardButton("Request Meeting with", switch_inline_query="{} wants to schedule a meeting with you".format(update.message.from_user['first_name'])),
    # ]]
    # reply_markup = InlineKeyboardMarkup(keyboard)

    # update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    #query = update.inline_query
    query = update.callback_query

def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)



def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    
    return ConversationHandler.END

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("570050014:AAGrqiHt0choAHLYANzc8-8bcUHI5VzbRFw")
    #updater = Updater("491905862:AAFLeZ9-H56wumXpGN0LoyUN_1Dmm751nH8")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PERSON: [MessageHandler(Filters.text, person)],

            NAME: [MessageHandler(Filters.text, name)],

            PERIOD: [MessageHandler(Filters.text, period)],

            REQUEST: [CallbackQueryHandler(request)],

            RESPONSE: [MessageHandler(Filters.text, response)],
            #RESPONSE: [CallbackQueryHandler(response)],

            AVAILABILITY: [CallbackQueryHandler(availability)] 
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(InlineQueryHandler(button))
    #dp.add_handler(InlineQueryHandler(inlinequery))
    #dp.add_handler(CallbackQueryHandler(request))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()





'''



def typing(bot, update):
timing = ['Monday',"Wednesday","Friday"]
keyboard = [[InlineKeyboardButton(timing[0], callback_data='1'),
                InlineKeyboardButton(timing[1], callback_data='2')],
            [InlineKeyboardButton(timing[2], callback_data='3')]]

reply_markup = InlineKeyboardMarkup(keyboard)

update.message.reply_text('Please choose:', reply_markup=reply_markup)



    
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")


    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    '''