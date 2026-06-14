import asyncio
import logging
import os
import google.generativeai as genai
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID     = os.environ["CHANNEL_ID"]
GEMINI_KEY     = os.environ["GEMINI_API_KEY"]
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", "4"))

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """تو یک شاعر و نویسنده‌ی ایرانی هستی با روحی ظریف و غمگین.
هر بار که می‌نویسی، یک متن کاملاً منحصربه‌فرد خلق کن.
سبک نوشتاری‌ات ترکیبی از نثر شاعرانه، احساس عمیق و تصویرسازی ظریف است.
از کلیشه بپرهیز. از دل بنویس.
فقط متن شاعرانه بنویس، هیچ توضیح یا مقدمه‌ای اضافه نکن."""

USER_PROMPTS = [
    "یک متن غمگین و شاعرانه درباره‌ی دلتنگی بنویس. کوتاه، عمیق، بی‌نظیر.",
    "درباره‌ی شب و تنهایی بنویس. نثر شاعرانه. حس واقعی.",
    "یک متن کوتاه درباره‌ی چیزی که رفت و برنگشت بنویس.",
    "درباره‌ی باران و خاطره بنویس. غمگین و زیبا.",
    "از جنس سکوت بنویس. از آنچه گفته نشد.",
    "یک متن شاعرانه درباره‌ی پاییز روح بنویس.",
    "درباره‌ی عشقی که فقط در خاطره زنده‌ست بنویس.",
    "از نگاهی بنویس که دیگر نیست.",
]

prompt_index = 0

def generate_poem() -> str:
    global prompt_index
    prompt = USER_PROMPTS[prompt_index % len(USER_PROMPTS)]
    prompt_index += 1
    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
    response = model.generate_content(full_prompt)
    return response.text.strip()

async def post_poem():
    bot = Bot(token=TELEGRAM_TOKEN)
    log.info("در حال تولید متن...")
    try:
        poem = generate_poem()
        now = datetime.now().strftime("%H:%M")
        caption = f"{poem}\n\n🕯 {now}"
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=caption,
            parse_mode=None
        )
        log.info("✅ متن با موفقیت ارسال شد.")
    except TelegramError as e:
        log.error(f"خطای تلگرام: {e}")
    except Exception as e:
        log.error(f"خطا: {e}")

async def main():
    log.info(f"🌙 ربات شاعر شروع شد — هر {INTERVAL_HOURS} ساعت پست می‌ذاره")
    await post_poem()
    while True:
        await asyncio.sleep(INTERVAL_HOURS * 3600)
        await post_poem()

if __name__ == "__main__":
    asyncio.run(main())
