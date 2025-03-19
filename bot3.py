import time
import schedule
import telebot
import random
import requests
from datetime import datetime

TOKEN = "7973266839:AAF5VPoQvApooSpPtCaqJUl0Iqdu16lfFJg"
bot = telebot.TeleBot(TOKEN)

# Link AppScript để lấy báo cáo từ Google Sheets
APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyHVTygxz9HgTgpq8KfHO2bcsE9j3IoV3mk1kFBwbl35qmRTLKvi7nEvrXrj09nzsGUsA/exec"

print("Bot đang chạy...")

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

# Xử lý lệnh /start và /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(f"Đã nhận lệnh: {message.text}")  # Log lệnh nhận được
    bot.reply_to(message, "Chào sếp! Nhập /baocao để nhận báo cáo hoặc /homnay để nhận bài học hôm nay.")

# Xử lý lệnh /baocao để lấy báo cáo từ Google Sheets
@bot.message_handler(commands=['baocao'])
def send_report(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "📊 Đang tạo báo cáo, vui lòng chờ...")

    print(f"Đã nhận lệnh: {message.text}")  # Log lệnh nhận được
    
    try:
        response = requests.get(APP_SCRIPT_URL)
        bot.send_message(chat_id, f"📢 Báo cáo: {response.text}")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Lỗi: {str(e)}")

# Danh sách câu Kinh Thánh động viên
BIBLE_VERSES = [
    "Ta làm được mọi sự nhờ Đấng ban thêm sức cho ta. – Phi-líp 4:13",
    "Hãy giao phó công việc mình cho Đức Giê-hô-va, thì những mưu kế con sẽ được thành công. – Châm Ngôn 16:3",
    "Chớ mệt nhọc trong việc lành, vì đến kỳ ta sẽ gặt, nếu ta không ngã lòng. – Ga-la-ti 6:9",
    "Hãy vững lòng, mạnh mẽ! Đừng sợ, đừng kinh hãi, vì Giê-hô-va Đức Chúa Trời của con sẽ đi cùng con. – Phục Truyền 31:6",
    "Nhưng ai trông đợi Đức Giê-hô-va thì được thêm sức mới; họ cất cánh bay cao như chim ưng, chạy mà không mệt nhọc, đi mà không mòn mỏi. – Ê-sai 40:31",
    "Ta há chẳng truyền dạy con sao? Hãy mạnh mẽ, can đảm chớ run sợ; vì Giê-hô-va Đức Chúa Trời của con sẽ ở cùng con trong mọi việc con làm. – Giô-suê 1:9",
    "Chúa sẽ chiến đấu cho anh em, còn anh em cứ yên lặng. – Xuất Ê-díp-tô Ký 14:14",
    "Hãy trông cậy Đức Giê-hô-va hết lòng, chớ nương cậy nơi sự thông sáng của con. – Châm Ngôn 3:5",
    "Kẻ nào làm việc chăm chỉ sẽ được cai trị, còn ai lười biếng sẽ bị phục dịch. – Châm Ngôn 12:24",
    "Hãy đứng vững, chớ rúng động, hãy làm công việc Chúa cách dư dật luôn, vì biết rằng công khó của anh em trong Chúa chẳng phải là vô ích. – 1 Cô-rinh-tô 15:58"
]

# Hàm gửi bài học Kinh Thánh hằng ngày vào lúc 5h30 sáng
def send_daily_lesson():
    today = datetime.today().strftime('%d-%m-%Y')
    lesson = lessons.get(today, "Hôm nay không có bài học.")

    # Thay "YOUR_CHAT_ID" bằng ID của bạn
    chat_id = "6416693025"
    message = f"Vâng! Thưa Sếp, bài học hôm nay ({today}) là: {lesson}"
    bot.send_message(chat_id, message)

# Đặt lịch gửi thông báo hàng ngày vào lúc 5h30 sáng
schedule.every().day.at("05:30").do(send_daily_lesson)

# Hàm trả lời khi người dùng hỏi bài học hôm nay
@bot.message_handler(commands=['homnay'])
def send_today_lesson(message):
    print(f"Đã nhận lệnh: {message.text}")  # Log lệnh nhận được
    
    today = datetime.today().strftime('%d-%m-%Y')
    lesson = lessons.get(today, "Hôm nay không có bài học.")
    bot.reply_to(message, f"Vâng! Thưa Sếp, bài học hôm nay ({today}) là: {lesson}")

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
    print(f"Đã nhận tin nhắn: {message.text}")  # Log tin nhắn nhận được
    
    reply = random.choice(RANDOM_REPLIES)
    bot.reply_to(message, reply)

# Danh sách từ khóa cảm ơn
THANKS_MESSAGES = ["cảm ơn", "thanks", "tks", "thank you", "ok", "oke"]

@bot.message_handler(func=lambda message: message.text.lower() in THANKS_MESSAGES)
def thanks_reply(message):
    print(f"Đã nhận tin nhắn: {message.text}")  # Log tin nhắn nhận được
    
    bot.reply_to(message, "Không có chi, đó là nhiệm vụ của em. Chúc Sếp làm việc vui vẻ! 😃")

# Chạy bot và kiểm tra lịch gửi thông báo
def run_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_bot()
bot.polling(none_stop=True, interval=0)
