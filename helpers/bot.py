import os
import logging
import html
import json
import traceback
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
    bot = await context.bot.getMe()
    message_reply = f"""Name: {bot.first_name}\nID: {bot.id}\nUsername: @{bot.username}"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_reply)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Log the error before we do anything else, so we can see it even if something breaks.
    logging.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id="@vhm_news_tech", text=message, parse_mode="HTML"
    )

def init():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", get_bot))
    app.add_handler(CommandHandler("os", os_control_handler))
    app.add_handler(CommandHandler("food", random_food_handler))
    app.add_handler(CommandHandler("search", google_handler))

    finance_command_handler(app)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)

    app.run_polling()
