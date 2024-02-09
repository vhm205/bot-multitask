import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from handlers.finance.stock import stock_reply_handler
from handlers.finance.leadership import leadership_reply_handler, leadership_detail_handler
from handlers.finance.insider_tx import insider_tx_reply_handler
from handlers.finance.shareholder import shareholder_reply_handler
from handlers.finance.news import news_reply_handler
from handlers.finance.report import report_reply_handler

menu = [
    ["price", "leadership", "insider TX"],
    ["shareholder", "news", "report"]
]
reply_markup = ReplyKeyboardMarkup(menu, one_time_keyboard=True)

OPTION, STOCK_CODE, LEADER_SHIP, INSIDER_TX, SHAREHOLDER, NEWS, REPORT = range(7)

async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, I'm a bot, please choose the options below:\n"
        "Send 'done' to stop talking to me.\n",
        reply_markup=reply_markup
    )

    return OPTION

async def option_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    await update.message.reply_text(
        "Please send me stock code or send 'done' to stop talking to me.\n",
        reply_markup=ReplyKeyboardRemove()
    )

    match message:
        case "price":
            return STOCK_CODE
        case "leadership":
            return LEADER_SHIP
        case "insider TX":
            return INSIDER_TX
        case "shareholder":
            return SHAREHOLDER
        case "news":
            return NEWS
        case "report":
            return REPORT

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.full_name)

    user_data = ctx.user_data
    if 'stock_code' in user_data:
        del user_data['stock_code']

    user_data.clear()
    await update.message.reply_text("Bye!")
    return ConversationHandler.END

def finance_command_handler(app: Application):
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('stock', start_handler)],
        states={
            OPTION: [
                MessageHandler(filters.TEXT, option_reply_handler),
            ],
            STOCK_CODE: [MessageHandler(filters.TEXT, stock_reply_handler)],
            LEADER_SHIP: [
                MessageHandler(filters.Regex(r'^\d+$') & ~filters.COMMAND, leadership_detail_handler),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex(r'^done$')), leadership_reply_handler)
            ],
            INSIDER_TX: [MessageHandler(filters.TEXT, insider_tx_reply_handler)],
            SHAREHOLDER: [MessageHandler(filters.TEXT, shareholder_reply_handler)],
            NEWS: [MessageHandler(filters.TEXT, news_reply_handler)],
            REPORT: [MessageHandler(filters.TEXT, report_reply_handler)],
        },
        fallbacks=[MessageHandler(filters.Regex(r'^done$'), cancel)],
    )

    app.add_handler(conversation_handler)
