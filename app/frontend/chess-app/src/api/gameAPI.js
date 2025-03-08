import axios from "axios";

export const resetGame = async () => {
    try {
        const response = await axios.put("/api/reset_game");
        return response.data;
    } catch (error) {
        console.error("New game failed:", error);
        throw error;
    }
};
  
export const exportGame = async () => {
    try {
        const response = await axios.get("/api/export_game");
        return response.data.pgn;
    } catch (error) {
        console.error("Export failed:", error);
        throw error;
    }
};

