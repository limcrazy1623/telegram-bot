import telebot
import requests
import random
import os
import json
import re
from datetime import datetime
import schedule
import time
import threading
import pytz

TOKEN = "7973266839:AAF5VPoQvApooSpPtCaqJUl0Iqdu16lfFJg"
bot = telebot.TeleBot(TOKEN)

# Link AppScript để lấy báo cáo từ Google Sheets
APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyHVTygxz9HgTgpq8KfHO2bcsE9j3IoV3mk1kFBwbl35qmRTLKvi7nEvrXrj09nzsGUsA/exec"

print("Bot đang chạy...")

# Xử lý lệnh /start và /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Chào sếp! Nhập /baocao để nhận báo cáo.")

# Xử lý lệnh /baocao để lấy báo cáo từ Google Sheets
@bot.message_handler(commands=['baocao'])
def send_report(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "📊 Đang tạo báo cáo, vui lòng chờ...")

    try:
        response = requests.get(APP_SCRIPT_URL)
        bot.send_message(chat_id, f"📢 Báo cáo: {response.text}")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Lỗi: {str(e)}")

# Danh sách bài học Kinh Thánh theo ngày
lessons = {
    "20-3-2025": "Người Giàu Vào Nước Thiên Đàng?",
    "21-3-2025": "Theo Chúa Sẽ Được Chỉ?",
    "22-3-2025": "Lòng Thương Xót Của Chúa",
    "23-3-2025": "Trở Nên Khôn Ngoan",
    "24-3-2025": "Nguồn cậy Trông Của Tôi",
    "25-3-2025": "Chúa Chẳng Bao Giờ Từ Bỏ",
    "26-3-2025": "Thực Hành Lời Chúa",
    "27-3-2025": "Làm Thầy",
    "28-3-2025": "Quyền Của Lưỡi",
    "29-3-2025": "Công Dân Sống Đẹp Lòng Chúa",
    "30-3-2025": "Tiếp Nhận và Thực Hành Sự Khôn Ngoan",
    "31-3-2025": "Nhận Biệt Để Sống Xứng Đáng"
}

FACEBOOK_LINK = "https://www.facebook.com/BaiHocKinhThanhHangNgay/?locale=vi_VN"

@bot.message_handler(commands=['homnay'])
def send_today_lesson(message):
    today = datetime.today().strftime('%-d-%-m-%Y')
    lesson = lessons.get(today, "Hôm nay không có bài học.")
    response = f"📖 *Bài học Kinh Thánh Hằng Ngày hôm nay ({today}):*\n➡️ {lesson}\n\n🔗 Xem chi tiết tại: [Facebook]({FACEBOOK_LINK})"
    
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text.strip().count('-') == 2)
def send_lesson_by_text(message):
    date_requested = message.text.strip()
    lesson = lessons.get(date_requested, "Không có bài học cho ngày này.")
    response = f"📖 Bài học Kinh Thánh Hằng Ngày hôm nay ({date_requested}):\n➡️ {lesson}"
    
    bot.reply_to(message, response)

# Định nghĩa múi giờ Việt Nam
tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')

# Hàm gửi bài học tự động hàng ngày
def send_daily_lesson():
    today = datetime.now().strftime('%-d-%-m-%Y')
    lesson = lessons.get(today, "Hôm nay không có bài học.")
    chat_id = '6416693025'
    bot.send_message(chat_id, f"📖 Bài học Kinh Thánh Hằng Ngày ({today}): {lesson}")

# Đặt lịch gửi thông báo hàng ngày vào lúc 5h00 sáng
schedule.every().day.at("22:00").do(send_daily_lesson)

# Lệnh tìm câu Kinh Thánh
def find_bible_verse(book, chapter, verse):
    with open("kinh_thanh_updated.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    found_book = False
    found_chapter = False
    found_verse = False
    verse_text = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.lower() == book.lower():
            found_book = True
            found_chapter = False
            continue

        if found_book and line.lower() == f"chương {chapter}".lower():
            found_chapter = True
            continue

        if found_chapter:
            parts = line.split(" ", 1)
            if len(parts) > 1 and parts[0].isdigit() and int(parts[0]) == verse:
                found_verse = True
                verse_text = parts[1]
                continue

            if found_verse:
                if line[0].isdigit():
                    break
                verse_text += " " + line

    return f"{book} {chapter}:{verse} {verse_text}" if found_verse else "Không tìm thấy câu Kinh Thánh này."

@bot.message_handler(commands=['bible'])
def get_bible_verse(message):
    try:
        query = message.text.replace('/bible ', '').strip()
        parts = query.split(" ")

        if len(parts) < 2 or ":" not in parts[1]:
            bot.reply_to(message, "Vui lòng nhập theo định dạng: /bible Sách Chương:Câu\nVí dụ: /bible Thi-thiên 23:1")
            return

        book = parts[0]
        chapter, verse = map(int, parts[1].split(":"))
        verse_text = find_bible_verse(book, chapter, verse)

        bot.reply_to(message, f"📖 {verse_text}")
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")

import requests
import json

TOKEN = "7973266839:AAF5VPoQvApooSpPtCaqJUl0Iqdu16lfFJg"
bot = telebot.TeleBot(TOKEN)

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyHVTygxz9HgTgpq8KfHO2bcsE9j3IoV3mk1kFBwbl35qmRTLKvi7nEvrXrj09nzsGUsA/exec"

@bot.message_handler(regexp=r"doanh thu tháng (\d+)")
def get_revenue(message):
    chat_id = message.chat.id
    match = re.search(r"(\d+)", message.text)
    if match:
        month = match.group(1)
        bot.send_message(chat_id, f"📊 Đang tính toán doanh thu tháng {month}...")
        
        try:
            response = requests.get(f"{APP_SCRIPT_URL}?month={month}")
            data = response.json()
            reply = (f"Vâng! Thưa Sếp\n"
                     f"📅 Doanh thu tháng {month}:\n"
                     f"💰 Tổng tiền: {data['tong_tien']}\n"
                     f"🖨️ Tiền in: {data['tien_in']}\n"
                     f"💵 Tiền lời: {data['tien_loi']}")
            bot.send_message(chat_id, reply)
        except Exception as e:
            bot.send_message(chat_id, f"❌ Lỗi: {str(e)}")

# Chạy đồng thời bot và schedule
def run_schedule_and_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule_thread = threading.Thread(target=run_schedule_and_bot)
schedule_thread.start()

# Chạy bot polling
bot.polling(none_stop=True, interval=3, timeout=30)
