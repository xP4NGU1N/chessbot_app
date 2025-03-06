package service

import (
	"fmt"
	"net/http"
	"bytes"
	"encoding/json"

	"chessapp/model"
)

// ApplyMove applies a move, updates the state, and stores it
func ApplyMove(newMove model.Move) (model.Position, error) {
	// Apply the move to the game and check if valid move
	if err := currentGame.PushMove(newMove.Move, nil); err != nil {
		return model.Position{}, fmt.Errorf("invalid move: %v", err)
	}

	// Get updated FEN
	updatedFEN := currentGame.FEN()

	// Get evaluation
	rating, err := GetEvaluation(updatedFEN, newMove.Model)
	if err != nil {
		currentGame.GoBack() // Undo move if evaluation fails
		return model.Position{}, fmt.Errorf("error getting evaluation: %v", err)
	}

	// Create new position
	updatedPosition := model.Position{
		FEN:    updatedFEN,
		Model:  newMove.Model,
		Rating: rating,
	}

	// Add the new position
	positionRepo.AddPosition(updatedPosition)

	return updatedPosition, nil
}

func GetNewEvaluation(fen string, modelName string) (model.Position, error) {
	rating, err := GetEvaluation(fen, modelName)
	if err != nil {
		return model.Position{}, fmt.Errorf("error getting evaluation: %w", err)
	}

	updatedPosition := model.Position{
		FEN:    fen,
		Model:	modelName,
		Rating:	rating,
	}
	err = positionRepo.UpdateLastPosition(updatedPosition)
	if err != nil {
		return model.Position{}, fmt.Errorf("error getting evaluation: %w", err)
	}

	return updatedPosition, nil
}

func GetEvaluation(fen string, model string) (float64, error) {
	// Call external Flask service to get evaluation
	rating, err := GetRatingFromFlask(fen, model)
	if err != nil {
		return 0, fmt.Errorf("error getting evaluation: %w", err)
	}
	return rating, nil
}

// GetRatingFromFlask calls the Flask server for evaluation
func GetRatingFromFlask(fen string, modelName string) (float64, error) {
	// Create the data to send to Flask server
	data := map[string]string{
		"fen":        fen,
		"model_name": modelName,
	}

	// ensure data to Flask is correctly formatted
	jsonData, err := json.Marshal(data)
	if err != nil {
		return 0, fmt.Errorf("error marshalling data: %v", err)
	}

	// Make a POST request to Flask server
	resp, err := http.Post("http://localhost:5000/evaluate", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return 0, fmt.Errorf("error calling Flask server: %v", err)
	}
	defer resp.Body.Close()

	// Parse the response from Flask server
	var response model.Position
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return 0, fmt.Errorf("error decoding response: %v", err)
	}

	// Validate that board state and model passed to Flask match the expected values
	if response.Model != modelName {
		return 0, fmt.Errorf("mismatch in model name returned by Flask server (expected: %s, got: %s)", modelName, response.Model)
	}
	if response.FEN != fen {
		return 0, fmt.Errorf("mismatch in FEN returned by Flask server (expected: %s, got: %s)", fen, response.FEN)
	}

	return response.Rating, nil
}
