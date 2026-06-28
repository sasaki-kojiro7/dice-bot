"""
ربات تلگرام تاس مثبت / منفی با کیبورد دائمی
---------------------------------------------
دو دکمه روی کیبورد پایین صفحه:
    🟢 Roll 2 🟢   ->  عدد مثبت رندوم بین 1 تا 9
    🔴 Roll 1 🔴   ->  عدد منفی رندوم بین -1 تا -9

دستورات:
    /on   -> کیبورد رو نشون می‌ده
    /off  -> کیبورد رو محو می‌کنه

نیازمندی:
    pip install python-telegram-bot --upgrade

اجرا:
    python dice_bot.py
"""

import random
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== توکن ربات رو اینجا بگذار =====
BOT_TOKEN = "8798661268:AAG_OTrNW-XfLRE3Yh2h1GaJ5gJ9SLEyaoU"
# =====================================

POSITIVE_BUTTON = "🟢 Roll 2 🟢"
NEGATIVE_BUTTON = "🔴 Roll 1 🔴"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# کیبورد دائمی با دو دکمه، کنار هم
dice_keyboard = ReplyKeyboardMarkup(
    [[POSITIVE_BUTTON, NEGATIVE_BUTTON]],
    resize_keyboard=True,
    is_persistent=True,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور /start"""
    await update.message.reply_text(
        "سلام! 🎲\n"
        "برای روشن کردن کیبورد تاس، دستور /on رو بزن.\n"
        "برای خاموش کردنش، /off رو بزن."
    )


async def turn_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور /on : نمایش کیبورد تاس"""
    await update.message.reply_text(
        "کیبورد تاس روشن شد ✅",
        reply_markup=dice_keyboard,
    )


async def turn_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور /off : محو کردن کیبورد تاس"""
    await update.message.reply_text(
        "کیبورد تاس خاموش شد ❌",
        reply_markup=ReplyKeyboardRemove(),
    )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """وقتی کاربر یکی از دکمه‌های کیبورد رو بزنه"""
    text = update.message.text

    if text == POSITIVE_BUTTON:
        number = random.randint(1, 9)
        await update.message.reply_text(f"🟢 {number} 🟢")

    elif text == NEGATIVE_BUTTON:
        number = random.randint(1, 9)
        await update.message.reply_text(f"🔴 {number} 🔴")


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("on", turn_on))
    application.add_handler(CommandHandler("off", turn_off))

    # هندل کردن کلیک روی دکمه‌های کیبورد (که به‌صورت متن ساده ارسال می‌شن)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button)
    )

    logger.info("ربات در حال اجراست...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
