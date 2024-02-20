import json
import requests
import logging
# import prettytable as pt
from helpers.utils import format_number
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# stock_info_other_table = pt.PrettyTable([
#     "Exchange", "Stock code"
# ])

def get_stock_price(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/historical/quote/{stock_code}")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data, None

def get_stock_period(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/historical/prices/hl?ticker={stock_code}&period=1y")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data, None

async def stock_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text
        logging.info("Stock message %s", message)
        result, msg = get_stock_price(message)
        stock_period, _ = get_stock_period(message)

        if result is None:
            return await update.message.reply_text(msg)

        vndirect_enterprise_profile = f"https://dstock.vndirect.com.vn/ho-so-doanh-nghiep/{message.upper()}"
        simplize_enterprise_profile = f"https://simplize.vn/co-phieu/{message.upper()}/ho-so-doanh-nghiep"
        message_reply = ""

        stock_price = [
            "<b>Thông tin cổ phiếu</b>",
            f"Giá đóng cửa: {format_number(result['priceClose'])}",
            f"Giá mở cửa: {format_number(result['priceOpen'])}",
            f"Giá cao nhất: {format_number(result['priceHigh'])}",
            f"Giá thấp nhất: {format_number(result['priceLow'])}",
            f"Giá trần: {format_number(result['priceCeiling'])}",
            f"Giá sàn: {format_number(result['priceFloor'])}",
            f"Giá tham chiếu: {format_number(result['priceReference'])}",
            f"Giá trung bình: {format_number(result['priceAverage'])}",
            f"Giá trị thay đổi: {format_number(result['netChange'], False)}",
            f"Phần trăm thay đổi: {result['pctChange']:.2f}%",
            f"Khối lượng giao dịch: {format_number(result['totalVolume'])}",
            f"Khối lượng mua: {format_number(result['totalBuyVolume'])}",
            f"Khối lượng bán: {format_number(result['totalSellVolume'])}",
        ]

        if stock_period is not None:
            stock_price += [
                f"Giá cao nhất 1 năm: {format_number(stock_period['high'])}",
                f"Giá thấp nhất 1 năm: {format_number(stock_period['low'])}",
            ]

        stock_price += [
            "---------",
            "<b>Tham khảo</b>",
            f"<a href='{vndirect_enterprise_profile}'>VnDirect</a>",
            f"<a href='{simplize_enterprise_profile}'>Simplize</a>"
        ]

        for item in stock_price:
            message_reply += f"• {item}\n"

        await update.message.reply_text(message_reply, parse_mode="HTML")

        # name = result['name']
        # ticker = result['ticker']
        # stock_exchange = result['stockExchange']
        # industryActivity = result['industryActivity']
        # outstandingSharesValue = "{:,}".format(result['outstandingSharesValue'])
        # volume = "{:,}".format(result['volume'])
        # market_cap = "{:,}".format(result['marketCap'])
        # price_close = "{:,}".format(result['priceClose'])
        # price_high = "{:,}".format(result['priceHigh'])
        # price_low = "{:,}".format(result['priceLow'])
        # price_referrance = "{:,}".format(result['priceReferrance'])
        # price_change = result['pctChange']
        # book_value = "{:,}".format(result['bookValue'])
        # eps_ratio = "{:,}".format(result['epsRatio'])
        # pe_ratio = result['peRatio']
        # pb_ratio = result['pbRatio']
        # roe = result['roe']
        # roa = result['roa']
        # date_updated = result['analysisUpdated']
        # website = result['website']
        # vndirect_enterprise_profile = f"https://dstock.vndirect.com.vn/ho-so-doanh-nghiep/{ticker}"
        # simplize_enterprise_profile = f"https://simplize.vn/co-phieu/{ticker}/ho-so-doanh-nghiep"
        # message_stock_reply = ""

        # stock_info_other = [(stock_exchange, ticker)]

        # stock_info = [
        #     f"Tên: <a href='{website}'>{name}</a>",
        #     f"Lĩnh vực: {industryActivity}",
        #     f"Lưu hành: {outstandingSharesValue}",
        #     f"Volume: {volume}",
        #     f"Market cap: {market_cap}",
        #     f"Close: {price_close}",
        #     f"High: {price_high}",
        #     f"Low: {price_low}",
        #     f"Reference: {price_referrance}",
        #     f"Change: {price_change}%",
        #     f"Book value: {book_value}",
        #     f"EPS: {eps_ratio}",
        #     f"P/E: {pe_ratio}",
        #     f"P/B: {pb_ratio}",
        #     f"ROE: {roe:.2f}",
        #     f"ROA: {roa:.2f}",
        #     f"<b><i>Cập nhật lúc: {date_updated}</i></b>",
        #     "---------",
        #     "<b>Tham khảo</b>",
        #     f"<a href='{vndirect_enterprise_profile}'>VnDirect</a>",
        #     f"<a href='{simplize_enterprise_profile}'>Simplize</a>"
        # ]

        # for item in stock_info_other:
        #     stock_info_other_table.add_row(list(item))

        # for item in stock_info:
        #     message_stock_reply += f"• {item}\n"

        # await update.message.reply_text(f"```{stock_info_other_table}```", parse_mode="MarkdownV2")
        # await update.message.reply_text(f"<b>Thông tin cổ phiếu</b>\n{message_stock_reply}", parse_mode="HTML")

        # stock_info_other_table.clear_rows()
        return ConversationHandler.END
    except Exception as e:
        logging.exception(e)
