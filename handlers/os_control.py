import subprocess
import platform
from telegram import Update
from telegram.ext import ContextTypes
from helpers.utils import extract_text_from_command

# https://core.telegram.org/bots/api#markdownv2-style
def get_help_options():
    return r"""*🔖 Danh sách options:*
    wakeup \- Wake up
    sleep \- Sleep the computer
    shutdown \- Shutdown the computer
    restart \- Restart the computer
    logout \- Logout the computer
    help \- Get help"""

async def os_control_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    _, option = extract_text_from_command(message)

    run_wakeup = {
        "Darwin": ["osascript", "-e", "tell application \"System Events\" to key code 123"],
        # "Darwin": ["caffeinate", "-u", "-t", "2"],
    }

    run_sleep = {
        "Darwin": ["pmset", "sleepnow"],
        "Linux": ["systemctl", "suspend"],
        "Windows": ["shutdown", r"\h"]
    }

    run_shutdown = {
        "Darwin": ["osascript", "-e", "tell application \"System Events\" to shut down"],
        "Linux": ["systemctl", "poweroff"],
        "Windows": ["shutdown", r"\s"]
    }

    run_restart = {
        "Darwin": ["osascript", "-e", "tell application \"System Events\" to restart"],
        "Linux": ["systemctl", "reboot"],
        "Windows": ["shutdown", r"\r"]
    }

    run_logout = {
        "Darwin": ["osascript", "-e", "tell application \"System Events\" to log out"],
        "Linux": ["systemctl", "logout"],
        "Windows": ["shutdown", r"\l"]
    }

    match option:
        case "wakeup":
            subprocess.run(run_wakeup[platform.system()])
        case "sleep":
            subprocess.run(run_sleep[platform.system()])
        case "shutdown":
            subprocess.run(run_shutdown[platform.system()])
        case "restart":
            subprocess.run(run_restart[platform.system()])
        case "logout":
            subprocess.run(run_logout[platform.system()])
        case _:
            await ctx.bot.send_message(chat_id=update.effective_chat.id, text=get_help_options(), parse_mode="MarkdownV2")
