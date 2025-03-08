import React from "react";

const EndgameDisplay = ({ score, onExportGame, onNewGame }) => {
    if (!score) return null;

    return (
        <div style={{
            position: "absolute", top: 0, left: 0, width: "100%", height: "100%",
            backgroundColor: "rgba(0, 0, 0, 0.5)", display: "flex", justifyContent: "center",
            alignItems: "center", flexDirection: "column", zIndex: 1000
        }}>
            <div style={{ color: "white", fontSize: "24px", marginBottom: "20px" }}>
                <strong>{score}</strong>
            </div>
            <div style={{ color: "white", fontSize: "24px", marginBottom: "250px" }}>
                <button onClick={onExportGame} style={{ margin: "10px", padding: "10px" }}>Export Game</button>
                <button onClick={onNewGame} style={{ margin: "10px", padding: "10px" }}>New Game</button>
            </div>
        </div>
    );
};

export default EndgameDisplay;
