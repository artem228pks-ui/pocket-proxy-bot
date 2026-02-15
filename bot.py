import os
import time
import random
import threading
import socks
import socket
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# ==================== НАСТРОЙКА ПРОКСИ ====================
# Весь трафик бота пойдет через локальный SOCKS5-прокси
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket

# ==================== ТВОИ ДАННЫЕ ====================
TOKEN = "8260184898:AAGSTkqgWvIyAhkAnpO4xscGg7qvFjFdd9g"  # твой токен
SSID = '''42["auth",{"session":"s%3AI6UMmR6CNcOHP0u1Wk3iVqZ2DhMEt7XojHAdmTlTjAcjlB6so9n4q8TpLXQrVfYw","isDemo":1,"uid":87654321,"platform":2}]'''

subscribers = set()
is_scanning = False

# Подключение к Pocket Option через прокси
try:
    from pocketoptionapi.stable_api import PocketOption
    pocket_api = PocketOption(SSID)
    pocket_api.connect()
    pocket_api.change_balance("PRACTICE")
    print("✅ Подключено к Pocket Option через прокси!")
except Exception as e:
    print(f"⚠️ Ошибка подключения: {e}, будет тестовый режим")
    pocket_api = None

# Команда /start
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("📊 Подписаться", callback_data='subscribe')]]
    await update.message.reply_text(
        "🤖 Бот сигналов Pocket Option (через прокси)\n\nНажми кнопку для подписки",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Обработчик кнопок
async def button_handler(update: Update, context):
    global is_scanning
    query = update.callback_query
    await query.answer()
    
    if query.data == 'subscribe':
        subscribers.add(query.from_user.id)
        await query.edit_message_text("✅ Ты подписан на сигналы!")
        
        if not is_scanning:
            is_scanning = True
            threading.Thread(target=send_signals, daemon=True).start()

# Функция отправки сигналов
def send_signals():
    global is_scanning
    app = Application.builder().token(TOKEN).build()
    
    assets = ["EURUSD_otc", "GBPUSD_otc", "BTCUSD_otc"]
    
    while is_scanning:
        try:
            # Пытаемся получить реальные сигналы через прокси
            if pocket_api:
                # Здесь будет реальный анализ
                # Пока тестовые сигналы
                pass
            
            # Тестовые сигналы (для отладки)
            asset = random.choice(assets)
            direction = random.choice(["CALL 📈", "PUT 📉"])
            price = round(random.uniform(1.05, 1.15), 5)
            
            msg = (f"🚨 *СИГНАЛ*\n"
                   f"Актив: {asset}\n"
                   f"Направление: {direction}\n"
                   f"Цена: {price}\n"
                   f"Время: {datetime.now().strftime('%H:%M:%S')}")
            
            for user_id in subscribers.copy():
                try:
                    app.bot.send_message(chat_id=user_id, text=msg, parse_mode='Markdown')
                except:
                    subscribers.discard(user_id)
            
            time.sleep(60)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(10)

# Запуск
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот с прокси запущен на Render!")
    print("📱 Отправь /start в Telegram")
    app.run_polling()

if __name__ == "__main__":
    main()
