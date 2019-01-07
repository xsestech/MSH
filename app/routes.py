
# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import request
from app import app
from app.models import Devices
from app import db

class State():
    state = 0
    currentState = 0
    id = 0
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
# Функция для непосредственной обработки диалога.


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'включи',
        'включить',
    ]:
        # Пользователь согласился, отправляем запрос на .
        res['response']['text'] = 'Включаю'
        State.state = 1
        return

    if req['request']['original_utterance'].lower() in [
        'выключи',
        'выключить'
    ]:
        res['response']['text'] = 'Выключаю'
        State.state = 0
        return
    if req['request']['original_utterance'].lower() in [
        'состояние'
    ]:
        if State.currentState == 0:
            res['response']['text'] = 'Выключено'
        else:
            res['response']['text'] = 'Включено'
        return
    # Функция возвращает две подсказки для ответа.


def get_suggests(user_id, sugest_text_1, sugest_text_2):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': sugest_text_1, 'hide': True},
        {'title': sugest_text_2, 'hide': True}
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.


    return suggests

def handle(req,res):
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


@app.route('/esp8266/<id>/<name>/<type>/<state>', methods=['GET'])
def esp8266(id, state, type, name):
    device = Devices.query.filter_by(dev_id=id).first()
    print(device.state)
    if state == "0":
        state = False
    if state == "1":
        state = True
    if device is None:
        dev = Devices(dev_id=id, type=type, prev_state=state, name=name)
        db.session.add(dev)
        db.session.commit()
        return "hi"
    else:
        device.prev_state = state
        if device.state == True:
            dev_state = 1
        else:
            dev_state = 0
        db.session.commit()
        return str(dev_state)

    # State.id = id
    # State.currentState = state
