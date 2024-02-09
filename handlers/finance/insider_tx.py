import logging
import requests
import json
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

async def get_insider_tx(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/ownership/insider-transactions/{stock_code}")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data[:10], None

async def insider_tx_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Insider Tx message %s", message)
    result, msg = await get_insider_tx(message)
    message_reply = "<b>Thông tin giao dịch nội bộ</b>\n"

    if result is None:
        return await update.message.reply_text(msg)

    for tx in result:
        traded_date = tx['tradedDate']
        is_buy = tx['isBuy']
        insider_name = tx['insiderName']
        insider_position = tx['insiderOccupation']
        stock_total = tx['result']
        value = tx['value']
        average_price = tx['averagePrice']
        tx_type = "Mua" if is_buy else "Bán"

        message_reply += f"- <u>{traded_date}</u>:\n"
        message_reply += f"Người giao dịch: {insider_name}\n"
        if insider_position != "":
            message_reply += f"Chức vụ: {insider_position}\n"
        message_reply += f"Loại: <strong>{tx_type}</strong>\n"
        message_reply += f"Lượng cổ phiếu: {'{:,}'.format(stock_total).rstrip('0').rstrip('.')}\n"
        message_reply += f"Giá trị: {'{:,}'.format(value).rstrip('0').rstrip('.')}\n"
        message_reply += f"Giá sau điều chỉnh: {'{:,}'.format(average_price).rstrip('0').rstrip('.')}\n"
        message_reply += '------------\n'

    await update.message.reply_text(f"{message_reply}", parse_mode="HTML")
    return ConversationHandler.END
