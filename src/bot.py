#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import cv2

TOKEN = os.environ.get('TOKEN')


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

DONE = range(1)

def start(update, context):

    user = update.message.from_user
    print("User: %s", user.first_name)
    update.message.reply_text(
        'Hello! Send the picture you want to analyze 👨‍⚕️')

    return 'Photo'


def photo(update, context):

    print('Getting picture...')
    update.message.reply_text("<image here>")

    return DONE

def done(update, context):
    
    print('Done...')
    update.message.reply_text("Bye!")

    return ConversationHandler.END


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            'Photo': [ 
                MessageHandler(Filters.photo, photo)
            ],

            DONE: [ 
                MessageHandler(Filters.text, done) 
            ],

        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    print('Starting Peltarion Bot...')
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()