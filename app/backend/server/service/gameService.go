package service

import (
	"fmt"
	"time"

	"github.com/corentings/chess/v2"
	"chessapp/repository"
	"chessapp/model"
)

var currentGame *chess.Game
var positionRepo *repository.PositionRepository

// automatically starts when package is initialised
func init() {
	ResetGame()
}

func ResetGame() (model.Position, error) {
	currentGame = chess.NewGame()
	currentGame.AddTagPair("Event", "Local Game")
	currentGame.AddTagPair("Site", "Local")
	currentGame.AddTagPair("Date", time.Now().Format("2006.01.02"))
	startingRating, err := GetEvaluation(currentGame.FEN(), "Giraffe")
	if err != nil {
		startingRating = 0
	}
	positionRepo = repository.NewPositionRepository(currentGame.FEN(), startingRating)

	startingPosition, err := positionRepo.GetLatestPosition()
	if err != nil {
		return model.Position{}, fmt.Errorf("invalid move: %v", err)
	}

	return startingPosition, nil
}

func GetCurrentPosition() (model.Position, error) {
	currentPosition, err := positionRepo.GetLatestPosition()
	if err != nil {
		return model.Position{}, fmt.Errorf("error getting position: %v", err)
	}

	return currentPosition, nil
}

func ExportGamePGN() (string, error) {
	// Check if the game has moves
	if len(currentGame.Moves()) == 0 {
		return "", fmt.Errorf("no moves recorded")
	}
	// Add the game result before exporting
	currentGame.AddTagPair("Result", currentGame.Outcome().String())

	return currentGame.String(), nil
}

func GetAllPositions() ([]model.Position) {
	allPositions := positionRepo.GetAllPositions()

	return allPositions
}