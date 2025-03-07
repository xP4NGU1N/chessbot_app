package controller

import (
	"net/http"

	"chessapp/service"
	"chessapp/model"
	"github.com/gin-gonic/gin"
)

func GetCurrentPosition(c *gin.Context) {
	currentPosition, err := service.GetCurrentPosition()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, currentPosition)
}

func UndoMove(c *gin.Context) {
	var undoMoveRequest model.CycleMoveRequest
	if err := c.BindJSON(&undoMoveRequest); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	newPosition, err := service.UndoMove(undoMoveRequest)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, newPosition)
}

func RedoMove(c *gin.Context) {
	var redoMoveRequest model.CycleMoveRequest
	if err := c.BindJSON(&redoMoveRequest); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	newPosition, err := service.RedoMove(redoMoveRequest)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusCreated, newPosition)
}

func ResetGame(c *gin.Context) {
	startingPosition, err := service.ResetGame()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusCreated, startingPosition)
}

func ExportGame(c *gin.Context) {
	game_pgn, err := service.ExportGamePGN()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, gin.H{"pgn": game_pgn})
}

func GetAllPositions(c *gin.Context) {
	allPositions := service.GetAllPositions()

	c.IndentedJSON(http.StatusOK, allPositions)
}