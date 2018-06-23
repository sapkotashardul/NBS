from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)
import logging
import pandas as pd
from dbhelper import DBHelper
db = DBHelper()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PERSON, NAME, PERIOD, AVAILABILITY = range(4)


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

def typing(bot, update):
    timing = ['Monday',"Wednesday","Friday"]
    keyboard = [[InlineKeyboardButton(timing[0], callback_data='1'),
                    InlineKeyboardButton(timing[1], callback_data='2')],
                [InlineKeyboardButton(timing[2], callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def period(bot, update):
    user = update.message.from_user
    length_of_event = update.message.text
    update.message.reply_text("Great, here are your free times!")
    free_times = db.get_free_time('1')
    for i in range(len(free_times)):
        day = pd.Timestamp(free_times[i][0]).date()
        start = pd.Timestamp(free_times[i][0])
        end = pd.Timestamp(free_times[i][1])
        free_period = pd.Timedelta(end - start)
        if free_period > pd.Timedelta(length_of_event + 'minutes'):
            update.message.reply_text(str(day) + ", " + str(start.time()) + " => " + str(end.time()))
    return AVAILABILITY

def availability(bot, update):
    update.message.reply_text("Great, here are your free times!")
    return ConversationHandler.END

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

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PERSON: [MessageHandler(Filters.text, person)],

            NAME: [MessageHandler(Filters.text, name)],

            PERIOD: [MessageHandler(Filters.text, period)],

            AVAILABILITY: [MessageHandler(Filters.text, availability)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.dispatcher.add_handler(CommandHandler('typing', typing))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

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