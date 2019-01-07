
# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import request

from app import app
from app import db
from app.models import Devices

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

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
    if req["request"]["nlu"]["tokens"][0].lower() in [
        'включи',
        'влючить'
    ]:
        name = req["request"]["nlu"]["tokens"][1].lower()
        device = Devices.query.filter_by(name=name).first()
        device.state = True
        res['response']['text'] = 'Включаю ' + str(device.state)
        db.session.commit()
    if req["request"]["nlu"]["tokens"][0].lower() in [
        'выключи',
        'вылючить'
    ]:
        res['response']['text'] = 'Выключаю'
        name = req["request"]["nlu"]["tokens"][1].lower()
        device = Devices.query.filter_by(name=name).first()
        device.state = False
        db.session.commit()


@app.route('/esp8266/<dev_id>/<name>/<dev_type>/<state>', methods=['GET'])
def esp8266(dev_id, state, dev_type, name):
    device = Devices.query.filter_by(dev_id=id).first()
    print(device.state)
    if state == "0":
        state = False
    if state == "1":
        state = True
    if device is None:
        dev = Devices(dev_id=dev_id, type=dev_type, prev_state=state, name=name)
        db.session.add(dev)
        db.session.commit()
        return "hi"
    else:
        device.prev_state = state
        if device.state:
            dev_state = 1
        else:
            dev_state = 0
        db.session.commit()
        return str(dev_state)

    # State.id = id
    # State.currentState = state
