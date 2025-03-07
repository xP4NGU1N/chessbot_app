import chess
import numpy as np

def extract_giraffe_features(board):
    # Initialize feature vector (351 features) Note: Paper mentioned 363 features
    feature_vector = np.zeros(351, dtype=np.float32)

    # ------------------ GLOBAL FEATURES (15 features) ------------------
    # 1. Side to Move (1 feature) - White = 1, Black = -1
    feature_vector[0] = 1 if board.turn == chess.WHITE else -1 

    # 2. Castling Rights (4 features)
    feature_vector[1] = 1 if board.has_kingside_castling_rights(chess.WHITE) else 0
    feature_vector[2] = 1 if board.has_queenside_castling_rights(chess.WHITE) else 0
    feature_vector[3] = 1 if board.has_kingside_castling_rights(chess.BLACK) else 0
    feature_vector[4] = 1 if board.has_queenside_castling_rights(chess.BLACK) else 0

    # 3. Material Configuration (10 features)
    offset = 5 # start index for material configuration
    piece_types = [chess.PAWN, chess.BISHOP, chess.KNIGHT, chess.ROOK, chess.QUEEN]
    for i, piece_type in enumerate(piece_types): # get the count of each piece remaining, white first then black
        feature_vector[offset+i] = len(board.pieces(piece_type, chess.WHITE))
        feature_vector[offset+i+len(piece_types)] = len(board.pieces(piece_type, chess.BLACK))
    offset += 10
    
    # ------------------ PIECE-CENTRIC FEATURES (208 features) ------------------
    # 4. Piece lists (160 features)
    slots = { chess.PAWN: 8, chess.KNIGHT: 2, chess.BISHOP: 2, chess.ROOK: 2, chess.QUEEN: 1, chess.KING: 1 }
    values = { chess.PAWN: 1, chess.BISHOP: 3, chess.KNIGHT: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 12 } # assume that king is MVP - what points to assign?

    for color in [chess.WHITE, chess.BLACK]: # get piece list for white first then black
        for piece_type, max_slots in slots.items():
            piece_squares = list(board.pieces(piece_type, color)) # get all squares for this piece type
            for i in range(max_slots): # for all remaining piece of this type
                if i < len(piece_squares):
                    # Compute position of piece
                    square = piece_squares[i]
                    feature_vector[offset] = (square%8)/7 # normalise x-coordinate (0-7 → 0-1)
                    feature_vector[offset+1] = (square//8)/7 # normalise y-coordinate (0-7 → 0-1)
                    feature_vector[offset+2] = 1 # piece exists flag
                    # Compute lowest valued attacker & defender, if none then leave as 0
                    attackers = board.attackers(not color, square)
                    defenders = board.attackers(color, square)
                    feature_vector[offset+3] = min([values[board.piece_at(att).piece_type] for att in attackers if att], default=0)
                    feature_vector[offset+4] = min([values[board.piece_at(defn).piece_type] for defn in defenders if defn], default=0)
                else:
                    feature_vector[offset:offset+5] = 0 # empty slot
                offset += 5 # each piece has 5 slots (x, y, exists, attacker, defender)

    # 5. Sliding Pieces Mobility (48 features)
    mobility_slots = { chess.BISHOP: 2, chess.ROOK: 2, chess.QUEEN: 1 }
    # Define directions for sliding pieces
    rook_directions = [8, -8, -1, 1] # Up, Down, Left, Right
    bishop_directions = [7, -9, -7, 9] # NW, SW, SE, NE
    queen_directions = rook_directions + bishop_directions # queen can move in both rook and bishop directions

    # Loop through color and each sliding piece (rook, bishop, queen)
    for color in [chess.WHITE, chess.BLACK]:
        for piece_type, max_slots in mobility_slots.items():
            piece_squares = list(board.pieces(piece_type, color)) # get all squares for this piece type
            # Select directions based on the piece type
            if piece_type == chess.ROOK:
                directions = rook_directions
            elif piece_type == chess.BISHOP:
                directions = bishop_directions
            else:
                directions = queen_directions
            for i in range(max_slots): # for all remaining piece of this type
                if i < len(piece_squares):                        
                    for direction in directions:
                        distance = 0
                        target = square
                        while True:
                            # Calculate the target square in the direction
                            target = target+direction
                            # Check if the target is within bounds (8x8 board)
                            if target < 0 or target >= 64:
                                break
                            # Check if the target square is blocked
                            if board.piece_at(target):
                                break
                            distance += 1
                        
                        # Store the mobility feature for this direction
                        feature_vector[offset] = distance
                        offset += 1
                else:
                    if piece_type == chess.ROOK or piece_type == chess.BISHOP:
                        feature_vector[offset:offset+4] = 0
                        offset += 4
                    else:
                        feature_vector[offset:offset+8] = 0
                        offset += 8

    # ------------------ SQUARE-CENTRIC FEATURES (128 features) ------------------
    # 6. Attack and Defend Maps (128 features)
    for square in chess.SQUARES:
        if board.turn == chess.WHITE: # if it is white turn, we want to know which black pieces are attacking the square
            attackers = board.attackers(chess.BLACK, square) 
            defenders = board.attackers(chess.WHITE, square)
        else:
            attackers = board.attackers(chess.WHITE, square)
            defenders = board.attackers(chess.BLACK, square)
        feature_vector[offset] = min([values[board.piece_at(att).piece_type] for att in attackers if att], default=0)
        feature_vector[offset+1] = min([values[board.piece_at(defn).piece_type] for defn in defenders if defn], default=0)
        offset += 2
        
    return feature_vector

def split_giraffe_features(X):
    global_feature_count = 15
    piece_centric_feature_count = 208

    global_features = X[:, :global_feature_count]
    piece_centric_features = X[:, global_feature_count:global_feature_count+piece_centric_feature_count]
    square_centric_features = X[:, global_feature_count+piece_centric_feature_count:]

    return global_features, piece_centric_features, square_centric_features

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
