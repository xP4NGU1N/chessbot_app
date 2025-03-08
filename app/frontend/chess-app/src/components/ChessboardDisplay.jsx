import React from "react";
import { Chessboard } from "react-chessboard";

const ChessboardDisplay = ({ game, onMove }) => {
    return (
        <div className="chessboard-container">
            <Chessboard id="ChessBoard" position={game.fen()} onPieceDrop={onMove} />
        </div>
    );
};

export default ChessboardDisplay;
