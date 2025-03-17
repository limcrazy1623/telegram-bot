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

# Xử lý khi người dùng yêu cầu một câu Kinh Thánh
@bot.message_handler(func=lambda message: "khích lệ tôi bằng một câu kinh thánh" in message.text.lower())
def send_bible_verse(message):
    verse = random.choice(BIBLE_VERSES)
    bot.reply_to(message, verse)

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
