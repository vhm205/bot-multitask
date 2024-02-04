from telegram import Update
from telegram.ext import ContextTypes
from helpers.utils import *

# https://core.telegram.org/bots/api#markdownv2-style
def get_help_options():
    return r"""*🔖 Danh sách options:*
    sleep \- Sleep the computer
    shutdown \- Shutdown the computer
    restart \- Restart the computer
    logout \- Logout the computer
    help \- Get help"""

async def finance_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    _, option = extract_text_from_command(message)

    match option:
        case _:
            await ctx.bot.send_message(chat_id=update.effective_chat.id, text=get_help_options(), parse_mode="MarkdownV2")
