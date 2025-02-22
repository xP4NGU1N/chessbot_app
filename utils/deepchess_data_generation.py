import numpy as np
import os
from deepchess_feature_extraction import process_pgn_folder

PGN_FOLDER = "./../strong_chess_players"
OUTPUT_FOLDER = "./dataset"
SAMPLE_SIZE = 1000000

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

bitboard_positions, labels = process_pgn_folder(PGN_FOLDER)

# Filter positions for white win and black win
white_win_indices = np.where(labels == 1)[0]
black_win_indices = np.where(labels == 0)[0]

# Shuffle indices
np.random.shuffle(white_win_indices)
np.random.shuffle(black_win_indices)

# Select a random sample
white_win_sample = white_win_indices[:SAMPLE_SIZE]
black_win_sample = black_win_indices[:SAMPLE_SIZE]

# Extract sampled positions and labels
sampled_positions = np.concatenate([bitboard_positions[white_win_sample], bitboard_positions[black_win_sample]])
sampled_labels = np.concatenate([labels[white_win_sample], labels[black_win_sample]])
print(f"Shape of sampled_positions: {sampled_positions.shape}")
print(f"Shape of sampled_labels: {sampled_labels.shape}")

np.save(os.path.join(OUTPUT_FOLDER, "deepchess_bitboard_positions.npy"), sampled_positions)
np.save(os.path.join(OUTPUT_FOLDER, "deepchess_labels.npy"), sampled_labels)