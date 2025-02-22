import random
import numpy as np
from .pgn_processor import pgn_to_fen_excl_draw

NUM_POSITIONS = 40 # number of positions to extract per game
MOVES_THRESHOLD = 5 # don't select from the first 5 moves
CAPTURE_MOVE = "x" # Capture move symbol in standard algebraic notation

# Function to convert FEN to 773-bit binary string
def fen_to_bitboard(fen):
    # Bitboard representation: 768 bits for pieces, 5 additional bits for side to move and castling rights
    bitboard = np.zeros(773, dtype=np.int8)

    # Split FEN into components (board, side, castling rights, etc.)
    # Example FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    parts = fen.split(' ')
    board, side_to_move, castling_rights, _ = parts[:4]

    # Map pieces to bitboard (binary representation)
    # 1 board (8x8) for each piece type for each side - then the '1's for each board will reflect where the pieces for that board are: 
    # Mapping of indices:
        # 0-63: White Pawns
        # 64-127: White Knights
        # 128-191: White Bishops
        # 192-255: White Rooks
        # 256-319: White Queens
        # 320-383: White King
        # 384-447: Black Pawns
        # 448-511: Black Knights
        # 512-575: Black Bishops
        # 576-639: Black Rooks
        # 640-703: Black Queens
        # 704-767: Black King
        # 768: Side to move (1 for White, 0 for Black)
        # 769-772: Castling rights (White Kingside, White Queenside, Black Kingside, Black Queenside)
        
    # Piece to bitboard index mapping
    piece_to_index = {
        'P': 0,  'N': 1,  'B': 2,  'R': 3,  'Q': 4,  'K': 5, # white pieces
        'p': 6,  'n': 7,  'b': 8,  'r': 9,  'q': 10, 'k': 11 # black pieces
    }    

    # Parse board representation
    row, col = 0, 0
    for char in board:
        if char == '/':
            row += 1 # move to the next row
            col = 0 # reset column
        elif char.isdigit():
            col += int(char) # skip empty squares
        else:
            piece_index = piece_to_index[char] # get the corresponding bitboard index
            square_index = row * 8 + col # convert (row, col) to 0-63 index
            bitboard[piece_index * 64 + square_index] = 1
            col += 1 # move to the next column

    # Set the side to move
    bitboard[768] = 1 if side_to_move == 'w' else 0

    # Set castling rights (1 for yes, 0 for no)
    bitboard[769] = 1 if 'K' in castling_rights else 0 # white kingside
    bitboard[770] = 1 if 'Q' in castling_rights else 0 # white queenside
    bitboard[771] = 1 if 'k' in castling_rights else 0 # black kingside
    bitboard[772] = 1 if 'q' in castling_rights else 0 # black queenside

    return bitboard

# Function to check if a move is a capture
def is_capture(move):
    return CAPTURE_MOVE in move

# Function to process a game and extract valid positions
def extract_positions(game):
    captures = game['captures']
    valid_positions = []

    # Skip the first 5 moves and make sure no capture move is selected
    for i in range(MOVES_THRESHOLD, len(captures)):
        capture = captures[i]
        if not capture:
            # Generate the FEN for the current position
            position_fen = game['fens'][i] # `game['fens'][i]` gives the FEN after this move
            valid_positions.append(position_fen)
    
    # Randomly select 10 positions
    selected_positions = random.sample(valid_positions, min(NUM_POSITIONS, len(valid_positions)))
    return [(fen, game['label']) for fen in selected_positions]

# Function to process all PGNs in the folder and convert positions to bitboard format
def process_pgn_folder(pgn_folder):
    games = pgn_to_fen_excl_draw(pgn_folder) # collect all unique FENs
    # Store positions in bitboard format
    bitboard_positions = []
    labels = []
    for game in games:
        selected_positions = extract_positions(game)
        for fen, label in selected_positions:
            bitboard = fen_to_bitboard(fen)
            bitboard_positions.append(bitboard)
            labels.append(label)
    return np.array(bitboard_positions), np.array(labels)

# Example usage of fen_to_bitboard with a test FEN
#test_fen = "rnbqkb1r/pppppppp/5n2/8/8/5N2/PPPPPPPP/RNBQKB1R w KQkq - 0 3"
#bitboard_representation = fen_to_bitboard(test_fen)
#print("Bitboard Representation: ", bitboard_representation)