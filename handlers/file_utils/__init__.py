import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from handlers.file_utils.convert_file import choose_output_extension, convert_file_handler

menu = [
    ["convert", "compress"],
]
reply_markup = ReplyKeyboardMarkup(menu, one_time_keyboard=True)

OPTION, CONVERT, COMPRESS = range(3)

async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, I'm a bot, please choose the options below:\n"
        "Send 'done' to stop talking to me.\n",
        reply_markup=reply_markup
    )

    return OPTION

async def option_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    reply_text = "Please send me a file or send 'done' to stop talking to me.\n"

    match message:
        case "convert":
            reply_text = "Please send me the file extension you want to convert (ex: pdf, doc).\n"
            await update.message.reply_text(
                reply_text,
                reply_markup=ReplyKeyboardRemove()
            )

            return CONVERT
        case "compress":
            await update.message.reply_text(
                reply_text,
                reply_markup=ReplyKeyboardRemove()
            )

            return COMPRESS

async def cancel(update: Update, _: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.full_name)

    await update.message.reply_text("Bye!")
    return ConversationHandler.END

def file_utils_command_handler(app: Application):
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('file', start_handler)],
        states={
            OPTION: [
                MessageHandler(filters.TEXT, option_reply_handler),
            ],
            CONVERT: [
                MessageHandler(filters.Regex(r'(\w+)$'), choose_output_extension),
                MessageHandler(filters.Document.ALL, convert_file_handler),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex(r'^done$'), cancel)],
    )

    app.add_handler(conversation_handler)
