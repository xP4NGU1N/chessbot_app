package repository

import (
	"errors"
	
	"chessapp/model"
)

// PositionRepository stores game positions
type PositionRepository struct {
	positions []model.Position
}

// NewPositionRepository initializes a repository with the starting position
func NewPositionRepository(startFEN string, startRating float64) *PositionRepository {
	return &PositionRepository{
		positions: []model.Position{
			{FEN: startFEN, Model: "Giraffe with Deepchess", Rating: startRating},
		},
	}
}

// AddPosition stores a new position
func (repo *PositionRepository) AddPosition(pos model.Position) {
	repo.positions = append(repo.positions, pos)
}

// GetLatestPosition returns the latest position
func (repo *PositionRepository) GetLatestPosition() (model.Position, error) {
	if len(repo.positions) == 0 {
		return model.Position{}, errors.New("no positions available")
	}
	return repo.positions[len(repo.positions)-1], nil
}

// UpdateLastPosition updates the most recent position
func (repo *PositionRepository) UpdateLastPosition(updatedPos model.Position) error {
	if len(repo.positions) == 0 {
		return errors.New("no positions to update")
	}
	// Update the latest position
	repo.positions[len(repo.positions)-1] = updatedPos
	return nil
}

// RemoveLastPosition removes the most recent position
func (repo *PositionRepository) RemoveLastPosition() error {
	if len(repo.positions) == 0 {
		return errors.New("no positions to remove")
	}
	repo.positions = repo.positions[:len(repo.positions)-1]
	return nil
}

// GetAllPositions returns the full move history
func (repo *PositionRepository) GetAllPositions() []model.Position {
	return repo.positions
}
