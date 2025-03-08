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
    fen := c.DefaultQuery("fen", "")
    model := c.DefaultQuery("model_name", "")

    // Validate the query parameters
    if fen == "" || model == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "FEN and model_name are required"})
        return
    }

	updatedPosition, err := service.GetNewEvaluation(fen, model)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, updatedPosition)
}

func GetBestMove(c *gin.Context) {
    fen := c.DefaultQuery("fen", "")
    model := c.DefaultQuery("model_name", "")

    // Validate the query parameters
    if fen == "" || model == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "FEN and model_name are required"})
        return
    }

	// get move suggestion from service
	bestMove, err := service.GetBestMove(fen, model)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	c.IndentedJSON(http.StatusOK, bestMove)
}