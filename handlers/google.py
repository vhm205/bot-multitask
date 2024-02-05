from googlesearch import search
from telegram import Update
from telegram.ext import ContextTypes

async def google_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    search_results = search(update.message.text, num_results=10, lang="en")
    reply_message = ""
    for result in search_results:
        reply_message += result + "\n"
        reply_message += "-----------\n"

    await update.message.reply_text(reply_message)
