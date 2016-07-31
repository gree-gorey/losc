# -*- coding:utf-8 -*-

import time
import flask
import pickle
from structures import Parameters, Store

__author__ = 'gree-gorey'

# Initialize the Flask application
app = flask.Flask(__name__)


store = Store()


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/parameters')
def parameters():
    return flask.render_template('parameters.html')


@app.route('/statistics')
def statistics():
    return flask.render_template('statistics.html',
                                 first_list_len=len(store.first_list),
                                 second_list_len=len(store.second_list),
                                 max=min(len(store.first_list), len(store.second_list)))


@app.route('/_create', methods=['GET', 'POST'])
def create():
    parameters_from_client = flask.request.json

    store.parameters.length = int(parameters_from_client['length'])
    store.parameters.statistics = parameters_from_client['statistics']
    store.parameters.frequency = parameters_from_client['frequency']
    # print parameters.length

    # устанавливаем параметры
    store.setup_parameters()

    # добавим отсчет времени
    store.time_begin = time.time()

    # собственно генерация листов
    store.generate()

    if store.success:
        # подсчет окончательной статы
        store.final_statistics()

        # для печати результатов
        store.print_results()

        # создаем файлы и пакуем в архив
        store.create_zip()

    result = {}

    return flask.jsonify(result=result)


@app.route('/_set_parameters', methods=['GET', 'POST'])
def set_parameters():
    global store

    # загружаем базу данных в переменную
    with open(u'data/store.p', u'r') as f:
        store = pickle.load(f)

    store.parameters = Parameters()

    parameters_from_client = flask.request.json
    # print parameters_from_client['list1']['features']['reflexivity']

    # создаем в сторе предварительные листы
    store.first_list = store.create_list_from_to_choose(parameters_from_client['list1'])
    store.second_list = store.create_list_from_to_choose(parameters_from_client['list2'])

    # нормализуем все к шкале от 0 до 1
    store.normalize()
    # print store.first_list[0].normalized_features

    # проверяем, должны ли различаться и если да, то различаем
    if parameters_from_client['differ_feature'] != 'question':
        store.key_for_differ_feature = parameters_from_client['differ_feature']
        store.which_higher = parameters_from_client['which_is_higher']
        store.differentiate()
    # print len(store.first_list)
    # print store.second_list[0].name

    # создаем вектор одинаковых
    store.parameters.same = parameters_from_client['same_features']

    # если листы оказались одинаковыми, нужно рандомно разделить их
    store.split()

    result = {}

    return flask.jsonify(result=result)


if __name__ == '__main__':
    app.run(
        # host="0.0.0.0",
        # port=int("80"),
        debug=True
    )
