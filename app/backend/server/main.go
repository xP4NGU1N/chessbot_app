package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

type position struct {
	FEN 	string	`json:"fen"`
	Rating	float64	`json:"rating"`
}

var positions = []position{}

func main() {
	router := gin.Default()
	router.GET("/positions", getPositions)
	router.POST("/position", makeMove)
	router.Run("localhost:8080")
}

func getPositions(c *gin.Context) {
    c.IndentedJSON(http.StatusOK, positions)
}

func makeMove(c *gin.Context) {
	var newPosition position
	if err := c.BindJSON(&newPosition); err != nil {
		return
	}

	positions = append(positions, newPosition)
	c.IndentedJSON(http.StatusCreated, newPosition)
}


