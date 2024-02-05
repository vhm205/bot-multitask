import logging
import requests
import json
import prettytable as pt
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

menu = [
    ["stock", "leadership", "news"]
]
reply_markup = ReplyKeyboardMarkup(menu, one_time_keyboard=True)

OPTION, STOCK_CODE, LEADER_SHIP, NEWS = range(4)

stock_info_other_table = pt.PrettyTable([
    "Exchange", "Stock code"
])

# https://api.simplize.vn/api/historical/quote/FPT
async def get_stock_price(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://simplize.vn/_next/data/PdMOX-JEefrCh5GFA2cvs/co-phieu/{stock_code}/so-lieu-tai-chinh.json?ticker={stock_code}")
    data = json.loads(response.content)
    pageProps = data['pageProps']
    summary = pageProps['summary']
    return summary

async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, I'm a bot, please choose the options below:\n"
        "Send /cancel to stop talking to me.\n",
        reply_markup=reply_markup
    )

    return OPTION

async def option_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    await update.message.reply_text(
        "Please send me stock code or press /cancel to stop talking to me.\n",
    )

    match message:
        case "stock":
            return STOCK_CODE
        case "leadership":
            return LEADER_SHIP
        case "news":
            return NEWS

# HANDLE STOCK REPLY
async def stock_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Stock message %s", message)
    result = await get_stock_price(message)

    name = result['name']
    industryActivity = result['industryActivity']
    outstandingSharesValue = "{:,}".format(result['outstandingSharesValue'])
    volume = "{:,}".format(result['volume'])
    market_cap = "{:,}".format(result['marketCap'])
    price_close = "{:,}".format(result['priceClose'])
    price_high = "{:,}".format(result['priceHigh'])
    price_low = "{:,}".format(result['priceLow'])
    price_referrance = "{:,}".format(result['priceReferrance'])
    price_change = result['pctChange']
    book_value = "{:,}".format(result['bookValue'])
    eps_ratio = "{:,}".format(result['epsRatio'])
    pe_ratio = result['peRatio']
    pb_ratio = result['pbRatio']
    roe = result['roe']
    roa = result['roa']
    date_updated = result['analysisUpdated']
    website = result['website']
    message_stock_reply = ""

    stock_info_other = [(
        result['stockExchange'],
        result['ticker'],
    )]

    stock_info = [
        f"Tên: <a href='{website}'>{name}</a>",
        f"Lĩnh vực: {industryActivity}",
        f"Lưu hành: {outstandingSharesValue}",
        f"Volume: {volume}",
        f"Market cap: {market_cap}",
        f"Close: {price_close}",
        f"High: {price_high}",
        f"Low: {price_low}",
        f"Reference: {price_referrance}",
        f"Change: {price_change}%",
        f"Book value: {book_value}",
        f"EPS: {eps_ratio}",
        f"P/E: {pe_ratio}",
        f"P/B: {pb_ratio}",
        f"ROE: {roe:.2f}",
        f"ROA: {roa:.2f}",
        f"<b><i>Cập nhật lúc: {date_updated}</i></b>",
    ]

    for item in stock_info_other:
        stock_info_other_table.add_row(list(item))

    for item in stock_info:
        message_stock_reply += f"• {item}\n"

    await update.message.reply_text(f"```{stock_info_other_table}```", parse_mode="MarkdownV2")
    await update.message.reply_text(f"<b>Thông tin cổ phiếu</b>\n{message_stock_reply}", parse_mode="HTML")

    stock_info_other_table.clear_rows()
    return ConversationHandler.END

# HANDLE LEADER SHIP REPLY
async def leadership_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Leadership message %s", message)
    return ConversationHandler.END

# HANDLE NEWS REPLY
async def news_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("News message %s", message)
    return ConversationHandler.END

async def cancel(update: Update, _: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.full_name)
    await update.message.reply_text("Bye!")
    return ConversationHandler.END

def finance_command_handler(app: Application):
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('finance', start_handler)],
        states={
            OPTION: [
                MessageHandler(filters.TEXT, option_reply_handler),
            ],
            STOCK_CODE: [MessageHandler(filters.TEXT, stock_reply_handler)],
            LEADER_SHIP: [MessageHandler(filters.TEXT, leadership_reply_handler)],
            NEWS: [MessageHandler(filters.TEXT, news_reply_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conversation_handler)
