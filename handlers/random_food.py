import requests
import json
import random
from telegram import Update
from telegram.ext import ContextTypes

foody_domain = "https://www.foody.vn"
foods = ["Phở", "Bánh canh", "Hủ tíu", "Bánh mi", "Mì hoành thánh", "Bò né", "Bún bò", "Cơm tấm"]

def get_foods(term: str):
    response = requests.get(f"https://www.foody.vn/__get/AutoComplete/Keywords?provinceId=217&term={term}")
    data = json.loads(response.content)
    return data

async def random_food_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        term = random.choice(foods)
        result = get_foods(term)
        del result[0];

        data = random.choice(result)

        name = data['name']
        thumb = data['img']
        thumb = thumb.replace("s50", "s640")
        link = data['link']
        address = data['address']
        isOpen = data['isOpening']
        openStatus = "Mở cửa" if isOpen else "Đóng cửa"
        await ctx.bot.send_photo(chat_id=update.effective_chat.id, photo=thumb, caption=f"{name}\n- Địa chỉ: {address}\n- Link: {foody_domain}{link}\n- Trạng thái: {openStatus}")
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
