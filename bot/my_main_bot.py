import sys
sys.path.append("..")  # Add the parent directory to sys.path

import logging, asyncio, openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, CallbackContext, \
    MessageHandler, filters
from groundx import Groundx, ApiException
from openai import OpenAI
from .keyboard_layouts import MAIN_KEYBOARD, RETURN_KEYBOARD, SEARCH_KEYBOARD


class MyMainBot:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.application = Application.builder().token(config["telegram"]["api_key"]).build()
        self.setup_handlers()
        self.groundx = Groundx(api_key=config["groundx"]["api_key"])
        self.openai_client = OpenAI(api_key=config["openai"]["api_key"])
        self.project_id = config["groundx"]["project_id"]

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logger.info(f"User {update.effective_user.id} started the bot")
        welcome_message = ('🤖: Hello there. I am your helpful assistant that holds Cannabis related knowledge.\n'
                           'How can I help you?:')
        await update.message.reply_text(welcome_message, reply_markup=MAIN_KEYBOARD)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()

            if query.data in ['deep_search']:
                await self.handle_search_request(context, query, query.data)
            elif query.data == 'quick_search':
                await query.edit_message_text(text="🤖: Please type and tell me how can I help you.",
                                              reply_markup=SEARCH_KEYBOARD)
                context.user_data['expecting_query'] = True
            elif query.data == 'run_search':
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

    async def handle_search_request(self, context, query, search_type):
        self.logger.info(f"Running search requests.\n")
        # await query.edit_message_text(text="🤖: Retrieving data from Google. Please wait...")

        try:
            # Follow-up message
            follow_up_text = {
                'deep_search': "We should be making questions here but it is not ready yet.\n",
            }.get(search_type, "What else can I do for you?")

            await query.edit_message_text(text=f"🤖: {follow_up_text}\nWhat else can I do for you?",
                                          reply_markup=SEARCH_KEYBOARD)
        except Exception as e:
            self.logger.error(f"Something failed while processing: {e}")
            await query.edit_message_text(text='⚠️ Sorry but something failed while processing query.\n'
                                               '🤖: What else can I do for you?',
                                          reply_markup=SEARCH_KEYBOARD)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.user_data
        if user_data.get('expecting_query'):
            user_query = update.message.text
            response = await self.process_quick_search(user_query)

            # Send the response as a text message
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

            # Then, send the keyboard as a separate message
            await context.bot.send_message(chat_id=update.effective_chat.id, text="What else can I do for you?",
                                           reply_markup=SEARCH_KEYBOARD)

            # Reset the flag
            user_data['expecting_query'] = False

    async def process_quick_search(self, query: str):
        # Process the query here
        self.logger.info(f"Searching GroundX for query: {query}")

        try:
            search_response = self.groundx.search.content(id=self.project_id, query=query)

            # Check if the search response has results
            if search_response.body["search"]["count"] == 0:
                return "I couldn't find any information on that topic. \nIs there anything else I can help you with?"

            maxInstructCharacters = 2000
            instruction = (
                "You are a helpful virtual assistant that answers questions using the content below. Your task is "
                "to create detailed answers to the questions "
                "by combining your understanding of the world "
                "only with the content provided below. Do not share links.")

            results = search_response.body["search"]
            self.logger.info("---- INIT OF RAW RESPONSE ----")
            self.logger.info(search_response)
            self.logger.info("---- END OF RAW RESPONSE ----")

            llmText = ""
            for r in results["results"]:
                if "text" in r and len(r["text"]) > 0:
                    if len(llmText) + len(r["text"]) > maxInstructCharacters:
                        break
                    elif len(llmText) > 0:
                        llmText += "\n"
                    llmText += r["text"]
            self.logger.info("Content fetched successfully from GroundX.")

            content = """%s
                    ===
                    %s
                    ===
                    """ % (instruction, llmText)

            self.logger.info("----------------------")
            self.logger.info(content)
            self.logger.info("----------------------")

            self.logger.info("Sending content to OpenAI for completion.")
            completion = self.openai_client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": content,
                },
                {"role": "user", "content": query},
            ])

            response_message = completion.choices[0].message.content if completion.choices else "No response available."
            self.logger.info("Response sent to user.")

            # Response
            return response_message
        except ApiException as e:
            self.logger.error(f"Error with GroundX API: {e}")
            return f"Error with GroundX API: {e}"
        except openai.OpenAIError as e:
            self.logger.error(f"Error with OpenAI API: {e}")
            return f"Error with OpenAI API: {e}"

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"

    def setup_handlers(self):
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CallbackQueryHandler(self.button))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    def run(self):
        self.application.run_polling()

