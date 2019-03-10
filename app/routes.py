# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import request
from datetime import datetime

from app import app
from app import db
from app.models import Devices
from app.models import Timer

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)
    times()
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle(req, res):
    # Эта функция обрабатывает запросы пользователя.
    if req["request"]["nlu"]["tokens"][0].lower() in [
        'включи',
        'включить'
    ] and req["request"]["nlu"]["tokens"][1].lower() in ['лампу']:
        name = req["request"]["nlu"]["tokens"][2].lower()
        device = Devices.query.filter_by(name=name, type='lamp').first()
        device.state = True
        res['response']['text'] = 'Включаю'
        db.session.commit()
    if req["request"]["nlu"]["tokens"][0].lower() in [
        'выключи',
        'выключить'
    ] and req["request"]["nlu"]["tokens"][1].lower() in ['лампу']:
        res['response']['text'] = 'Выключаю'
        name = req["request"]["nlu"]["tokens"][2].lower()
        device = Devices.query.filter_by(name=name).first()
        device.state = False
        db.session.commit()
    if req["request"]["nlu"]["tokens"][0].lower() in ['таймер']:
        dev_name = req["request"]["nlu"]["tokens"][2].lower()
        on_hour = req["request"]["nlu"]["entities"][0]['value']['hour']
        on_minute = req["request"]["nlu"]["entities"][0]['value']['minute']
        off_hour = req["request"]["nlu"]["entities"][1]['value']['hour']
        off_minute = req["request"]["nlu"]["entities"][1]['value']['minute']
        timer = Timer(dev_name=dev_name, on_minute=on_minute, on_hour=on_hour, off_hour=off_hour, off_minute=off_minute)
        db.session.add(timer)
        db.session.commit()


def times():
    timer = Timer.query.all()
    _t = datetime.now()
    hour = _t.hour
    minute = _t.minute
    for t in timer:
        name = t.dev_name
        device = Devices.query.filter_by(name=name).first()
        if not hour <= t.on_hour and not minute <= t.on_minute:
            device.state = True
        if not hour <= t.off_hour and not minute <= t.off_minute:
            device.state = False


@app.route('/esp8266/<dev_id>/<name>/<dev_type>/<state>', methods=['GET'])
def esp8266(dev_id, state, dev_type, name):
    # Эта функция раьотает  с устройством
    dev_state = 0
    device = Devices.query.filter_by(dev_id=dev_id).first()
    if state == "0":
        state = False
    if state == "1":
        state = True
    if device is None:
        dev = Devices(dev_id=id, type=dev_type, prev_state=state, dev_name=name)
        db.session.add(dev)
        db.session.commit()
        return "hi"
    else:
        device.prev_state = state
        if device.state:
            dev_state = 1
        if not device.state:
            dev_state = 0
        db.session.commit()
        return str(dev_state)
