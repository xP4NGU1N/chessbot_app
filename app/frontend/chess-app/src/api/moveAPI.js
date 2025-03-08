import axios from "axios";

export const sendMove = async (move, fen, model) => {
    try {
        const response = await axios.post("/api/make_move", { move, fen, model_name: model });
        return response.data;
    } catch (error) {
        console.error("Error sending move:", error);
        throw error;
    }
};
  
export const undoMove = async (model) => {
    try {
        const response = await axios.put("/api/undo_move", { model_name: model });
        return response.data;
    } catch (error) {
        console.error("Undo failed:", error);
        throw error;
    }
};
  
export const redoMove = async (model) => {
    try {
        const response = await axios.post("/api/redo_move", { model_name: model });
        return response.data;
    } catch (error) {
        console.error("Redo failed:", error);
        throw error;
    }
};