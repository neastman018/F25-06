import React, { useState } from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
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
    padding: '10px',
});

// Avoid passing isFlipped to the DOM element
const FlipCardInner = styled(Box)(({ isflipped }) => ({
    width: "15vw",
    height: "8vw",
    transition: "transform 0.6s",
    transformStyle: "preserve-3d",
    transform: isflipped ? "rotateY(180deg)" : "none",
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
}));

const cardStyles = {
    position: "absolute",
    width: "100%",
    height: "100%",
    backfaceVisibility: "hidden", // Hides the back side when flipping
    borderRadius: "10px", // Rounded corners
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)", // Shadow
};

const FlipCardFront = styled(Card)({
    ...cardStyles,
});

const FlipCardBack = styled(Card)({
    ...cardStyles,
    transform: "rotateY(180deg)",
});

export default function FlipCardLink({post}) {
    const [isFlipped, setIsFlipped] = useState(false);
    const [isClicked, setIsClicked] = useState(false);


    const handleMouseEnter = () => {
        setIsFlipped(true);
    };

    const handleMouseLeave = () => {
        setIsFlipped(false);
    };

    const handleClicked = () => {
        setIsClicked(true);
        window.location.href = post.link;
    };



    return (
        <FlipCard onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave} onClick={handleClicked} 
            style={{ 
            opacity: isClicked ? 0.5 : 1, 
            transition: 'background-color 0.3s ease-in-out' 
        }}>
            <FlipCardInner isflipped={isFlipped}>
                {/* Front Side */}
                <FlipCardFront>
                    <CardContent sx = {{display: 'flex', justifyContent: 'center', alignItems: 'center', height:'100%'}}>
                        <Typography variant='h2' style={{ color: "#861F41", fontSize: '1.5rem', fontWeight: 'bold', textAlign: 'center'}}>
                            {post.title}
                        </Typography>
                    </CardContent>
                </FlipCardFront>

                {/* Back Side */}
                <FlipCardBack>
                    <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                        <Typography varient='body1' style={{ color: "#000", fontSize: '1.0rem', textAlign: 'center' }}>
                            {post.description}
                        </Typography>
                    </CardContent>
                </FlipCardBack>
            </FlipCardInner>
        </FlipCard>
    );
};