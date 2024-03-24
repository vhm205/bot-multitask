import os
import logging
import textwrap
import google.generativeai as genai
from IPython.display import Markdown
from IPython.display import display
from telegram import Update
from telegram.ext import ContextTypes

from helpers.utils import extract_text_from_command

API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

async def google_ai_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    try:
        _, text = extract_text_from_command(update.message.text)

        response = model.generate_content(text, stream=True)
        for chunk in response:
            await update.message.reply_text(f"```{chunk.text}```", parse_mode="MarkdownV2")
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
        logging.exception(e)
