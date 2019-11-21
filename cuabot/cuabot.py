import pyqrcode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, Filters, MessageHandler


class CUABot:

    def __init__(self, config):
        self.config = config

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.config['welcome_message'])

    def question(self, update, context):
        keyboard = [[InlineKeyboardButton(room["name"], callback_data=str(index))]
                    for index, room in enumerate(self.config['rooms'])]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.config['select_room_message'], reply_markup=reply_markup)

    def on_error(self, update, context):
        print("ERROR: ", context.error)

    def receive_question(self, update, context):
        query = update.callback_query
        context.user_data['selected_room'] = update.callback_query['data']
        query.edit_message_text(text=self.config['enter_question_message'])

    def question_text_handler(self, update, context):
        # Here we take out the room from the context to not send the question to other room chat
        selected_room_raw = context.user_data.pop('selected_room', None)
        if selected_room_raw is None:
            update.message.reply_text(self.config['no_room_selected_message'])
        else:
            room_index = int(selected_room_raw)
            selected_room = self.config['rooms'][room_index]
            update.message.forward(selected_room['chat_id'])
            update.message.reply_text("Gracias su pregunta fue enviada a: %s" % selected_room['name'])

    def get_chat_id(self, update, context):
        update.message.reply_text("Chat ID: %s" % update.message['chat']['id'])

    def generate_qr(self, qr_file):
        bot = Bot(self.config['bot_token'])
        cuabot_url = self.get_bot_url(bot)
        qr = pyqrcode.create(cuabot_url)
        qr.svg(qr_file, scale=8)
        return cuabot_url

    def get_bot_url(self, bot):
        bot_user = bot.get_me()
        cuabot_url = "https://t.me/%s" % bot_user.username
        return cuabot_url

    def run(self):
        # Fixme validar que no reciba preguntas de grupos
        updater = Updater(token=self.config['bot_token'], use_context=True)
        bot_url = self.get_bot_url(updater.bot)
        print("Cuabot is running on", bot_url)
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler(self.config['question_handler'], self.question))
        updater.dispatcher.add_handler(CommandHandler("get_chat_id", self.get_chat_id))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.receive_question, pass_user_data=True))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.question_text_handler, pass_user_data=True))
        updater.dispatcher.add_error_handler(self.on_error)
        print("Running with config: %s" % self.config)
        updater.start_polling()