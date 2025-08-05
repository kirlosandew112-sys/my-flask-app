from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()  # Загружаем переменные из .env
# Получаем BOT_TOKEN и CHAT_ID из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_to_telegram(name, phone, message=None, is_callback=False):
    try:
        if is_callback:
            text = f"📞 Новий запит на зворотний дзвінок:\n\n👤 Ім'я: {name}\n📞 Телефон: {phone}"
        else:
            text = f"📦 Нова заявка з сайту:\n\n👤 Ім'я: {name}\n📞 Телефон: {phone}\n📝 Повідомлення: {message or 'Немає повідомлення'}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(url, data={'chat_id': CHAT_ID, 'text': text})
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')
    if not name or not phone:
        return render_template('error.html', message="Будь ласка, заповніть усі обов'язкові поля.")
    if send_to_telegram(name, phone, message):
        return render_template('success.html')
    return render_template('error.html', message="Помилка відправки заявки. Спробуйте ще раз.")

@app.route('/callback', methods=['POST'])
def callback():
    name = request.form.get('name')
    phone = request.form.get('phone')
    if not name or not phone:
        return render_template('error.html', message="Будь ласка, заповніть усі обов'язкові поля.")
    if send_to_telegram(name, phone, is_callback=True):
        return render_template('success.html')
    return render_template('error.html', message="Помилка відправки запиту. Спробуйте ще раз.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)