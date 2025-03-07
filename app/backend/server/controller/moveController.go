package controller

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"chessapp/model"
	"chessapp/service"
)

func MakeMove(c *gin.Context) {
	var newMove model.Move
	if err := c.BindJSON(&newMove); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	// Apply the move and get evaluation from service
	updatedPosition, err := service.ApplyMove(newMove)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusCreated, updatedPosition)
}

func EvaluatePosition(c *gin.Context) {
	var unratedPosition model.UnratedPosition
	if err := c.BindJSON(&unratedPosition); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	updatedPosition, err := service.GetNewEvaluation(unratedPosition.FEN, unratedPosition.Model)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, updatedPosition)
}

func GetBestMove(c *gin.Context) {
	var moveRequest model.UnratedPosition
	if err := c.BindJSON(&moveRequest); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	// get move suggestion from service
	bestMove, err := service.GetBestMove(moveRequest)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	c.IndentedJSON(http.StatusOK, bestMove)
}