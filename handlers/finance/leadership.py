import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# HANDLE LEADER SHIP REPLY
async def leadership_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Leadership message %s", message)
    return ConversationHandler.END
