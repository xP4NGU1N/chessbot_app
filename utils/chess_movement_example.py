import chess

def test_chess_movement():
    print("Chess Board Square Indexing:\n")
    print("    A  B  C  D  E  F  G  H")
    print("   -------------------------")

    for rank in range(8):
        rank_number = 8 - rank # ranks go from 8 (top) to 1 (bottom)
        row = [f"{rank_number} |"] 

        for file in range(8):
            square = chess.square(file, 7 - rank) # convert file/rank to 0-63 index
            row.append(f"{square:2}") # format square index with spacing

        print(" ".join(row))

    print("\nMovement Examples:")
    
    center_square = chess.E4 # E4 is a central square (index 28)
    print(f"E4 index: {center_square} (square: {chess.square_name(center_square)})")
    move_up = center_square + 8 # move up to E5
    print(f"Move Up (+8): {move_up} (square: {chess.square_name(move_up)})")
    move_down = center_square - 8 # move down to E3
    print(f"Move Down (-8): {move_down} (square: {chess.square_name(move_down)})")
    move_right = center_square + 1 # move right to F4
    print(f"Move Right (+1): {move_right} (square: {chess.square_name(move_right)})")
    move_left = center_square - 1 # move left to D4
    print(f"Move Left (-1): {move_left} (square: {chess.square_name(move_left)})")

test_chess_movement()
