import React from "react";

const Controls = ({ onUndo, onRedo, onNewGame, onExport, onGetBestMove }) => {
    return (
        <div>
            <div style={{ marginTop: "20px"}}>
                <button className="controlButtons" onClick={onUndo}>Undo</button>
                <button className="controlButtons" onClick={onRedo}>Redo</button>
                <button className="controlButtons" onClick={onNewGame}>New Game</button>
                <button className="controlButtons" onClick={onExport}>Export</button>
                <button className="controlButtons" onClick={onGetBestMove}>Get Best Move</button>
            </div>
        </div>
    );
};

export default Controls;
