import React, { useRef } from 'react';

const LiveFeed = () => {
    const videoRef = useRef(null);

    // This function will handle PiP toggle
    const handlePiP = async () => {
        try {
            if (videoRef.current) {
                // Check if video is already in PiP mode
                if (!document.pictureInPictureElement) {
                    // If not in PiP, request PiP mode
                    await videoRef.current.requestPictureInPicture();
                } else {
                    // If already in PiP, exit PiP mode
                    await document.exitPictureInPicture();
                }
            }
        } catch (error) {
            console.error('Error with PiP toggle:', error);
        }
    };

    return (
        <div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <video
                ref={videoRef}
                style={{ width: '100%', height: '100%' }}
                controls
                onClick={handlePiP} // Toggle PiP when clicked
            >
                <source src="your-drone-feed-url.mp4" type="video/mp4" />
                Your browser does not support the video tag.
            </video>
        </div>
    );
};

export default LiveFeed;
