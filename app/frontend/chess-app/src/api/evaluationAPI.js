import axios from "axios";

export const evaluatePosition = async (fen, selectedModel) => {
    try {
        const response = await axios.get("/api/evaluate_position", { params: { fen, model_name: selectedModel } });
        return response.data;
    } catch (error) {
        console.error("Error evaluating position:", error);
        throw error;
    }
};

export const getBestMove = async (fen, modelName) => {
    try {
        const response = await axios.get("/api/get_best_move", { params: { fen, model_name: modelName } });
        return response.data;
    } catch (error) {
        console.error("Error getting best move:", error);
        throw error;
    }
};
