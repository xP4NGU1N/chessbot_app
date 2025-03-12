from pgn_processor import pgn_to_fen, select_random_fens, analyze_position
from giraffe_feature_extraction import extract_giraffe_features
import os
import numpy as np
import chess

PGN_FOLDER = "./../strong_chess_players" # relative to code folder
OUTPUT_FOLDER = "./dataset" # relative to code folder

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Lists to store features and labels
features_list = []
labels_list = []

fens = pgn_to_fen(PGN_FOLDER) # collect all unique FENs
random_fens = select_random_fens(fens, 1000000) # select 1,000,000 random FENs
print("Done extracting games as FENs.")
for i, fen in enumerate(random_fens):
    # Status update
    if (i+1) % 50000 == 0:
        print(f"Processed {i+1}/{len(random_fens)} FENs...")
    score = analyze_position(fen) # get Stockfish analysis for the FEN (score)
    # Convert evaluation to win probability
    if score["type"] == "mate":
        win_prob = 1.0 if score["value"] > 0 else 0.0 # mate is a forced win/loss
    elif score["type"] == "cp":
        cp = score["value"]/100
        win_prob = 1/(1+10**(-cp/4)) # convert Stockfish score into win probability (https://www.chessprogramming.org/Pawn_Advantage,_Win_Percentage,_and_Elo)

    # Extract the Giraffe features for the board state
    board = chess.Board(fen)
    # Convert score to range of -1 to 1
    win_prob = 2*win_prob-1 # -1 represents black win, 1 represents white win
    features = extract_giraffe_features(board)
    
    features_list.append(features)
    labels_list.append(win_prob)

# Convert to NumPy arrays for efficient storage
features_array = np.array(features_list, dtype=np.float32) # shape: (1000000, 351)
labels_array = np.array(labels_list, dtype=np.float32) # shape: (1000000,)

# Save the data as a NumPy file
np.savez(os.path.join(OUTPUT_FOLDER, "giraffe_chess_dataset.npz"), features=features_array, labels=labels_array)

# test
data = np.load("./dataset/giraffe_chess_dataset.npz")
features = data["features"]
labels = data["labels"]
print("Features shape:", features.shape)
print("Labels shape:", labels.shape)
