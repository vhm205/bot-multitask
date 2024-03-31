import logging
import os
import json
import requests
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

SHORT_URL_API_URL = os.environ.get('BITLY_SHORT_API_URL')
SHORT_URL_API_KEY = os.environ.get('BITLY_SHORT_URL_API_KEY')

API_DEFAULT = "https://api.cloudconvert.com/v2"
CLOUD_CONVERT_API_URL = os.environ.get('CLOUD_CONVERT_API_URL') or API_DEFAULT
CLOUD_CONVERT_API_KEY = os.environ.get('CLOUD_CONVERT_API_KEY')
CLOUD_CONVERT_API_KEY_2 = os.environ.get('CLOUD_CONVERT_API_KEY_2')

CONVERT = 1

async def choose_output_extension(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    ctx.chat_data['ext_output'] = message

    await update.message.reply_text(
        "Please send me a file or send 'done' to stop talking to me.\n",
        reply_markup=ReplyKeyboardRemove()
    )
    return CONVERT

def create_job(url: str, ext_output: str):
    payload = {
        "tasks": {
            "import-file": {
                "operation": "import/url",
                "url": url
            },
            "convert-file": {
                "operation": "convert",
                "input": "import-file",
                "output_format": ext_output,
            },
            "export-file": {
                "operation": "export/url",
                "input": "convert-file"
            }
        },
    }

    response = requests.post(f"{CLOUD_CONVERT_API_URL}/jobs", json=payload, headers={
        "Authorization": f"Bearer {CLOUD_CONVERT_API_KEY_2}", "Content-Type": "application/json"})
    data = json.loads(response.content)

    if response.ok == False and data['code'] == 'CREDITS_EXCEEDED':
        response = requests.post(f"{CLOUD_CONVERT_API_URL}/jobs", json=payload, headers={
            "Authorization": f"Bearer {CLOUD_CONVERT_API_KEY}", "Content-Type": "application/json"})
        data = json.loads(response.content)

        if response.ok == False and data['code'] == 'CREDITS_EXCEEDED':
            raise Exception(data['message'])

    url = data['data']['tasks'][0]['result']['files'][0]['url']
    return url

def create_short_url(long_url: str):
    payload = {
        "long_url": long_url,
        "domain": "bit.ly",
    }
    response = requests.post(f"{SHORT_URL_API_URL}/shorten",
                             json=payload, headers={
                                 "Authorization": f"Bearer {SHORT_URL_API_KEY}",
                                 "Content-Type": "application/json"
                             })
    data = json.loads(response.content)
    short_url = data['link']
    return short_url

async def convert_file_handler(update: Update, ctx: ContextTypes.chat_data):
    try:
        ext_output = ctx.chat_data['ext_output']
        file = await ctx.bot.get_file(update.message.document)

        url = create_job(file.file_path, ext_output)
        short_url = create_short_url(url)

        reply_text = f"Output: {url}\n-------------\nShort URL: {short_url}"
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f'{type(e).__name__}: {e}')
        logging.exception(e)
    finally:
        return ConversationHandler.END
