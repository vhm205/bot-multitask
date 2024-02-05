import os
import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, ContextTypes, filters

from helpers.commands import set_commands

from handlers.google import google_handler
from handlers.os_control import os_control_handler
from handlers.random_food import random_food_handler
from handlers.finance import finance_command_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_commands()
    user = update.message.from_user
    logging.info("User %s started the conversation.", user.full_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {user.name}, I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def get_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await context.bot.getMe()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{message}")

def init():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", get_bot))
    app.add_handler(CommandHandler("os", os_control_handler))
    app.add_handler(CommandHandler("food", random_food_handler))
    app.add_handler(CommandHandler("search", google_handler))

    finance_command_handler(app)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()
