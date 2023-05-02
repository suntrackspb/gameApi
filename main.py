import random

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

data = {
    "stars": [
        {
            "id": 1,
            "star": "Брэд Питт",
            "name1": "Бен Аффлек",
            "name2": "Брэдли Купер",
            "name3": "Райан Гослинг"
        },
        {
            "id": 2,
            "star": "Леонардо ДиКаприо",
            "name1": "Джозеф Гордон-Левитт",
            "name2": "Райан Гослинг",
            "name3": "Том Хиддлстон"
        },
        {
            "id": 3,
            "star": "Том Харди",
            "name1": "Хью Джекман",
            "name2": "Райан Гослинг",
            "name3": "Шайа ЛаБаф"
        },
        {
            "id": 4,
            "star": "Марго Робби",
            "name1": "Эмма Уотсон",
            "name2": "Дакота Джонсон",
            "name3": "Кира Найтли"
        },
        {
            "id": 5,
            "star": "Райан Рейнольдс",
            "name1": "Райан Гослинг",
            "name2": "Крис Пратт",
            "name3": "Тайка Вайтити"
        },
        {
            "id": 6,
            "star": "Эмма Стоун",
            "name1": "Зои Дешанель",
            "name2": "Эми Адамс",
            "name3": "Элли Фаннинг"
        },
        {
            "id": 7,
            "star": "Дженнифер Лоуренс",
            "name1": "Эмма Стоун",
            "name2": "Натали Портман",
            "name3": "Кейт Бланшетт"
        },
        {
            "id": 8,
            "star": "Джеймс Франко",
            "name1": "Дэйв Франко",
            "name2": "Тоби Магуайр",
            "name3": "Райан Гослинг"
        },
        {
            "id": 9,
            "star": "Анджелина Джоли",
            "name1": "Мила Кунис",
            "name2": "Кэмерон Диаз",
            "name3": "Оливия Уайлд"
        },
        {
            "id": 10,
            "star": "Джейсон Момоа",
            "name1": "Крис Хемсворт",
            "name2": "Тейлор Китч",
            "name3": "Джерард Батлер"
        }
    ]
}


gamers = {}

gamers_answer = {}


def check_answer(_ans, _id):
    if _ans == data['stars'][_id - 1]['star']:
        return True
    else:
        return False


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/start', methods=['POST'])
def start():
    name = request.get_json()['name']
    category = request.get_json()['category']
    gamers[name] = [x for x in range(1, 11)]
    gamers_answer[name] = [False] * 10
    print(name, category)
    print(gamers)
    print(gamers_answer)
    return jsonify({"status": "ok"})


@app.route('/api/v1/question', methods=['POST'])
def question():
    name = request.get_json()['name']
    if len(gamers[name]) == 0:
        print({"status": "error"})
        return jsonify({"status": "error"})
    _index = random.randint(0, len(gamers[name]) - 1)
    print(gamers)
    print(gamers_answer)
    quest = data['stars'][gamers[name][_index] - 1]
    array = [quest['star'], quest['name1'], quest['name2'], quest['name3']]
    random.shuffle(array)
    obj = {
        "id": quest['id'],
        "names": array
    }

    return jsonify(obj)


@app.route('/api/v1/answer', methods=['POST'])
def answer():
    data = request.get_json()
    print(data)
    answer = data['answer']
    id = data['id']
    name = data['name']
    check = check_answer(answer, id)
    if check:
        gamers_answer[name][id - 1] = True
    gamers[name].remove(id)
    print(f"=== {gamers}")
    print(f"=== {gamers_answer}")
    if len(gamers[name]) == 0:
        return jsonify({"status": "end",  "result": gamers_answer[name]})
    return jsonify(check)


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()
