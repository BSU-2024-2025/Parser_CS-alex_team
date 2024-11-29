from flask import Flask, request, jsonify
from parser import evaluate_expression 
app = Flask(__name__)

data_store = {}


@app.route('/send', methods=['POST'])
def send_data():
    try:
        # Получаем данные из запроса
        name = request.json.get('name')
        text = request.json.get('text')

        if not name or not text:
            return jsonify({'error': 'Name and text fields are required'}), 400

        # Сохраняем данные в хранилище
        data_store[name] = text
        return jsonify({'message': 'Data saved successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get/<string:name>', methods=['GET'])
def get_data(name):
    try:
        # Получаем текст по имени из хранилища
        text = data_store.get(name)

        if text is None:
            return jsonify({'error': 'No data found for the given name'}), 404

        return jsonify({'name': name, 'text': text}), 200

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

