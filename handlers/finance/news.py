import logging
import json
import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from helpers.utils import remove_html_tags_regex

vneconomy_domain = "https://vneconomy.vn"

def get_news_vneconomy(code: str):
    stock_code = code.lower()
    response = requests.get(f'https://search.hemera.com.vn/search/1/{stock_code}/time/1')
    data = json.loads(response.content)
    count = data['Count']
    data = data['List']

    if count == 0:
        return None, "VNEconomy can't fetch data"

    return data[0:10], None

def get_news(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/news-event/list?ticker={stock_code}&isWl=false&page=0&size=10")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data, None

def get_news_company(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/events/list?ticker={stock_code}&type=3&page=0&size=12")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data, None

def get_events(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/events/list?ticker={stock_code}&isWl=false&page=0&size=5")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data, None

async def news_reply_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text
        logging.info("News message %s", message)
        news, msg_news = get_news(message)
        news_company, msg_news_company = get_news_company(message)
        events, msg_events = get_events(message)
        news_vneconomy, msg_news_vneconomy = get_news_vneconomy(message)

        # NEWS VNECONOMY
        if news_vneconomy is None:
            return await update.message.reply_text(msg_news_vneconomy)

        message_news_vneconomy_reply = "<b>VN Economy</b>\n"
        for item in news_vneconomy:
            print(item)
            title = remove_html_tags_regex(item['Title'])
            slug = item['UrlArticle']
            message_news_vneconomy_reply += f"<a href='{vneconomy_domain}/{slug}'>{title}</a>\n"
            message_news_vneconomy_reply += "---------\n"

        await update.message.reply_text(message_news_vneconomy_reply, parse_mode="HTML")

        # NEWS
        if news is None:
            return await update.message.reply_text(msg_news)

        message_news_reply = "<b>Tin tức</b>\n"
        for item in news:
            message_news_reply += f"<a href='https://api.simplize.vn/api/company/news-event/detail/{item['id']}'>{item['title']}</a>\n"
            message_news_reply += "---------\n"

        await update.message.reply_text(message_news_reply, parse_mode="HTML")

        # NEWS COMPANY
        if news_company is None:
            return await update.message.reply_text(msg_news_company)

        message_news_company_reply = "<b>Tin tức công ty</b>\n"
        for item in news_company:
            message_news_company_reply += f"<a href='{item['attachedLink']}'>{item['title']}</a>\n"
            message_news_company_reply += "---------\n"

        await update.message.reply_text(message_news_company_reply, parse_mode="HTML")

        # EVENTS
        if events is None:
            return await update.message.reply_text(msg_events)

        message_events_reply = "<b>Sự kiện</b>\n"
        for item in events:
            message_events_reply += f"<a href='{item['attachedLink']}'>{item['title']}</a>\n"
            message_events_reply += "---------\n"

        await update.message.reply_text(message_events_reply, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(e.args[0])
    finally:
        return ConversationHandler.END
