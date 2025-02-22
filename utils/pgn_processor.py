import os
import random
import chess.pgn
from stockfish import Stockfish

import chess
import chess.engine


STOCKFISH_PATH = "C:\\Users\\User\\Downloads\\stockfish\\stockfish-windows-x86-64-avx2" # windows
# STOCKFISH_PATH = "/opt/homebrew/bin/stockfish" # mac

# Initialize Stockfish engine
# Define the parameters for Stockfish
parameters = {
    "Threads": 12,
    "Hash": 256,
    "UCI_LimitStrength": True, # limit strength using Elo rating
    "UCI_Elo": 2800
}

# Initialize Stockfish with the given parameters
stockfish = Stockfish(path=STOCKFISH_PATH, parameters=parameters)

# Function to collect all unique FENs from PGN files
def pgn_to_fen(pgn_folder):
    unique_positions = set() # to ensure uniqueness of positions
    for filename in os.listdir(pgn_folder):
        if filename.endswith(".PGN"):
            filepath = os.path.join(pgn_folder, filename)
            with open(filepath, "r") as pgn_file:
                while True: # read multiple games in a single PGN file
                    try:
                        game = chess.pgn.read_game(pgn_file)
                        if game is None:
                            break
                        board = game.board()
                        for move in game.mainline_moves():
                            board.push(move)
                            fen = board.fen()
                            unique_positions.add(fen) # collect all unique FENs
                    except Exception as e:
                        print(f"Error processing a game in {filename}: {e}")
                        break # skip the rest of this file if an error occurs
    return list(unique_positions)

# Function to collect FENs from PGN files with exact outcomes
def pgn_to_fen_excl_draw(pgn_folder):
    extracted_games = []
    for filename in os.listdir(pgn_folder):
        if filename.endswith(".PGN") or filename.endswith(".pgn"):
            filepath = os.path.join(pgn_folder, filename)
            with open(filepath, "r", encoding="utf-8") as pgn_file:
                while True:
                    try:
                        game = chess.pgn.read_game(pgn_file)
                        if game is None:
                            break
                        result = game.headers.get("Result", "") # get game result
                        if result == "1-0":
                            label = 1 # white won
                        elif result == "0-1":
                            label = 0 # black won
                        else:
                            continue # skip drawn games
                        board = game.board()
                        game_data = { "fens": [], "captures": [], "label": label } # store game data

                        for move in game.mainline_moves():
                            game_data["captures"].append(board.is_capture(move)) # check before pushing the move
                            board.push(move)
                            game_data["fens"].append(board.fen()) # store FEN after move is made
                        extracted_games.append(game_data)

                    except Exception as e:
                        print(f"Error processing a game in {filename}: {e}")
                        break # skip the rest of this file if an error occurs
    return extracted_games # return list of games with moves, FENs, and labels

# Function to select a random sample of FENs
def select_random_fens(fens, num_positions):
    # Randomly select 'num_positions' from the list of FENs
    return random.sample(fens, num_positions)

# Function to analyze a position
# returns a static evaluation of the position from the point of view of the side to move
def analyze_position(fen):
    stockfish.set_fen_position(fen)
    stockfish.set_depth(5)
    return stockfish.get_evaluation() # returns dict: {"type": "cp" or "mate", "value": number}