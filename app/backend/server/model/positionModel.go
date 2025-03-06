package model

type Position struct {
	FEN    string  `json:"fen"`
	Model  string  `json:"model_name"`
	Rating float64 `json:"rating"`
}

type UnratedPosition struct {
	FEN    string  `json:"fen"`
	Model  string  `json:"model_name"`
}