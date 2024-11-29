from flask import Flask, request, jsonify
from parser import evaluate_expression 
import os
app = Flask(__name__)

data_store = {}


@app.route('/getall', methods=['GET'])
def get_all_files():
    dir_list = os.listdir('files')
    names = [_.split('.')[0] for _ in dir_list]
    result = list()
    for name in names:
        cur = dict()
        cur["name"] = name
        with open('files/' + name + '.txt', 'r') as file:
            cur['text'] = file.read()
        result.append(cur)
    return jsonify({'result': result}), 200
@app.route('/send', methods=['POST'])
def send_data():
    try:
        # Получаем данные из запроса
        name = request.json.get('name')
        text = request.json.get('text')

        if not name or not text:
            return jsonify({'error': 'Name and text fields are required'}), 400

        # Сохраняем данные в хранилище
        #data_store[name] = text
        with open("files/" + name + ".txt", 'w') as file:
            file.write(text)
        return jsonify({'message': 'Data saved successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get/<string:name>', methods=['GET'])
def get_data(name):
    try:
        # Получаем текст по имени из хранилища
        result = ""
        with open("files/" + name + ".txt", 'r') as file:
            result = file.read()

        return result

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_request():
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        data = request.get_json()
        
        # Вызываем функцию с полученными данными
        result = evaluate_expression(data)
        
        # Возвращаем результат в виде JSON-ответа
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
