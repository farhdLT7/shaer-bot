import asyncio
import logging
import os
from groq import Groq
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
GROQ_KEY       = os.environ["GROQ_API_KEY"]
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", "4"))

client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """تو یک شاعر و نویسنده ایرانی هستی با روحی ظریف و غمگین.
هر بار که می نویسی، یک متن کاملا منحصربه فرد خلق کن.
سبک نوشتاریت ترکیبی از نثر شاعرانه، احساس عمیق و تصویرسازی ظریف است.
از کلیشه بپرهیز. از دل بنویس.
فقط متن شاعرانه بنویس، هیچ توضیح یا مقدمه ای اضافه نکن."""

USER_PROMPTS = [
    "یک متن غمگین و شاعرانه درباره دلتنگی بنویس. کوتاه، عمیق، بی نظیر.",
    "درباره شب و تنهایی بنویس. نثر شاعرانه. حس واقعی.",
    "یک متن کوتاه درباره چیزی که رفت و برنگشت بنویس.",
    "درباره باران و خاطره بنویس. غمگین و زیبا.",
    "از جنس سکوت بنویس. از آنچه گفته نشد.",
    "یک متن شاعرانه درباره پاییز روح بنویس.",
    "درباره عشقی که فقط در خاطره زنده است بنویس.",
    "از نگاهی بنویس که دیگر نیست.",
]

prompt_index = 0

def generate_poem() -> str:
    global prompt_index
    prompt = USER_PROMPTS[prompt_index % len(USER_PROMPTS)]
    prompt_index += 1
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )
    return response.choices[0].message.content.strip()

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
        log.info("متن با موفقیت ارسال شد.")
    except TelegramError as e:
        log.error(f"خطای تلگرام: {e}")
    except Exception as e:
        log.error(f"خطا: {e}")

async def main():
    log.info(f"ربات شاعر شروع شد - هر {INTERVAL_HOURS} ساعت پست میذاره")
    await post_poem()
    while True:
        await asyncio.sleep(INTERVAL_HOURS * 3600)
        await post_poem()

if __name__ == "__main__":
    asyncio.run(main())
