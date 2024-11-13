import React, { useState } from "react";
import { Card, CardContent, Box } from "@mui/material";
import { styled } from "@mui/system";

// Styled component for the flip card
const FlipCard = styled(Box)({
    perspective: "1000px", // Gives the card a 3D effect
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: '20px',
    flexGrow: 1,
    flexShrink: 0,
    flexBasis: 'auto',
});

// Avoid passing isFlipped to the DOM element
const FlipCardInner = styled(Box)(({ isflipped }) => ({
    width: "45vw",
    height: "25vw",
    transition: "transform 0.6s",
    transformStyle: "preserve-3d",
    transform: isflipped ? "rotateY(180deg)" : "none",
    display: 'flex',
    justifyContent: 'left',
    alignItems: 'center',
}));

const cardStyles = {
    position: "absolute",
    width: "100%",
    height: "100%",
    backfaceVisibility: "hidden", // Hides the back side when flipping
};

// Styled components for the front and back sides of the flip card
const FlipCardFront = styled(Card)({
    ...cardStyles,
});

const FlipCardBack = styled(Card)({
    ...cardStyles,
    transform: "rotateY(180deg)",
});

export default function FlipCardPicture({ post }) {
    const [isFlipped, setIsFlipped] = useState(false);

    const handleMouseEnter = () => {
        setIsFlipped(true);
    };

    const handleMouseLeave = () => {
        setIsFlipped(false);
    };

    const handleClicked = () => {
        window.location.href = post.link;
    };

    return (
        <FlipCard onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave} onClick={handleClicked}>
            <FlipCardInner isflipped={isFlipped}>
                {/* Front Side */}
                <FlipCardFront>
                    <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', padding: 0 }}>
                        <Box
                            component="img"
                            sx={{
                                height: '100%',
                                width: '100%',
                                objectFit: 'cover', // Ensures the image covers the entire area without stretching
                            }}
                            alt=""
                            src="RobotsOperating.jpg"
                        />
                    </CardContent>
                </FlipCardFront>

                {/* Back Side */}
                <FlipCardBack>
                    <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', padding: 0 }}>
                        <Box
                            component="img"
                            sx={{
                                height: '100%',
                                width: '100%',
                                objectFit: 'cover', // Ensures the image covers the entire area without stretching
                            }}
                            alt=""
                            src="RobotBreakdown.png"
                        />
                    </CardContent>
                </FlipCardBack>
            </FlipCardInner>
        </FlipCard>
    );
}
