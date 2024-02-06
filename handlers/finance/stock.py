import json
import requests
import logging
import prettytable as pt
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

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

# HANDLE STOCK REPLY
async def stock_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Stock message %s", message)
    result = await get_stock_price(message)

    name = result['name']
    ticker = result['ticker']
    stock_exchange = result['stockExchange']
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
    vndirect_enterprise_profile = f"https://dstock.vndirect.com.vn/ho-so-doanh-nghiep/{ticker}"
    simplize_enterprise_profile = f"https://simplize.vn/co-phieu/{ticker}/ho-so-doanh-nghiep"
    message_stock_reply = ""

    stock_info_other = [(stock_exchange, ticker)]

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
        "---------",
        "<b>Tham khảo</b>",
        f"<a href='{vndirect_enterprise_profile}'>VnDirect</a>",
        f"<a href='{simplize_enterprise_profile}'>Simplize</a>"
    ]

    for item in stock_info_other:
        stock_info_other_table.add_row(list(item))

    for item in stock_info:
        message_stock_reply += f"• {item}\n"

    await update.message.reply_text(f"```{stock_info_other_table}```", parse_mode="MarkdownV2")
    await update.message.reply_text(f"<b>Thông tin cổ phiếu</b>\n{message_stock_reply}", parse_mode="HTML")

    stock_info_other_table.clear_rows()
    return ConversationHandler.END
