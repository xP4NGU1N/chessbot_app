package service

import (
	"fmt"

	"chessapp/model"
)

func UndoMove(undoMoveReq model.CycleMoveRequest) (model.Position, error) {
	// returns false if cannot go back
	if !currentGame.GoBack() {
		return model.Position{}, fmt.Errorf("no move to undo")
	}

	err := positionRepo.RemoveLastPosition()
	if err != nil {
		return model.Position{}, fmt.Errorf("error removing last move: %v", err)	
	}

	lastPosition, err := positionRepo.GetLatestPosition()
	if err != nil {
		currentGame.GoForward()
		return model.Position{}, fmt.Errorf("error getting last move: %v", err)	
	}

	if lastPosition.Model == undoMoveReq.Model {
		return lastPosition, nil
	}

	newRating, err := GetEvaluation(currentGame.FEN(), undoMoveReq.Model)
	if err != nil {
		currentGame.GoForward()
		return model.Position{}, fmt.Errorf("error evaluating prev position: %v", err)
	}

	newPosition := model.Position{
		FEN:    lastPosition.FEN,
		Model:  undoMoveReq.Model,
		Rating: newRating,
	}
	
	err = positionRepo.UpdateLastPosition(newPosition)
	if err != nil {
		currentGame.GoForward()
		return model.Position{}, fmt.Errorf("error updating prev position: %v", err)
	}

	return newPosition, nil
}

func RedoMove(redoMoveReq model.CycleMoveRequest) (model.Position, error) {
	// returns false if cannot go forward (i.e. did not undo previously)
	if !currentGame.GoForward() {
		return model.Position{}, fmt.Errorf("no move to redo")
	}

	updatedFEN := currentGame.FEN()

	rating, err := GetEvaluation(updatedFEN, redoMoveReq.Model)
	if err != nil {
		currentGame.GoBack()
		return model.Position{}, fmt.Errorf("error evaluating position: %v", err)
	}

	updatedPosition := model.Position{
		FEN:    updatedFEN,
		Model:  redoMoveReq.Model,
		Rating: rating,
	}

	positionRepo.AddPosition(updatedPosition)

	return updatedPosition, nil
}