import asyncio
import logging
import requests
import json
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

async def get_reports(code: str, type: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/documents/list?ticker={stock_code}&type={type}&page=0&size=9")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data

async def report_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Report message %s", message)
    result_bctc = get_reports(message, 'BCTC')
    result_bctn = get_reports(message, 'BCTN')
    result_bcb = get_reports(message, 'BCB')
    result_nqdhcd = get_reports(message, 'NQDHCD')

    [bcb, bctn, bctc, nqdhcd] = await asyncio.gather(result_bcb, result_bctn, result_bctc, result_nqdhcd)

    message_bctc_reply = "<b>Báo cáo tài chính</b>\n"
    message_bctn_reply = "<b>Báo cáo thường niên</b>\n"
    message_bcb_reply = "<b>Báo cáo bạch</b>\n"
    message_nqdhcd_reply = "<b>Nghị quyết đại hội đồng cổ đông</b>\n"

    for item in bctc:
        issue_date = item['issueDate']
        link = item['attachedLink']
        title = item['title']
        message_bctc_reply += f"- {issue_date}: <a href='{link}'>{title}</a>\n"

    for item in bctn:
        issue_date = item['issueDate']
        link = item['attachedLink']
        title = item['title']
        message_bctn_reply += f"- {issue_date}: <a href='{link}'>{title}</a>\n"

    for item in bcb:
        issue_date = item['issueDate']
        link = item['attachedLink']
        title = item['title']
        message_bcb_reply += f"- {issue_date}: <a href='{link}'>{title}</a>\n"

    for item in nqdhcd:
        issue_date = item['issueDate']
        link = item['attachedLink']
        title = item['title']
        message_nqdhcd_reply += f"- {issue_date}: <a href='{link}'>{title}</a>\n"

    await update.message.reply_html(message_bctc_reply)
    await update.message.reply_html(message_bctn_reply)
    await update.message.reply_html(message_bcb_reply)
    await update.message.reply_html(message_nqdhcd_reply)

    return ConversationHandler.END
