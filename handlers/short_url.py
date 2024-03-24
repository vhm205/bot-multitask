import logging
import os
import requests
import json
from helpers.utils import extract_option_from_command
from telegram import Update
from telegram.ext import ContextTypes

api_domain = os.environ.get('SHORTEN_URL') or "https://mmoment.tech"
api_version = os.environ.get('SHORTEN_API_VERSION') or "v1"

def get_help_options():
    return r"""*🔖 Danh sách options:*
    m/method\=edit \- Edit short url \(default is create\)
    id \- Short url id
    url \- Original url
    """

def create_short_url(url: str):
    response = requests.post(f"{api_domain}/api/{api_version}/hidden", json={"url": url})
    data = json.loads(response.content)
    return data

def update_short_url(url: str, mid: str):
    response = requests.patch(f"{api_domain}/api/{api_version}/hidden/{mid}", json={"url": url, "mid": mid})
    data = json.loads(response.content)
    return data

async def short_url_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text
        option = extract_option_from_command(message)
        method = option.get("m") or option.get("method")
        mid = option.get("id")
        original_url = option.get("url")

        if original_url is None:
            await ctx.bot.send_message(chat_id=update.effective_chat.id, text=get_help_options(), parse_mode="MarkdownV2")
            return

        if method == "edit":
            result = update_short_url(original_url, mid)
        else:
            result = create_short_url(original_url)

        reply_text = f"This is your short url: {result['shortUrl']}"

        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f'{type(e).__name__}: {e}')
        logging.exception(e)
