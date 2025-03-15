import os
import logging
import random
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Lấy token & API từ biến môi trường (do Railway cung cấp)
BOT_TOKEN = os.getenv("cb80b05e-57e1-49cc-99a0-5d2dec7505a9")
GAS_API_URL = os.getenv("https://script.google.com/macros/s/AKfycbx9voP5oBi-m5nrCy6IVDlDfSdn5Fp_K5mmeLQwU_lSDPSkON0UTg6_Ui5E9JoW_1DS5g/exec")
OPENROUTER_API_KEY = os.getenv("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")

# Danh sách câu trả lời ngẫu nhiên
RANDOM_REPLIES = [
    "Dạ sếp, em có thể giúp gì ạ? 😊",
    "Chào sếp! Hôm nay có gì cần em hỗ trợ không? 😃",
    "Sếp ơi, em sẵn sàng giúp đây! 🚀",
    "Em đây, sếp cần gì cứ bảo nhé! 💪",
]

# Từ khóa tin nhắn đơn giản
SIMPLE_MESSAGES = ["alo", "hi", "hello", "ê", "chào", "ok", "hê"]

# Hàm gọi OpenRouter AI
def call_openrouter(message):
    if message.strip().lower() in SIMPLE_MESSAGES:
        return random.choice(RANDOM_REPLIES)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": message}]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Lỗi AI: {str(e)}"

# Hàm gọi API Google Apps Script để lấy báo cáo công việc
def get_google_sheet_report():
    try:
        response = requests.get(GAS_API_URL)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"❌ Lỗi báo cáo: {str(e)}"

# Hàm xử lý tin nhắn
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip().lower()

    if "báo cáo công việc" in user_message:
        report = get_google_sheet_report()
        await update.message.reply_text(report)
    else:
        bot_response = call_openrouter(user_message)
        await update.message.reply_text(bot_response)

# Hàm khởi động bot Telegram
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot đang chạy... Nhấn Ctrl + C để dừng!")
    app.run_polling()

if __name__ == "__main__":
    main()
