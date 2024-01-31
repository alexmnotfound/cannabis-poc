import sys
sys.path.append("..")  # Add the parent directory to sys.path

import logging, asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, CallbackContext
from .keyboard_layouts import MAIN_KEYBOARD, RETURN_KEYBOARD, SEARCH_KEYBOARD


class MyMainBot:
    def __init__(self, token):
        self.logger = logging.getLogger(__name__)
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logger.info(f"User {update.effective_user.id} started the bot")
        welcome_message = ('🤖: Hello there. I am your helpful assistant that holds Cannabis related knowledge.\n'
                           'How can I help you?:')
        await update.message.reply_text(welcome_message, reply_markup=MAIN_KEYBOARD)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()

            '''
            if query.data in ['run_search', 'get_info', 'get_all_reports']:
                await self.handle_report_request(context, query, query.data)
            '''
            if query.data == 'run_search':
                await query.edit_message_text(text="🤖: Choose which type of search you want to do.",
                                              reply_markup=SEARCH_KEYBOARD)
            elif query.data == 'get_info':
                await query.edit_message_text(text="🤖: Sorry this isn't ready yet",
                                              reply_markup=RETURN_KEYBOARD)
            elif query.data == 'return':
                await query.edit_message_text(text='🤖: What else can I do for you?',
                                              reply_markup=MAIN_KEYBOARD)
        except Exception as e:
            self.logger.error(f"Something failed while processing: {e}")
            await query.edit_message_text(text='⚠️ Sorry but something failed while processing query.\n'
                                               '🤖: What else can I do for you?',
                                          reply_markup=MAIN_KEYBOARD)

    def setup_handlers(self):
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CallbackQueryHandler(self.button))

    def run(self):
        self.application.run_polling()

