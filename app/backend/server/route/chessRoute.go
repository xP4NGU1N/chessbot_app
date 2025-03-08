package route

import (
	
	"github.com/gin-gonic/gin"
	"chessapp/controller"
)


func RegisterRoutes(router *gin.Engine) {
	router.GET("/get_current_position", controller.GetCurrentPosition)
	// request: {}
	// response: { fen, model_name, rating }
	router.GET("/evaluate_position", controller.EvaluatePosition)
	// request: { fen, model_name }
	// response: { fen, model_name, rating }
	router.GET("/get_best_move", controller.GetBestMove)
	// request: { fen, model_name }
	// response: { model_name, move }
	router.GET("/export_game", controller.ExportGame)
	// request: {}
	// response: { pgn }
	router.GET("/get_all_positions", controller.GetAllPositions) // for testing
	// request {}
	// response { positions[] }

	router.POST("/make_move", controller.MakeMove)
	// request: { fen, model_name, move }
	// response: { fen, model_name, rating }
	router.POST("/redo_move", controller.RedoMove)
	// request: { model_name }
	// response: { fen, model_name, rating }

	router.PUT("/undo_move", controller.UndoMove)
	// request: { model_name }
	// response: { fen, model_name, rating }
	router.PUT("/reset_game", controller.ResetGame)
	// request: {}
	// response: { fen, model_name, rating }
}