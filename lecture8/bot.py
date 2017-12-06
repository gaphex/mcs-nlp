import os
import json
import pickle
import asyncio
import logging
import telegram
import subprocess

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from speech2text import speech2text
from config import TOKEN, LOG_FILE, DL_DIR


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
        self.dsp.add_handler(MessageHandler(Filters.text, echo))
        self.dsp.add_handler(MessageHandler(Filters.voice, process_audio))
        Filters.audio
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
                'My purpose is to demonstrate how ').format(
        update.message.from_user.first_name, update.message.from_user.last_name, bot.name)
    bot.sendMessage(update.message.chat_id, text=help_msg)
    
    
def process_audio(bot, update):
    logger.info('process_audio recieved: {}'.format(''))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:

        voice_file_id = update.message.voice.file_id
        voice_file = bot.get_file(voice_file_id)
        ogg_fname = "{}/{}".format(DL_DIR, "voice.ogg")
        voice_file.download(ogg_fname)
        logger.info('downloaded')
        transcript = speech2text(ogg_fname)
        bot.sendMessage(update.message.chat_id, text=transcript)

    except Exception as e:
        logger.error(e)

my_bot = Bot()
my_bot.power_on()
