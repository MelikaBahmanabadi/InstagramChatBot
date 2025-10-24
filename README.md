# Instagram DM Bot Simulator

ربات پاسخگوی اینستاگرام با استفاده از FastAPI، RAG و Free LLM API

## نصب و اجرا

### 1. کلون پروژه
```bash
git clone https://github.com/MelikaBahmanabadi/InstagramChatBot.git
cd InstagramChatBot
```

### 2. نصب وابستگی‌ها
```bash
pip3 install -r requirements.txt
```

اگر با خطای `externally-managed-environment` مواجه شدید:
```bash
pip3 install --break-system-packages -r requirements.txt
```

### 3. اجرای سرویس
```bash
python3 main.py
```

سرویس روی `http://localhost:8000` اجرا می‌شود.

## استفاده

### ارسال درخواست

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "user123",
    "message_id": "m001",
    "text": "قیمت گوشی سامسونگ چقدره؟"
  }'
```

### پاسخ نمونه

```json
{
  "reply": "قیمت گوشی سامسونگ Galaxy S23 با قیمت 28,500,000 تومان موجود است..."
}
```

### نمونه 2: سوال درباره لپ‌تاپ

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{"sender_id":"user2","message_id":"m002","text":"لپ تاپ ایسوس دارید؟"}'
```

پاسخ:
```json
{
  "reply": "بله، ما لپ‌تاپ ایسوس VivoBook را در فروشگاه داریم. این لپ‌تاپ ۱۵ اینچی با پردازنده Core i5، ۸ گیگابایت رم و قیمت ۱۸,۵۰۰,۰۰۰ تومان ارائه می‌شود..."
}
```

### نمونه 3: سوال درباره هدفون

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{"sender_id":"user3","message_id":"m003","text":"هدفون بی سیم"}'
```

پاسخ:
```json
{
  "reply": "سلام! از بین محصولات موجود، دو هدفون بی‌سیم داریم: هدفون سونی WH-1000XM5 با قیمت 14,500,000 تومان و هدفون بیتس Studio3 با قیمت 11,200,000 تومان..."
}
```

## ساختار پروژه

```
InstagramChatBot/
├── main.py              # FastAPI endpoint
├── config.py            # تنظیمات
├── requirements.txt     # وابستگی‌ها
├── database/
│   └── db_manager.py    # مدیریت دیتابیس
├── services/
│   ├── rag_service.py   # سرویس RAG
│   └── llm_service.py   # سرویس LLM
└── db/
    └── app_data.sqlite  # دیتابیس (100 محصول)
```

## ویژگی‌ها

- استفاده از Free LLM API (بدون نیاز به API Key)
- RAG برای بازیابی اطلاعات از دیتابیس
- امنیت کامل (SQL Injection Prevention, Rate Limiting)
- 100 محصول تستی در دیتابیس SQLite
- پاسخ‌های فارسی

## دیتابیس

دیتابیس `db/app_data.sqlite` شامل 100 محصول الکترونیکی است و از قبل آماده شده است.

ساختار جدول:
```sql
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  description TEXT,
  price REAL
);
```

## نکات

- نیازی به تنظیم API Key نیست
- دیتابیس از قبل آماده است
- Rate Limit: 10 درخواست در دقیقه
