import React from 'react';

export default function VideoPlayer({ src, coverphoto="", width = "640px", height = "360px", controls = true, autoplay = false, loop = false, muted = false,  }) {
    if (!src) {
        return <p>No video source provided</p>;
    }

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '20px' }}>
            <video 
                width={width} 
                height={height} 
                controls={controls} 
                autoPlay={autoplay} 
                loop={loop} 
                muted={muted}
                style={{ borderRadius: '10px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)' }}
                poster={coverphoto}
            >
                <source src={src} type="video/mp4" />
                Your browser does not support the video tag.
            </video>
        </div>
    );
}
