from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Получаем абсолютный путь к файлу data.json
data_file = os.path.join(os.path.dirname(__file__), 'data.json')

# Функция для загрузки данных голосования
def load_data():
    try:
        print(f"Пытаемся открыть файл: {data_file}")
        with open(data_file, 'r') as f:
            print(f"Файл успешно открыт!")
            return json.load(f)
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден: {e}")
    except Exception as e:
        print(f"Другая ошибка: {e}")
    return {}

# Функция для сохранения данных голосования
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Обрабатываем голосование
        feature = request.form['feature']  # Получаем выбранную пользователем функцию
        data = load_data()

        if feature in data:
            data[feature] += 1  # Увеличиваем количество голосов за выбранную функцию
        else:
            data[feature] = 1  # Если такой функции еще нет, добавляем её в список

        save_data(data)  # Сохраняем обновленные данные голосования
        return redirect(url_for('index'))
    
    data = load_data()  # Загружаем данные для отображения на главной странице
    return render_template("index.html", data=data)  # Передаем данные в шаблон

@app.route('/vote', methods=['POST'])
def vote():
    feature = request.form['feature']  # Получаем выбранную пользователем функцию
    data = load_data()

    if feature in data:
        data[feature] += 1  # Увеличиваем количество голосов за выбранную функцию
    else:
        data[feature] = 1  # Если такой функции еще нет, добавляем её в список

    save_data(data)  # Сохраняем обновленные данные голосования
    return redirect(url_for('index'))

#@app.route('/results')
#def results():
#    data = load_data()
#    return jsonify(data)  # Возвращаем результаты голосования в формате JSON

if __name__ == '__main__':
    app.run(debug=True)
