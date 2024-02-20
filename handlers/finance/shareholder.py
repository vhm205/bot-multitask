import json
import requests
import logging
import prettytable as pt
from numerize.numerize import numerize
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

shareholder_table = pt.PrettyTable([
    "ID", "Share held", "Current Value", "Change"
])

def get_shareholder_info(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/ownership/shareholder-fund-details/{stock_code}")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    shareholders = data['shareholderDetails'][0:10]
    fund_holdings = data['fundHoldings'][0:10]
    return shareholders, fund_holdings

async def shareholder_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Shareholder message %s", message)
    shareholders, msg = get_shareholder_info(message)

    if shareholders is None:
        return await update.message.reply_text(msg)

    message_shareholder_reply = "<b>Tên | Quốc tịch | Tỷ lệ sở hữu</b>\n"

    for i, shareholder in enumerate(shareholders):
        message_shareholder_reply += '---------\n'
        message_shareholder_reply += f"{i + 1}) {shareholder['investorFullName']} | {shareholder['countryOfInvestor']} | {shareholder['pctOfSharesOutHeld']}%\n"
        shareholder_table.add_row([
            i + 1,
            numerize(shareholder['sharesHeld']),
            numerize(shareholder['currentValue']),
            numerize(shareholder['changeValue']),
        ])

    await update.message.reply_text(f"{message_shareholder_reply}", parse_mode="HTML")
    await update.message.reply_text(f"<pre>{shareholder_table}</pre>", parse_mode="HTML")

    return ConversationHandler.END
