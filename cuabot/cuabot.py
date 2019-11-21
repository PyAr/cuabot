from functools import wraps

import telegram
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, dispatcher, Updater



class CUABot:

    def __init__(self, config):
        self.config = config

    def start(self, update, context):
        print("Start")
        context.bot.send_message(chat_id=update.effective_chat.id, text="hola")

    def question(self, update, context):
        print("Question")
        keyboard = [[InlineKeyboardButton(room["name"], callback_data=room['chat_id'])] for room in self.config['rooms']]

        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.config['question_message'], reply_markup=reply_markup)

    def on_error(self, update, context):
        print("ERROR: ", context.error)

    def run(self):
        updater = Updater(token=self.config['bot_token'], use_context=True)
        print("====== Bot:", updater)
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler(self.config['question_handler'], self.question))
        updater.dispatcher.add_error_handler(self.on_error)
        print("Runing with config: %s" % self.config)
        updater.start_polling()