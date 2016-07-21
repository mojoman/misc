#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to fetch page from Lurk using mediawiki api

import mwclient
from telegram.ext import Updater
import telegram
from creole import creole2html
import html2text
import logging
import time
import gc

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Use /lurk <page>')


def lurk(bot, update, args):
	try:	
		# html2text converter
		h2t = html2text.HTML2Text()
		h2t.ignore_links = True
		h2t.ignore_images = True
				
		# MW api connection
		# MW client		
		site = mwclient.Site('lurkmore.to', path='/')
		page_title = " ".join(args)
		page = site.Pages[unicode(page_title)]
		page_text = h2t.handle(creole2html(page.text()))
		chunks = [page_text[i:i+4000] for i in range(0, len(page_text), 4000)]
		for s in chunks:
			time.sleep(2)
			bot.sendMessage(update.message.chat_id, text=s)
		del page
		del site
		gc.collect()
	except:
		bot.sendMessage(update.message.chat_id, text='Use /lurk <page>')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("<TOKEN>")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("lurk", lurk)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
