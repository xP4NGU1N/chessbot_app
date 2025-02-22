import numpy as np

def split_features(X):
    global_feature_count = 15
    piece_centric_feature_count = 208

    global_features = X[:, :global_feature_count]
    piece_centric_features = X[:, global_feature_count:global_feature_count+piece_centric_feature_count]
    square_centric_features = X[:, global_feature_count+piece_centric_feature_count:]

    return global_features, piece_centric_features, square_centric_features

def load_and_split_data(file_path, train_ratio=0.6, val_ratio=0.2, random_seed=42):
    np.random.seed(random_seed)

    # Load dataset
    data = np.load(file_path)
    features = data["features"]
    labels = data["labels"]

    # Shuffle indices
    total_size = len(features)
    indices = np.random.permutation(total_size)

    # Compute split sizes
    train_size = int(train_ratio*total_size)
    val_size = int(val_ratio*total_size)

    # Assign indices
    train_indices = indices[:train_size]
    val_indices = indices[train_size:train_size+val_size]
    test_indices = indices[train_size+val_size:]

    # Split data
    X_train, y_train = features[train_indices], labels[train_indices]
    X_val, y_val = features[val_indices], labels[val_indices]
    X_test, y_test = features[test_indices], labels[test_indices]

    # Split features into modules
    X_train_split = split_features(X_train)
    X_val_split = split_features(X_val)
    X_test_split = split_features(X_test)

    return (X_train_split, y_train), (X_val_split, y_val), (X_test_split, y_test)

def preview_data_shapes(train_data, val_data, test_data):
    (X_train_global, X_train_piece, X_train_square), y_train = train_data
    (X_val_global, X_val_piece, X_val_square), y_val = val_data
    (X_test_global, X_test_piece, X_test_square), y_test = test_data

    # Print feature shapes
    print("======================== Train Set ========================")
    print("Global Features Shape:", X_train_global.shape)
    print("Piece-Centric Features Shape:", X_train_piece.shape)
    print("Square-Centric Features Shape:", X_train_square.shape)
    print("Labels Shape:", y_train.shape)

    # Preview a random sample from the train data
    random_index_train = np.random.randint(0, len(X_train_global))
    print("\nRandom Train Sample:")
    print("Global Features:", X_train_global[random_index_train])
    print("Piece-Centric Features:", X_train_piece[random_index_train])
    print("Square-Centric Features:", X_train_square[random_index_train])
    print("Label:", y_train[random_index_train])

    print("\n======================== Validation Set ========================")
    print("Global Features Shape:", X_val_global.shape)
    print("Piece-Centric Features Shape:", X_val_piece.shape)
    print("Square-Centric Features Shape:", X_val_square.shape)
    print("Labels Shape:", y_val.shape)

    # Preview a random sample from the validation data
    random_index_val = np.random.randint(0, len(X_val_global))
    print("\nRandom Validation Sample:")
    print("Global Features:", X_val_global[random_index_val])
    print("Piece-Centric Features:", X_val_piece[random_index_val])
    print("Square-Centric Features:", X_val_square[random_index_val])
    print("Label:", y_val[random_index_val])

    print("\n======================== Test Set ========================")
    print("Global Features Shape:", X_test_global.shape)
    print("Piece-Centric Features Shape:", X_test_piece.shape)
    print("Square-Centric Features Shape:", X_test_square.shape)
    print("Labels Shape:", y_test.shape)

    # Preview a random sample from the test data
    random_index_test = np.random.randint(0, len(X_test_global))
    print("\nRandom Test Sample:")
    print("Global Features:", X_test_global[random_index_test])
    print("Piece-Centric Features:", X_test_piece[random_index_test])
    print("Square-Centric Features:", X_test_square[random_index_test])
    print("Label:", y_test[random_index_test])

# Test
#train_data, val_data, test_data = load_and_split_data("./dataset/chess_dataset.npz")
#(X_train_global, X_train_piece, X_train_square), y_train = train_data
#(X_val_global, X_val_piece, X_val_square), y_val = val_data
#(X_test_global, X_test_piece, X_test_square), y_test = test_data

#print("Train Global Features:", X_train_global.shape)
#print("Validation Piece-Centric Features:", X_val_piece.shape)
#print("Test Square-Centric Features:", X_test_square.shape)



