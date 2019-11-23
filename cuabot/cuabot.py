import pyqrcode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, Filters, MessageHandler


class CUABot:

    def __init__(self, config):
        self.config = config

    def get_bot_url(self, bot):
        bot_user = bot.get_me()
        url = 'https://t.me/{}'.format(bot_user.username)
        return url

    def generate_qr(self, qr_file):
        bot = Bot(self.config['bot_token'])
        url = self.get_bot_url(bot)
        qr = pyqrcode.create(url)
        qr.svg(qr_file, scale=8)
        return url

    def get_commands(self):
        commands = []
        commands.append('{0} - {1}'.format(self.config['question_handler'], self.config['question_handler_description']))
        commands.append('{0} - {1}'.format(self.config['anonymous_question_handler'], self.config['anonymous_question_handler_description']))
        return '\n'.join(commands)

    def start_handler(self, update, context):
        update.message.reply_text(self.config['welcome_message'])

    def get_chat_id(self, update, context):
        update.message.reply_text('Chat ID: {}'.format(update.message['chat']['id']))

    def on_error_handler(self, update, context):
        print('ERROR: ', context.error)

    def question_handler(self, update, context):
        keyboard = [[InlineKeyboardButton(room['name'], callback_data=str(index))]
                    for index, room in enumerate(self.config['rooms'])]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(self.config['select_room_message'], reply_markup=reply_markup)
    
    def anonymous_question_handler(self, update, context):
        context.chat_data['anonymous'] = True
        self.question_handler(update, context)

    def select_room_handler(self, update, context):
        query = update.callback_query
        context.chat_data['selected_room'] = query['data']
        query.edit_message_text(text=self.config['enter_question_message'])

    def question_text_handler(self, update, context):
        # Here we take out the room from the context to not send the question to other room chat
        anonymous = context.chat_data.pop('anonymous', False)
        selected_room_raw = context.chat_data.pop('selected_room', None)
        if selected_room_raw is None:
            update.message.reply_text(self.config['no_room_selected_message'])
        else:
            room_index = int(selected_room_raw)
            selected_room = self.config['rooms'][room_index]
            if (anonymous):
                context.bot.send_message(chat_id=selected_room['chat_id'], text=update.message.text)
            else:
                update.message.forward(selected_room['chat_id'])
            update.message.reply_text('{0} {1}'.format(self.config['sent_question_message'],selected_room['name']))

    def run(self):
        # Fixme validar que no reciba preguntas de grupos
        updater = Updater(token=self.config['bot_token'], use_context=True)
        bot_url = self.get_bot_url(updater.bot)
        print('Cuabot is running on', bot_url)
        updater.dispatcher.add_handler(CommandHandler('start', self.start_handler))
        updater.dispatcher.add_handler(CommandHandler('get_chat_id', self.get_chat_id))
        updater.dispatcher.add_handler(CommandHandler(self.config['question_handler'], self.question_handler))
        updater.dispatcher.add_handler(CommandHandler(self.config['anonymous_question_handler'], self.anonymous_question_handler, pass_chat_data=True))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.select_room_handler, pass_chat_data=True))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.question_text_handler, pass_chat_data=True))
        updater.dispatcher.add_error_handler(self.on_error_handler)
        print('Running with config: {}'.format(self.config))
        updater.start_polling()