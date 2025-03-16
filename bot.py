import telebot
import requests
import time

TOKEN = "7973266839:AAF5VPoQvApooSpPtCaqJUl0Iqdu16lfFJg"  # Thay bằng token bot của bạn
CHAT_ID = "6416693025"  # Thay bằng ID chat của bạn
APP_SCRIPT_URL = "YOUR_APP_SCRIPT_URL"  # Thay bằng URL App Script của bạn

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Xin chào! Gõ /baocao để nhận báo cáo công việc hôm nay.")

@bot.message_handler(commands=['baocao'])
def send_report(message):
    bot.send_message(CHAT_ID, "📊 Đang tạo báo cáo, vui lòng chờ...")
    
    try:
        response = requests.get(APP_SCRIPT_URL)
        report = response.text
        bot.send_message(CHAT_ID, report)
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ Lỗi khi lấy báo cáo: {e}")

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Lỗi: {e}")
            time.sleep(10)  # Chờ 10s rồi thử lại
