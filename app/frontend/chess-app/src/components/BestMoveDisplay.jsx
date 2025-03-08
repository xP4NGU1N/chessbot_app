import React from "react";

const BestMoveDisplay = ({ bestMove }) => {
    if (!bestMove) return null;

    return (
        <div style={{ marginTop: "10px", color: "green" }}>
            <strong>Best Move: {bestMove}</strong>
        </div>
    );
};

export default BestMoveDisplay;
