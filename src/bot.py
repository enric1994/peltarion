#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import cv2
import requests
import json
import base64

TOKEN = os.environ.get('TOKEN')
URL = os.environ.get('URL')
AUTH = os.environ.get('AUTH')


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

DONE = range(1)

def start(update, context):

    user = update.message.from_user
    print("User: %s", user.first_name)
    update.message.reply_text(
        'Hello! 👨‍⚕️ We use AI to detect early signs of skin cancer')
    time.sleep(0.5)
    update.message.reply_text('Please, upload a picture of your skin')

    return 'Photo'


def photo(update, context):

    print('Getting picture...')
    update.message.reply_text("🔬 Analyzing...")

    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    name = '{}_{}.png'.format(user.first_name, time.strftime("%Y%m%d-%H%M%S"))
    filename = '/peltarion/data/{}'.format(name)
    print('Saving picture as "{}"...'.format(filename))
    photo_file.download(filename)
    
    ## Preprocess
    img = cv2.imread(filename)
    # Resize to 64x64
    small = cv2.resize(img, (64,64))
    # Hard crop
    crop_img = small[0:64, 0:64]
    cv2.imwrite(filename,crop_img)

    predict_mask(filename, URL, AUTH)
    print('Image received from API')
    update.message.reply_photo(photo=open('/peltarion/data/result.png', 'rb'),
                                caption="Cancer prediction")

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

def predict_mask(image_path, url, auth, output_path='/peltarion/data/result.png'):
    files = {
        'image': (image_path, open(image_path, 'rb')),
    }

    response = requests.post(url, files=files, auth=(auth, ''))
    base64_image=json.loads(response.text)['mask'].split(',')[1]
    
    imgdata = base64.b64decode(base64_image)
    filename = output_path
    with open(filename, 'wb') as f:
        f.write(imgdata)
    print('done!')

if __name__ == '__main__':
    main()