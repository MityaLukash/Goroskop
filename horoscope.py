#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Данные о знаках зодиака
ZODIAC = {
    'aries': {'name': 'Овен', 'dates': '21 марта - 19 апреля'},
    'taurus': {'name': 'Телец', 'dates': '20 апреля - 20 мая'},
    'gemini': {'name': 'Близнецы', 'dates': '21 мая - 20 июня'},
    'cancer': {'name': 'Рак', 'dates': '21 июня - 22 июля'},
    'leo': {'name': 'Лев', 'dates': '23 июля - 22 августа'},
    'virgo': {'name': 'Дева', 'dates': '23 августа - 22 сентября'},
    'libra': {'name': 'Весы', 'dates': '23 сентября - 22 октября'},
    'scorpio': {'name': 'Скорпион', 'dates': '23 октября - 21 ноября'},
    'sagittarius': {'name': 'Стрелец', 'dates': '22 ноября - 21 декабря'},
    'capricorn': {'name': 'Козерог', 'dates': '22 декабря - 19 января'},
    'aquarius': {'name': 'Водолей', 'dates': '20 января - 18 февраля'},
    'pisces': {'name': 'Рыбы', 'dates': '19 февраля - 20 марта'}
}

# Список предсказаний
PREDICTIONS = [
    "Сегодня отличный день для новых начинаний!",
    "Звезды советуют быть осторожным в финансовых вопросах.",
    "Вас ждёт приятная встреча со старым другом.",
    "Сегодня лучше сосредоточиться на работе и не отвлекаться.",
    "Удачный день для творчества и самовыражения.",
    "Возможны неожиданные повороты событий, будьте готовы.",
    "День благоприятен для общения и новых знакомств.",
    "Прислушайтесь к своей интуиции — она вас не подведёт.",
    "Звезды предвещают небольшое приключение.",
    "Сегодня важно уделить время отдыху и восстановлению сил.",
    "Вас ждёт успех в делах, начатых ранее.",
    "Будьте внимательны к деталям — в них скрыт успех."
]

COLORS = ['красный', 'синий', 'зелёный', 'жёлтый', 'фиолетовый', 'оранжевый']

def get_horoscope(sign_key):
    """Возвращает словарь с предсказанием для знака"""
    sign = ZODIAC.get(sign_key)
    if not sign:
        return None
    return {
        'name': sign['name'],
        'dates': sign['dates'],
        'prediction': random.choice(PREDICTIONS),
        'luck': random.randint(1, 10),
        'lucky_number': random.randint(1, 99),
        'color': random.choice(COLORS),
        'date': datetime.now().strftime('%d.%m.%Y')
    }

class HoroscopeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(MAIN_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Читаем данные формы
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = urllib.parse.parse_qs(post_data.decode('utf-8'))
        sign = params.get('sign', [''])[0]

        if not sign or sign not in ZODIAC:
            # Если знак не выбран или неверный
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(ERROR_PAGE.encode('utf-8'))
            return

        horoscope = get_horoscope(sign)
        result_page = RESULT_PAGE.format(
            name=horoscope['name'],
            dates=horoscope['dates'],
            prediction=horoscope['prediction'],
            luck=horoscope['luck'],
            number=horoscope['lucky_number'],
            color=horoscope['color'],
            date=horoscope['date']
        )
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result_page.encode('utf-8'))

# HTML-шаблоны (простые, без CSS)
MAIN_PAGE = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Гороскоп</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: #f0f0f0; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        select, button { padding: 8px; margin: 10px; font-size: 16px; }
        button { background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 Гороскоп на сегодня</h1>
        <form method="POST">
            <select name="sign" required>
                <option value="">Выберите знак</option>
                <option value="aries">Овен (21.03-19.04)</option>
                <option value="taurus">Телец (20.04-20.05)</option>
                <option value="gemini">Близнецы (21.05-20.06)</option>
                <option value="cancer">Рак (21.06-22.07)</option>
                <option value="leo">Лев (23.07-22.08)</option>
                <option value="virgo">Дева (23.08-22.09)</option>
                <option value="libra">Весы (23.09-22.10)</option>
                <option value="scorpio">Скорпион (23.10-21.11)</option>
                <option value="sagittarius">Стрелец (22.11-21.12)</option>
                <option value="capricorn">Козерог (22.12-19.01)</option>
                <option value="aquarius">Водолей (20.01-18.02)</option>
                <option value="pisces">Рыбы (19.02-20.03)</option>
            </select>
            <br>
            <button type="submit">✨ Узнать гороскоп ✨</button>
        </form>
    </div>
</body>
</html>'''

RESULT_PAGE = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Гороскоп для {name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: #f0f0f0; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .prediction {{ font-size: 18px; margin: 20px; padding: 20px; background: #f9f9f9; border-radius: 5px; }}
        a {{ display: inline-block; margin-top: 20px; color: #4CAF50; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 {name}</h1>
        <p>📅 {dates}</p>
        <p>📆 {date}</p>
        <div class="prediction">«{prediction}»</div>
        <p>🍀 Уровень удачи: {luck}/10</p>
        <p>🔢 Счастливое число: {number}</p>
        <p>🎨 Счастливый цвет: {color}</p>
        <a href="/">← Назад к выбору знака</a>
        <br><br>
        <a href="/">✨ Новое предсказание ✨</a>
    </div>
</body>
</html>'''

ERROR_PAGE = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Ошибка</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; }
        a { color: #4CAF50; }
    </style>
</head>
<body>
    <div class="container">
        <h1>❌ Ошибка</h1>
        <p>Пожалуйста, выберите знак зодиака.</p>
        <a href="/">Вернуться на главную</a>
    </div>
</body>
</html>'''

if __name__ == '__main__':
    server = HTTPServer(('localhost', 5000), HoroscopeHandler)
    print('Сервер запущен на http://localhost:5000')
    print('Нажмите Ctrl+C для остановки')
    server.serve_forever()