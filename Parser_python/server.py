from flask import Flask, request, jsonify
from parser import evaluate_expression
app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_request():
    if request.method == 'POST':
        data = request.get_json()
        
        result = evaluate_expression(data["expression"])
        
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

