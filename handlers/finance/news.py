import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# HANDLE NEWS REPLY
async def news_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("News message %s", message)
    return ConversationHandler.END
