package service

import (
	"fmt"
	"net/http"
	"bytes"
	"encoding/json"

	"chessapp/model"
)

func GetBestMove(moveRequest model.UnratedPosition) (model.SuggestedMove, error) {
	// Get best move from Flask
	move, err := GetBestMoveFromFlask(moveRequest.FEN, moveRequest.Model)
	if err != nil {
		return model.SuggestedMove{}, fmt.Errorf("error getting best move: %v", err)
	}
	bestMove := model.SuggestedMove{
		Model:  moveRequest.Model,
		Move:   move,
	}
	return bestMove, nil
}

func GetBestMoveFromFlask(fen string, modelName string) (string, error) {
	// Create the data to send to Flask server
	data := map[string]string{
		"fen":        fen,
		"model_name": modelName,
	}

	// ensure data to Flask is correctly formatted
	jsonData, err := json.Marshal(data)
	if err != nil {
		return "", fmt.Errorf("error marshalling data: %v", err)
	}

	// Make a POST request to Flask server
	resp, err := http.Post("http://localhost:5000/best_move", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("error calling Flask server: %v", err)
	}
	defer resp.Body.Close()

	// Parse the response from Flask server
	var response model.SuggestedMove
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return "", fmt.Errorf("error decoding response: %v", err)
	}

	// Validate that board state and model passed to Flask match the expected values
	if response.Model != modelName {
		return "", fmt.Errorf("mismatch in model name returned by Flask server (expected: %s, got: %s)", modelName, response.Model)
	}

	return response.Move, nil
}