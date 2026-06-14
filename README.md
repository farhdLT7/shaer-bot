# 🌙 ربات شاعر تلگرام

هر ۴ ساعت یک متن غمگین و شاعرانه با هوش مصنوعی تولید می‌کنه و توی کانالت می‌ذاره.

---

## مرحله ۱ — ساخت ربات تلگرام

1. به [@BotFather](https://t.me/BotFather) برو
2. بنویس `/newbot`
3. اسم و یوزرنیم بده
4. **توکن** رو کپی کن (شبیه: `7123456789:AAF...`)

---

## مرحله ۲ — ادمین کردن ربات در کانال

1. برو به کانالت → **Administrators**
2. ربات رو اضافه کن
3. دسترسی **Post Messages** رو بده

---

## مرحله ۳ — گرفتن Anthropic API Key

1. برو به [console.anthropic.com](https://console.anthropic.com)
2. ثبت‌نام کن (کریدیت رایگان اولیه داره)
3. از بخش **API Keys** یه کلید بساز

---

## مرحله ۴ — هاست روی Railway (رایگان)

### 4.1 آپلود کد
```bash
# یه ریپو GitHub بساز و این فایل‌ها رو push کن
git init
git add .
git commit -m "ربات شاعر"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

### 4.2 دیپلوی روی Railway
1. برو به [railway.app](https://railway.app) و با GitHub لاگین کن
2. روی **New Project** کلیک کن
3. **Deploy from GitHub repo** رو انتخاب کن
4. ریپوت رو انتخاب کن

### 4.3 متغیرهای محیطی (مهم!)
توی Railway برو به **Variables** و این سه تا رو اضافه کن:

| متغیر | مقدار |
|-------|-------|
| `TELEGRAM_BOT_TOKEN` | توکن از BotFather |
| `CHANNEL_ID` | مثلاً `@mychannel` یا `-100123456789` |
| `ANTHROPIC_API_KEY` | کلید از console.anthropic.com |
| `INTERVAL_HOURS` | `4` (یا هر عددی که می‌خوای) |

---

## تست محلی (اختیاری)

```bash
pip install -r requirements.txt

export TELEGRAM_BOT_TOKEN="توکنت"
export CHANNEL_ID="@کانالت"
export ANTHROPIC_API_KEY="کلیدت"

python bot.py
```

---

## ساختار فایل‌ها

```
├── bot.py           # کد اصلی ربات
├── requirements.txt # کتابخونه‌ها
├── railway.toml     # تنظیمات هاست
└── README.md
```

---

## نمونه خروجی

> گاهی دلتنگی مثل مه است — نه می‌بینیش، نه می‌توانی از آن بگریزی.
> فقط نفس که می‌کشی، سرد می‌شود...
>
> 🕯 ۲۳:۰۰
