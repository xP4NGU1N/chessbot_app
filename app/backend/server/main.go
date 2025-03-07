package main

import (

	"chessapp/route"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.SetTrustedProxies([]string{"127.0.0.1", "localhost"}) // for local deployment

	// Define routes
	route.RegisterRoutes(router)

	// Start server
	router.Run("localhost:8080")
}
