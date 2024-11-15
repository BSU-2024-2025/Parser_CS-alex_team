from flask import Flask, request, jsonify
from parser import evaluate_expression
app = Flask(__name__)

def example_function(data):
    # Ваша логика обработки данных здесь, например:
    result = {"message": f"Hello, {data['name']}!"}
    return result

@app.route('/process', methods=['POST'])
def process_request():
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        data = request.get_json()
        
        # Вызываем функцию с полученными данными
        result = evaluate_expression(data["expression"])
        
        # Возвращаем результат в виде JSON-ответа
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

