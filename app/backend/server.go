package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	fmt.Println("Server started on port 8080")
	http.ListenAndServe(":8080", nil)
}


