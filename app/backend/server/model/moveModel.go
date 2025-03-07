package model

type Move struct {
	FEN		string  `json:"fen"`
	Model	string  `json:"model_name"`
	Move	string	`json:"move"`
}

type SuggestedMove struct {
	Model	string  `json:"model_name"`
	Move	string  `json:"move"`
}

type CycleMoveRequest struct {
	Model	string  `json:"model_name"`
}