# -*- coding:utf-8 -*-

import time
import flask
import pickle
from structures import List, Parameters

__author__ = 'gree-gorey'

# Initialize the Flask application
app = flask.Flask(__name__)

# создаем пустой экземпляр класса с параметрами
parameters = Parameters()

# загружаем базу данных в переменную
with open(u'store.p', u'r') as f:
    store = pickle.load(f)


def set_parameters(paramaters_from_client):
    # добавляем параметры первого листа
    parameters.first_list = List()
    parameters.first_list.pos = paramaters_from_client['pos']
    if parameters.first_list.pos == 'verb':
        parameters.first_list.arguments = paramaters_from_client['arguments']
        parameters.first_list.reflexivity = paramaters_from_client['reflexivity']
        parameters.first_list.instrumentality = paramaters_from_client['instrumentality']
        parameters.first_list.relation = paramaters_from_client['relation']
    elif parameters.first_list.pos == 'noun':
        parameters.first_list.part = paramaters_from_client['part']
    parameters.first_list.get_vector()

    # добавляем параметры второго листа
    parameters.second_list = List()
    parameters.second_list.pos = self.list_2_pos.checkedId()
    if parameters.second_list.pos == 1:
        parameters.second_list.arguments = self.arguments_list2.currentIndex()
        parameters.second_list.reflexivity = self.reflexivity_list2.currentIndex()
        parameters.second_list.instrumentality = self.instrumentality_list2.currentIndex()
        parameters.second_list.relation = self.relation_list2.currentIndex()
    elif parameters.second_list.pos == 2:
        parameters.second_list.part = self.part_list2.currentIndex()
    parameters.second_list.get_vector()

    # создаем в сторе предварительные листы
    store.first_list = store.create_list_from_to_choose(parameters.first_list)
    store.second_list = store.create_list_from_to_choose(parameters.second_list)

    store.normalize()

    # проверяем, должны ли различаться
    if self.differ_radio.checkedId() == 1:
        self.parent().parent().store.differ = self.diff_parameter.currentIndex()
        self.parent().parent().store.which_higher = self.higher.currentIndex()
        self.parent().parent().store.differentiate()

    # создаем вектор одинаковых
    parameters.get_same(self.parent().parent().store)

    store.split()


parameters.statistics = self.statistics.currentIndex()
parameters.freq = self.freq.currentIndex()
parameters.length = int(self.length.text())


def go():
    # устанавливаем параметры
    store.setup_parameters(parameters)

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


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/set_parameters')
def set_parameters():
    return flask.render_template('parameters.html')


@app.route('/set_statistics')
def set_statistics():
    return flask.render_template('statistics.html')


@app.route('/preview')
def preview():
    return flask.render_template('preview.html')


@app.route('/_query')
def query():
    query = flask.request.args.get('query', 0, type=unicode)
    parameter = flask.request.args.get('parameter', 0, type=unicode)
    # WORKS
    if parameter == 'all':
        res = es.search(index="temp_dict", body={"query": {"match": {"_all": query}},
                        "sort": [{"field_for_sorting": {"order": "asc"}}],
                        "size": 500})
    # WORKS
    elif parameter == 'header':
        res = es.search(index="temp_dict", body={"query": {"match": {"header.forms.normalized_content": query}},
                        "sort": [{"field_for_sorting": {"order": "asc"}}],
                        "size": 500})
    # WORKS
    elif parameter == 'form':
        res = es.search(index="temp_dict",
                        body={"query": {"multi_match": {"query": query, "fields": ["header.forms.normalized_content"]}},
                              "sort": [{"field_for_sorting": {"order": "asc"}}],
                              "size": 500})
        res_form_from_senses = es.search(index="temp_dict", body=get_query_example('form', query))
        res_ref_from_senses = es.search(index="temp_dict", body=get_query_example('ref', query))
        res['hits']['hits'] += res_form_from_senses['hits']['hits']
        res['hits']['hits'] += res_ref_from_senses['hits']['hits']
    # WORKS
    elif parameter == 'def':
        res = es.search(index="temp_dict", body=get_query('def', query))
    # WORKS
    elif parameter == 'example':
        res = es.search(index="temp_dict", body=get_query_example('example', query))
    # WORKS
    elif parameter == 'place':
        res = es.search(index="temp_dict",
                        body={"query": {"multi_match": {"query": query, "fields": ["header.forms.place",
                                                                                   "header.place",
                                                                                   "senses.elements.place"]}},
                              "sort": [{"field_for_sorting": {"order": "asc"}}],
                              "size": 500})
        res_place_from_senses = es.search(index="temp_dict", body=get_query('place', query))
        res['hits']['hits'] += res_place_from_senses['hits']['hits']
    # WORKS
    elif parameter == 'style':
        res = es.search(index="temp_dict",
                        body={"query": {"multi_match": {"query": query, "fields": ["header.forms.style",
                                                                                   "header.style",
                                                                                   "senses.elements.style"]}},
                              "sort": [{"field_for_sorting": {"order": "asc"}}],
                              "size": 500})
        res_style_from_senses = es.search(index="temp_dict", body=get_query('style', query))
        res['hits']['hits'] += res_style_from_senses['hits']['hits']
    else:
        res = {'hits': {}}
        res['hits']['hits'] = None

    if res['hits']['hits']:
        result = [True, res['hits']['hits']]
    else:
        result = [False, None]
    return flask.jsonify(result=result)


@app.route('/_get_by_id')
def get_by_id():
    index = flask.request.args.get('index', 0, type=unicode)
    # print index
    result = es.get(index="temp_dict", doc_type='entry', id=index)
    return flask.jsonify(result=result)


@app.route('/_get_letter_list')
def get_letter_list():
    slice_number = flask.request.args.get('slice', 0, type=int)
    links = create_links(es)
    entries = get_entries_by_class(es, slice_number)
    result = {'links': links, 'entries': entries}
    return flask.jsonify(result=result)


@app.route('/_save', methods=['GET', 'POST'])
def save():
    json_from_client = flask.request.json
    entry = normalize(json_from_client['entry'])
    entry = add_class(entry)

    if json_from_client['edit'] == 'edit':
        index = json_from_client['index']
        try:
            res = es.index(index='temp_dict', doc_type='entry', id=index, body=entry)
            result = {'feedback': 'success', 'id': res['_id']}
        except:
            result = {'feedback': 'failure'}
    else:
        try:
            res = es.index(index='temp_dict', doc_type='entry', body=entry)
            result = {'feedback': 'success', 'id': res['_id']}
        except:
            result = {'feedback': 'failure'}

    return flask.jsonify(result=result)


@app.route('/_delete', methods=['GET', 'POST'])
def delete():
    json_from_client = flask.request.json
    index = json_from_client['index']
    try:
        es.delete(index="temp_dict", doc_type="entry", id=index)
        result = {'feedback': 'success'}
    except:
        result = {'feedback': 'failure'}
    return flask.jsonify(result=result)


@app.route('/_export_tei', methods=['GET', 'POST'])
def export_tei():
    res = es.search(index="temp_dict", body={"query": {"match_all": {}},
                    "sort": [{"field_for_sorting": {"order": "asc"}}],
                    "size": 10000})

    all_entries = [hit["_source"] for hit in res['hits']['hits']]

    try:
        xml_doc = create_tei_xml(all_entries)
        create_zip(xml_doc)
        result = "success"
    except:
        result = "failure"

    return flask.jsonify(result=result)


@app.route('/_export_json', methods=['GET', 'POST'])
def _export_json():
    res = es.search(index="temp_dict", body={"query": {"match_all": {}},
                    "sort": [{"field_for_sorting": {"order": "asc"}}],
                    "size": 10000})

    all_entries = [hit["_source"] for hit in res['hits']['hits']]

    try:
        create_zip_with_json(all_entries)
        result = "success"
    except:
        result = "failure"

    return flask.jsonify(result=result)


@app.route('/_user_info', methods=['GET', 'POST'])
def user_info():
    user = dict()
    user['logged'] = flask_login.current_user.is_authenticated
    if user['logged']:
        user['name'] = flask_login.current_user.id
    return flask.jsonify(result=user)


if __name__ == '__main__':
    app.run(
        # host="0.0.0.0",
        # port=int("80"),
        debug=True
    )
