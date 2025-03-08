from utils import extract_giraffe_features, split_giraffe_features, fen_to_bitboard
from model_architecture import GiraffeOriginal, GiraffeWithTransformer, FinalPos2Vec
import chess
import torch

layer_sizes = [773, 600, 400, 200, 100]
pos2vec = FinalPos2Vec(layer_sizes)
pos2vec.load_state_dict(torch.load("models/Pos2Vec_autoencoder.pth", weights_only=True))
models = {
    "Giraffe": GiraffeOriginal(global_dim=15, piece_dim=208, square_dim=128, global_nodes=12, piece_nodes=64, square_nodes=24, fc_nodes=64, dropout_rate=0.4),
    "Giraffe with Transformer": GiraffeWithTransformer(pos2vec=pos2vec)
}
models["Giraffe"].load_state_dict(torch.load("models/final_giraffe_model.pth", map_location=torch.device("cpu"), weights_only=True))
models["Giraffe with Transformer"].load_state_dict(torch.load("models/transformer_model.pth", map_location=torch.device("cpu"), weights_only=True))

def evaluate_position(model_name, board):
    model = models[model_name]
    model.eval()

    if model_name == "Giraffe":
        x_g, x_p, x_s = (split_giraffe_features(torch.tensor(extract_giraffe_features(board).reshape(1, -1), dtype=torch.float32)))
        with torch.no_grad():
            return model(x_g, x_p, x_s).squeeze().item()
        
    elif model_name == "Giraffe with Transformer":
        x = torch.tensor(fen_to_bitboard(board.fen()).reshape(1, -1), dtype=torch.float32)
        with torch.no_grad():
            return model(x).item()
    
    return None

def get_best_move(model_name, board):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    
    model = models[model_name]
    model.eval()

    if model_name == "Giraffe":
        giraffe_features = []
        for move in legal_moves:
            board.push(move)
            giraffe_feature = extract_giraffe_features(board)
            giraffe_features.append(torch.tensor(giraffe_feature, dtype=torch.float32))
            board.pop()
        X = torch.stack(giraffe_features)
        X_g, X_p, X_s = split_giraffe_features(X)
        with torch.no_grad():
            scores = model(X_g, X_p, X_s).squeeze()
        best_idx = torch.argmax(scores).item() if board.turn == chess.WHITE else torch.argmin(scores).item()
        return board.san(legal_moves[best_idx])
    
    elif model_name == "Giraffe with Transformer":
        giraffe_features = []
        for move in legal_moves:
            board.push(move)
            giraffe_feature = torch.tensor(fen_to_bitboard(board.fen()), dtype=torch.float32)
            giraffe_features.append(giraffe_feature)
            board.pop()
        X = torch.stack(giraffe_features)
        with torch.no_grad():
            scores = model(X).squeeze()
        best_idx = torch.argmax(scores).item() if board.turn == chess.WHITE else torch.argmin(scores).item()
        return board.san(legal_moves[best_idx])
    
    return None