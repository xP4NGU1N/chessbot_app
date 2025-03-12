# Giraffe and DeepChess Models for Computer Chess & Simple Chess Web Application

This repository contains implementations of computer chess models trained following the architectures described in the [Giraffe Paper](https://arxiv.org/pdf/1509.01549) and the [DeepChess Paper](https://arxiv.org/pdf/1711.09667). Model training is performed using Jupyter notebooks (.ipynb).

In addition, a simple web application is provided that lets you play chess locally with integrated evaluations and move suggestions.

---

## Features

- **Chess Gameplay:** Play chess by making moves on the board.
- **Position Evaluation:** View the evaluation of the current board position.
- **Best Move Suggestion:** Receive recommendations for the best move.
- **Export Game as PGN:** Save your game in PGN format.

---

## Application Architecture

The application is divided into three main components:

### 1. Interface with Models (Python Flask)
This service interfaces with the trained chess models.

- **Directory:** `app/backend/chess_model_service`
- **How to Run:**
  ```bash
    cd app/backend/chess_model_service
    python server.py
    ```


### 2. Backend (Go with Gin)
Handles the backend logic and communication for the application.

- **Directory:** `app/backend/server`
- **How to Run:**
  ```bash
    cd app/backend/server
    go run main.go
    ```


### 3. Frontend (React with Vite)
The web interface for playing chess.

- **Directory:** `app/frontend/chess-app`
- **How to Run:**
  ```bash
    cd app/frontend/chess-app
    npm run dev
    ```



