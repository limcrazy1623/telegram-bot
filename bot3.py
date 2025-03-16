import telebot
import requests
import random
import os

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

# Danh sách câu trả lời ngẫu nhiên
RANDOM_REPLIES = [
    "Dạ sếp, em có thể giúp gì ạ? 😊",
    "Chào sếp! Hôm nay có gì cần em hỗ trợ không? 😃",
    "Sếp ơi, em sẵn sàng giúp đây! 🚀",
    "Em đây, sếp cần gì cứ bảo nhé! 💪",
]

# Danh sách từ khóa tin nhắn đơn giản
SIMPLE_MESSAGES = ["alo", "hi", "hello", "ê", "chào", "ok", "hê"]

@bot.message_handler(func=lambda message: message.text.lower() in SIMPLE_MESSAGES)
def random_reply(message):
    reply = random.choice(RANDOM_REPLIES)
    bot.reply_to(message, reply)

# Danh sách từ khóa cảm ơn
THANKS_MESSAGES = ["cảm ơn", "thanks", "tks", "thank you", "ok", "oke"]

@bot.message_handler(func=lambda message: message.text.lower() in THANKS_MESSAGES)
def thanks_reply(message):
    bot.reply_to(message, "Không có chi, đó là nhiệm vụ của em. Chúc Sếp làm việc vui vẻ! 😃")

bot.polling(none_stop=True, interval=0)
