import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import TOKEN, LOG_FILE


# Enable logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Logging to file
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
# Logging to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


class Bot:
    def __init__(self):

        self.updater = Updater(TOKEN)
        self.dsp = self.updater.dispatcher

        # register handler functions which define how the bot reacts to events
        self.dsp.add_handler(CommandHandler("start", get_help))
        self.dsp.add_handler(CommandHandler("help", get_help))
        self.dsp.add_handler(CommandHandler("sentiment", get_sentiment))
        self.dsp.add_handler(MessageHandler(Filters.text, echo))
        self.dsp.add_error_handler(error)

        logger.info('Im alive!')

    def power_on(self):
        # start the Bot
        self.updater.start_polling()
        self.updater.idle()

# define command handlers. These usually take the two arguments: bot and
# update. Error handlers also receive the raised TelegramError object in error.


def echo(bot, update):
    logger.info('echo recieved message: {}'.format(update.message.text))
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    # all uncaught telegram-related exceptions will be rerouted here
    logger.error('Update "%s" caused error "%s"' % (update, error))


def get_help(bot, update):
    logger.info('get_help recieved message: {}'.format(update.message.text))
    help_msg = ('Greetings, {} {}! Name is {}, at your service.\n'
                'I currently support the following commands:\n'
                '/start - begins our chat and prints this message\n'
                '/help - prints this message\n'
                '/sentiment [message] - predicts the sentiment of the message').format(
        update.message.from_user.first_name, update.message.from_user.last_name, bot.name)
    bot.sendMessage(update.message.chat_id, text=help_msg)


def get_sentiment(bot, update):
    logger.info('get_sentiment recieved message: {}'.format(update.message.text))
    try:
        # get message text without the command '/sentiment'
        usr_msg = update.message.text.split(' ', maxsplit=1)[1]
        msg_sentiment = 0.5
        '''
        Now determine the sentiment of usr_msg.
        This should return a real number in [0,1].
        Your code goes here.
        '''
        bot.sendMessage(update.message.chat_id, text=msg_sentiment)
    except IndexError:
        bot.sendMessage(update.message.chat_id, text='Write your message after the command')
    except Exception as e:
        logger.error(e)

my_bot = Bot()
my_bot.power_on()
