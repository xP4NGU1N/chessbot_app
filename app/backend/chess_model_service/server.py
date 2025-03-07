from flask import Flask, request, jsonify
from model_eval import evaluate_position, get_best_move, models
import chess


app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    fen = data.get("fen", "")
    model_name = data.get("model_name", "Giraffe")

    if not fen:
        return jsonify({"error": "FEN string required"}), 400
    if model_name not in models:
        return jsonify({"error": f"Invalid model name: {model_name}"}), 400

    board = chess.Board(fen)
    rating = evaluate_position(model_name, board)

    return jsonify({"fen": fen, "model_name": model_name, "rating": rating})

@app.route('/best_move', methods=['POST'])
def best_move():
    data = request.get_json()
    fen = data.get("fen", "")
    model_name = data.get("model_name", "Giraffe")

    if not fen:
        return jsonify({"error": "FEN string required"}), 400
    if model_name not in models:
        return jsonify({"error": f"Invalid model name: {model_name}"}), 400

    board = chess.Board(fen)
    best_move = get_best_move(model_name, board)

    return jsonify({"model_name": model_name, "move": best_move})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) # '0.0.0.0' to broadcast
