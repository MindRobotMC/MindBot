from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import logging

# تنظیمات
TOKEN = 'توکن رباتت رو اینجا بذار'
ADMIN_ID = 7608419661  # آیدی عددی شما

# لیست کاربران (در حافظه ذخیره می‌شه)
user_ids = set()

# فعال کردن لاگ برای دیباگ
logging.basicConfig(level=logging.INFO)

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text
    user_ids.add(user_id)

    # پیام خوش‌آمدگویی برای کاربران عادی
    if user_id != ADMIN_ID:
        keyboard = [[InlineKeyboardButton("🧠 کانال ما", url="https://t.me/MindOverMC")]]
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("سلام! به ربات MindOverMC خوش اومدی 👋", reply_markup=markup)
        return

    # فقط برای ادمین: ارسال همگانی
    if text.startswith("ارسال همگانی:"):
        msg = text.replace("ارسال همگانی:", "").strip()
        success = 0
        fail = 0
        for uid in list(user_ids):
            try:
                context.bot.send_message(
                    chat_id=uid,
                    text=msg,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🧠 MindOverMC", url="https://t.me/MindOverMC")]])
                )
                success += 1
            except:
                fail += 1
        update.message.reply_text(f"✅ پیام برای {success} نفر ارسال شد.\n❌ ناموفق: {fail}")
    else:
        update.message.reply_text("✏️ برای ارسال همگانی اینطوری پیام بده:\n\nارسال همگانی: متن موردنظر")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
