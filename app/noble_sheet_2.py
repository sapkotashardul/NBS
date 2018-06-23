from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PERSON, NAME, PERIOD, AVAILABILITY = range(4)


def start(bot, update):
    #reply_keyboard = [['Boy', 'Girl', 'Other']]
    user = update.message.from_user
    update.message.reply_text(
        'Hi, {}! Who do you want to schedule a meeting with?'.format(user.first_name))

        #reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return PERSON


def person(bot, update):
    user = update.message.from_user
    name_of_user = update.message.text
    update.message.reply_text("What's the name of the event?")

    return NAME

def name(bot, update):
    user = update.message.from_user
    name_of_event = update.message.text
    update.message.reply_text("How long do you want the event to be?")

    return PERIOD

def period(bot, update):
    user = update.message.from_user
    length_of_event = update.message.text
    update.message.reply_text("Great, here are your free times!")

    return AVAILABILITY

def availability(bot, update):
    update.message.reply_text("Great, here are your free times!")
    return ConversationHandler.END

# def gender(bot, update):
#     user = update.message.from_user
#     logger.info("Gender of %s: %s", user.first_name, update.message.text)
#     update.message.reply_text('I see! Please send me a photo of yourself, '
#                               'so I know what you look like, or send /skip if you don\'t want to.',
#                               reply_markup=ReplyKeyboardRemove())
#
#     return PHOTO
#
#
# def photo(bot, update):
#     user = update.message.from_user
#     photo_file = bot.get_file(update.message.photo[-1].file_id)
#     photo_file.download('user_photo.jpg')
#     logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
#     update.message.reply_text('Gorgeous! Now, send me your location please, '
#                               'or send /skip if you don\'t want to.')
#
#     return LOCATION
#
#
# def skip_photo(bot, update):
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     update.message.reply_text('I bet you look great! Now, send me your location please, '
#                               'or send /skip.')
#
#     return LOCATION
#
#
# def location(bot, update):
#     user = update.message.from_user
#     user_location = update.message.location
#     logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
#                 user_location.longitude)
#     update.message.reply_text('Maybe I can visit you sometime! '
#                               'At last, tell me something about yourself.')
#
#     return BIO
#
#
# def skip_location(bot, update):
#     user = update.message.from_user
#     logger.info("User %s did not send a location.", user.first_name)
#     update.message.reply_text('You seem a bit paranoid! '
#                               'At last, tell me something about yourself.')
#
#     return BIO
#
#
# def bio(bot, update):
#     user = update.message.from_user
#     logger.info("Bio of %s: %s", user.first_name, update.message.text)
#     update.message.reply_text('Thank you! I hope we can talk again some day.')
#
#     return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


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

            PERIOD: [MessageHandler(Filters.text, period)
                       ],

            AVAILABILITY: [MessageHandler(Filters.text, availability)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

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