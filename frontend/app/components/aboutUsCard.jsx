import React, { useState } from "react";
import { Card, CardContent, Box, Typography } from "@mui/material";
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
const FlipCardInner = styled(Box)(({ isflipped, width, height }) => ({
    width: width || "45vw",
    height: height || "25vw",
    transition: "transform 0.6s",
    transformStyle: "preserve-3d",
    transform: isflipped ? "rotateY(180deg)" : "none",
    display: 'flex',
    justifyContent: 'center', // Center content horizontally
    alignItems: 'center', // Center content vertically
    position: 'relative',
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

export default function AboutUsCard({ post, width = "45vw", height = "25vw" }) {
    const [isFlipped, setIsFlipped] = useState(false);

    const handleMouseEnter = () => {
        setIsFlipped(true);
    };

    const handleMouseLeave = () => {
        setIsFlipped(false);
    };

    const handleClicked = () => {
        // Add click functionality if needed
    };

    return (
        <FlipCard onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave} onClick={handleClicked} sx={{p:3}}>
            <FlipCardInner isflipped={isFlipped} width={width} height={height}>
                {/* Front Side */}
                <FlipCardFront>
                    {/* Title */}
                    <Typography variant='h5' sx={{ textAlign: 'center', paddingTop: '5px', fontSize: '0.95em'}}>
                        {post.name}
                    </Typography>
                    <Typography variant='body2' sx={{ textAlign: 'center' , fontSize: '0.85em'}}>
                        {post.major}
                    </Typography>
                    
                    {/* Image and Role Container */}
                    <CardContent 
                        sx={{ 
                            display: 'flex', 
                            flexDirection: 'column', 
                            justifyContent: 'center', 
                            alignItems: 'center', 
                            height: 'calc(100% - 40px)', // Remaining height for image and role
                            padding: '0px 10px' // Padding on sides only
                        }}
                    >
                        <Box
                            component="img"
                            sx={{
                                height: '65%', // Reduce image height
                                width: 'auto',  // Maintain aspect ratio
                                objectFit: 'contain', // Ensures the image covers the area without cropping
                                borderRadius: '10px', // Optional rounded corners for image
                            }}
                            alt={post.alt}
                            src={post.image}
                        />
                        {/* Role */}
                        <Typography variant='body' sx={{ textAlign: 'center', marginTop: '8px', fontSize: '0.85em' }}>
                            {post.role}
                        </Typography>
                    </CardContent>
                </FlipCardFront>

                {/* Back Side */}
                <FlipCardBack>
                    <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', padding: '10px' }}>
                        <Typography variant='body' sx={{ textAlign: 'center', fontSize: '0.75em'}}>
                            {post.description}
                        </Typography>
                    </CardContent>
                </FlipCardBack>
            </FlipCardInner>
        </FlipCard>
    );
}
