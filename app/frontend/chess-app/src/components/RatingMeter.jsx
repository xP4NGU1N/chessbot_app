import React from "react";

const RatingMeter = ({ rating }) => {
    return (
    <div
        style={{
            width: "30px",
            height: "600px",
            background: `linear-gradient(to top, white ${(rating + 1) * 50}%, black ${(rating + 1) * 50}%)`,
            transition: "background 2.5s ease",
            border: "2px solid black",
        }}
        ></div>
    );
};

export default RatingMeter;
