import React, { useState, useEffect } from "react";
import { Chess } from "chess.js";
import { evaluatePosition, getBestMove } from "../api/evaluationAPI";
import { resetGame, exportGame } from "../api/gameAPI";
import { sendMove, undoMove, redoMove } from "../api/moveAPI";
import ChessboardDisplay from "./ChessboardDisplay";
import RatingMeter from "./RatingMeter";
import Controls from "./Controls";
import BestMoveDisplay from "./BestMoveDisplay";
import EndgameDisplay from "./EndgameDisplay";

const ChessGame = () => {
    const [game, setGame] = useState(new Chess());
    const [rating, setRating] = useState(0);
    const [model, setModel] = useState("Giraffe");
    const [bestMove, setBestMove] = useState(null);
    const [gameOver, setGameOver] = useState(false); 

    useEffect(() => {
        const fetchInitialPosition = async () => {
            try {
                const data = await resetGame();
                setRating(data.rating);
            } catch (error) {
                console.error("Error fetching initial position:", error);
            }
        };
        fetchInitialPosition();
    }, []);

    useEffect(() => {
        setGameOver(game.isGameOver());
    }, [game]);
    
    const makeMove = async (sourceSquare, targetSquare) => {
        const newGame = new Chess(game.fen());
        try {
            setGame(newGame);
            const move = newGame.move({ from: sourceSquare, to: targetSquare });
            const response = await sendMove(move.san, game.fen(), model);
            setRating(response.rating);
            setBestMove(null);
        } catch (error) {
            console.error("Move failed:", error);
        }
    };

    const handleUndo = async () => {
        try {
            const data = await undoMove(model);
            setGame(new Chess(data.fen));
            setRating(data.rating);
            setBestMove(null);
        } catch (error) {
            console.error("Undo failed:", error);
        }
    };

    const handleRedo = async () => {
        try {
            const data = await redoMove(model);
            setGame(new Chess(data.fen));
            setRating(data.rating);
            setBestMove(null);
        } catch (error) {
            console.error("Redo failed:", error);
        }
    };

    const handleNewGame = async () => {
        if (window.confirm("Are you sure you want to start a new game?")) {
            try {
                const data = await resetGame();
                setGame(new Chess(data.fen));
                setRating(data.rating);
                setGameOver(false)
                setBestMove(null);
            } catch (error) {
                console.error("New game failed:", error);
            }
        }
    };

    const handleModelChange = async (event) => {
        const newModel = event.target.value;
        setModel(newModel);
        setBestMove(null);
        try {
            const response = await evaluatePosition(game.fen(), newModel);
            setRating(response.rating); 
        } catch (error) {
            console.error("Error evaluating position:", error);
        }
    };

    const handleExportGame = async () => {
        try {
            const pgn = await exportGame();
            navigator.clipboard.writeText(pgn);
            alert("Game exported to clipboard!");
        } catch (error) {
            console.error("Export failed:", error);
        }
    };

    const handleGetBestMove = async () => {
        try {
            const response = await getBestMove(game.fen(), model);
            setBestMove(response.move);
        } catch (error) {
            console.error("Error fetching best move:", error);
        }
    };

    const getScore = () => {
        if (gameOver) {
            if (game.isCheckmate()) {
                return game.turn() === "b" ? "White Wins" : "Black Wins";
            }
            if (game.isDraw()) return "Draw";
            if (game.isStalemate()) return "Stalemate";
            return "Game Over";
        }
        return null;
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <div style={{ marginBottom: "15px" }}>
                <label style={{ marginRight: "10px"}}>Select model:</label>
                <select value={model} onChange={handleModelChange}>
                    <option value="Giraffe">Giraffe</option>
                    <option value="Giraffe with Transformer">Giraffe with Transformer</option>    
                </select>
            </div>

            <div style={{ marginBottom: "15px" }}>
                <strong>{model} Rating:</strong> {rating.toFixed(3)}
            </div>

            <Controls
                model={model}
                onUndo={handleUndo}
                onRedo={handleRedo}
                onNewGame={handleNewGame}
                onExport={handleExportGame}
                onGetBestMove={handleGetBestMove}
            />

            <div style={{ marginTop: "15px" }}>
                <h2>{game.turn() === "b" ? "Black" : "White"}'s turn to play</h2>
            </div>

            <BestMoveDisplay bestMove={bestMove} />

            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", marginTop: "20px" }}>
                <RatingMeter rating={rating} />
                <ChessboardDisplay game={game} onMove={makeMove} />
            </div>

            <EndgameDisplay
                score={getScore()}
                onExportGame={handleExportGame}
                onNewGame={handleNewGame}
            />
        </div>
    );
};

export default ChessGame;
