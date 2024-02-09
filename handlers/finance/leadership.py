import logging
import requests
import json
import asyncio
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from helpers.utils import format_number

LEADER_SHIP = 2

def get_list_leadership(code: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/management/bod-member/{stock_code}")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data, None

def get_leadership_detail(code: str, id: str):
    stock_code = code.upper()
    response = requests.get(f"https://api.simplize.vn/api/company/management/bod-member-detail/{stock_code}/{id}")
    data = json.loads(response.content)
    status = data['status']
    data = data['data']

    if status != 200 or data is None:
        return None, data['message']

    return data, None

async def leadership_detail_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    ticker = ctx.user_data['stock_code']
    result, msg = get_leadership_detail(ticker, message)

    if result is None:
        return await update.message.reply_text(msg)

    message_basic_info_reply = "<b>Thông tin ban lãnh đạo</b>\n"
    message_basic_info_reply += f"ID: {result['id']}\n"
    message_basic_info_reply += f"Tên: {result['fullName']}\n"

    if 'birthday' in result and result['birthday'] != "":
        message_basic_info_reply += f"Ngày sinh: {result['birthday']}\n"

    if 'identityCard' in result and result['identityCard'] != "":
        message_basic_info_reply += f"CMND: {result['identityCard']}\n"

    if 'placeOfOrgin' in result:
        message_basic_info_reply += f"Nguyên quán: {result['placeOfOrgin']}\n"

    if 'permannentAddress' in result:
        message_basic_info_reply += f"Cư trú: {result['permannentAddress']}\n"

    await update.message.reply_text(message_basic_info_reply, parse_mode="HTML")

    message_bod_current_holdings = "<b>Cổ phiếu đang nắm giữ</b>\n"
    message_bod_current_holdings += "--------\n"
    for bod in result['bodCurrentHoldings']:
        message_bod_current_holdings += f"Mã CP: <b>{bod['ticker']}</b>\n"
        message_bod_current_holdings += f"Số lượng: {format_number(bod['quantity'])}\n"
        message_bod_current_holdings += f"Tỷ lệ: {bod['rate']}%\n"
        message_bod_current_holdings += f"Tính đến ngày: {bod['toDate']}\n"
        message_bod_current_holdings += f"Giá trị: {format_number(bod['value'])}\n"
        await update.message.reply_text(message_bod_current_holdings, parse_mode="HTML")
        message_bod_current_holdings = ""

    await update.message.reply_text("--------------------")

    message_roles_current = "<b>Chức vụ hiện tại</b>\n"
    message_roles_current += "--------\n"
    for role in result['bodRoles']:
        message_roles_current += f"Vị trí: {role['name']}\n"
        message_roles_current += f"Tổ chức: {role['companyName']}\n"
        if role['startDate'] != "":
            message_roles_current += f"Thời gian bổ nhiệm: {role['startDate']}\n"
        await update.message.reply_text(message_roles_current, parse_mode="HTML")
        message_roles_current = ""

    await update.message.reply_text("--------------------")

    message_relationships = "<b>Gia đình</b>\n"
    message_relationships += "--------\n"
    for people in result['bodRelationships']:
        message_relationships += f"Tên: {people['fullName']}\n"
        message_relationships += f"Mối quan hệ: {people['relationship']}\n"
        message_relationships += f"Mã CP: <b>{people['ticker']}</b>\n"
        message_relationships += f"CP nắm giữ: {format_number(people['quantity'])}\n"
        message_relationships += f"Giá trị CP: {format_number(people['value'])}\n"
        message_relationships += f"Tính đến ngày: {people['toDate']}\n"
        await update.message.reply_text(message_relationships, parse_mode="HTML")
        message_relationships = ""

    ref = f"https://simplize.vn/co-phieu/{ticker}/ho-so-doanh-nghiep#ban-lanh-dao"
    await update.message.reply_text(f"Tham khảo: \n<a href='{ref}'>Simplize</a>", parse_mode="HTML")

    await update.message.reply_text(
        "Please send me ID of leadership for get detail or send 'done' to stop talking to me.\n",
        reply_markup=ReplyKeyboardRemove()
    )
    return LEADER_SHIP

async def leadership_reply_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logging.info("Leadership message %s", message)
    result, msg = get_list_leadership(message)

    if result is None:
        return await update.message.reply_text(msg)

    ctx.user_data['stock_code'] = message

    ceo = result['ceo']
    members = result['boards']['members']
    manager = result['management']['members']

    message_ceo_reply = "<b>CEO</b>\n"
    message_members_reply = "<b>Hội đồng quản trị</b>\n"
    message_manager_members_reply = "<b>Ban kiểm soát</b>\n"

    if ceo != "":
        message_ceo_reply += f"ID: {ceo['id']}\n"
        message_ceo_reply += f"Tên: {ceo['fullName']}\n"
        message_ceo_reply += f"Chức vụ: {ceo['roleName']}\n"
        message_ceo_reply += f"Số năm đương nhiệm: <b>{ceo['tenure']} năm</b>\n"

    for member in members:
        message_members_reply += f"ID: {member['id']}\n"
        message_members_reply += f"Tên: {member['fullName']}\n"
        message_members_reply += f"Chức vụ: {member['roleName']}\n"
        message_members_reply += f"Số năm đương nhiệm: <b>{member['tenure']} năm</b>\n"
        message_members_reply += "---------\n"

    for member in manager:
        message_manager_members_reply += f"ID: {member['id']}\n"
        message_manager_members_reply += f"Tên: {member['fullName']}\n"
        message_manager_members_reply += f"Chức vụ: {member['roleName']}\n"
        message_manager_members_reply += f"Số năm đương nhiệm: <b>{member['tenure']} năm</b>\n"
        message_manager_members_reply += "---------\n"

    await update.message.reply_text(message_ceo_reply, parse_mode="HTML")
    await update.message.reply_text(message_members_reply, parse_mode="HTML")
    await update.message.reply_text(message_manager_members_reply, parse_mode="HTML")

    await update.message.reply_text(
        "Please send me ID of leadership or send 'done' to stop talking to me.\n",
        reply_markup=ReplyKeyboardRemove()
    )

    return LEADER_SHIP
