import telebot
import requests
import random
import os
from datetime import datetime
import schedule
import time
import threading  # Thêm thư viện threading
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
    today = datetime.today().strftime('%-d-%-m-%Y')  # Kiểm tra lại định dạng
    print("Hôm nay là:", today)  # Debug để kiểm tra ngày
    
    lesson = lessons.get(today, "Hôm nay không có bài học.")
    response = f"📖 *Vâng! Thưa Sếp, bài học Kinh Thánh Hằng Ngày hôm nay ({today}):*\n➡️ {lesson}\n\n🔗 Xem chi tiết tại: [Facebook]({FACEBOOK_LINK})"
    
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text.strip().count('-') == 2)
def send_lesson_by_text(message):
    date_requested = message.text.strip()
    
    lesson = lessons.get(date_requested, "Không có bài học cho ngày này.")
    response = f"📖 Vâng! Thưa Sếp, bài học Kinh Thánh Hằng Ngày hôm nay ({date_requested}):\n➡️ {lesson}"
    
    bot.reply_to(message, response)

# Định nghĩa múi giờ Việt Nam
tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')

# Hàm gửi bài học tự động hàng ngày
def send_daily_lesson():
    today = datetime.now().strftime('%-d-%-m-%Y')  # Định dạng ngày đúng với danh sách lessons
    lesson = lessons.get(today, "Hôm nay không có bài học.")
    chat_id = '6416693025'
    bot.send_message(chat_id, f"Vâng! Thưa Sếp, bài học Kinh Thánh Hằng Ngày ({today}) là: {lesson}")

# Đặt lịch gửi thông báo hàng ngày vào lúc 5h00 sáng
schedule.every().day.at("22:00").do(send_daily_lesson)
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

# Biến lưu trạng thái xem tin nhắn trước có phải "câu kinh thánh" không
last_message_was_bible_request = {}

@bot.message_handler(func=lambda message: message.text.lower() == "câu kinh thánh")
def send_bible_verse_first(message):
    global last_message_was_bible_request
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ok Sếp, tôi sẽ khích lệ Sếp bằng một câu Kinh Thánh")
    bot.send_message(chat_id, random.choice(BIBLE_VERSES))
    last_message_was_bible_request[chat_id] = True  # Đánh dấu tin nhắn trước là yêu cầu câu Kinh Thánh

@bot.message_handler(func=lambda message: message.text.lower() == "câu nữa")
def send_bible_verse_again(message):
    global last_message_was_bible_request
    chat_id = message.chat.id
    if last_message_was_bible_request.get(chat_id, False):  # Kiểm tra xem tin nhắn trước có phải là "câu kinh thánh" không
        bot.send_message(chat_id, "Vâng!")
        bot.send_message(chat_id, random.choice(BIBLE_VERSES))
    else:
        bot.send_message(chat_id, "Sếp muốn một câu Kinh Thánh à? Hãy nói 'câu kinh thánh' trước nhé!")
    last_message_was_bible_request[chat_id] = True  # Đánh dấu tin nhắn này là yêu cầu câu Kinh Thánh

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

# Hàm chạy đồng thời schedule và bot.polling
def run_schedule_and_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Tạo một thread cho schedule
schedule_thread = threading.Thread(target=run_schedule_and_bot)
schedule_thread.start()



# Hàm chạy đồng thời schedule và bot.polling
def run_schedule_and_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Tạo một thread cho schedule
schedule_thread = threading.Thread(target=run_schedule_and_bot)
schedule_thread.start()
import time

def find_bible_verse(book, chapter, verse):
    with open("kinh_thanh_updated.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    found_book = False
    found_chapter = False
    found_verse = False
    verse_text = ""

    for line in lines:
        line = line.strip()

        if not line:  # Nếu dòng trống, bỏ qua
            continue

        # Tìm sách
        if line.lower() == book.lower():
            found_book = True
            found_chapter = False
            continue

        # Tìm chương
        if found_book and line.lower() == f"chương {chapter}".lower():
            found_chapter = True
            continue

        # Tìm câu
        if found_chapter:
            parts = line.split(" ", 1)  # Tách số câu và nội dung
            if len(parts) > 1 and parts[0].isdigit() and int(parts[0]) == verse:
                found_verse = True
                verse_text = parts[1]
                continue

            # Nếu đã tìm thấy câu, tiếp tục nối các dòng tiếp theo
            if found_verse:
                if line[0].isdigit():  # Nếu dòng mới bắt đầu bằng số, tức là câu mới -> dừng lại
                    break
                verse_text += " " + line  # Nối thêm nội dung

    return f"{book} {chapter}:{verse} {verse_text}" if found_verse else "Không tìm thấy câu Kinh Thánh này."

def send_long_message(chat_id, text):
    """ Chia nhỏ tin nhắn dài để tránh lỗi 414 trên Telegram """
    max_length = 4096  # Telegram giới hạn tin nhắn
    for i in range(0, len(text), max_length):
        bot.send_message(chat_id, text[i:i+max_length])

@bot.message_handler(func=lambda message: True)  # Xử lý tất cả tin nhắn
def auto_detect_bible_verse(message):
    try:
        query = message.text.strip()

        # 🔍 Kiểm tra định dạng "Sách Chương:Câu" bằng Regex
        match = re.match(r"([\wÀ-Ỹà-ỹ-]+) (\d+):(\d+)", query)
        if not match:
            return  # Nếu tin nhắn không phải câu Kinh Thánh, bỏ qua

        book, chapter, verse = match.groups()
        chapter = int(chapter)
        verse = str(verse)  # Chuyển số câu về dạng chuỗi

        # 🔥 Tìm câu Kinh Thánh trong file
        verse_text = find_bible_verses(book, chapter, verse, max_verses=1)

        # 🔹 Gửi kết quả
        send_long_message(message.chat.id, f"📖 {verse_text}")

    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")
# Chạy bot polling
bot.polling(none_stop=True, interval=0)
import telebot

TOKEN = "7973266839:AAF5VPoQvApooSpPtCaqJUl0Iqdu16lfFJg"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello!")

# Chạy polling với drop_pending_updates để tránh lỗi 409
while True:
    try:
        bot.polling(none_stop=True, interval=3, timeout=30)
    except Exception as e:
        print(f"❌ Lỗi: {e}. Bot sẽ thử lại sau...")
        time.sleep(10)  # Chờ 10 giây trước khi thử lại

