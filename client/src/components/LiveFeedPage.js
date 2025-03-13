import React, { useState, useEffect } from 'react';
import './LiveFeedPage.css';

const LiveFeedPage = () => {
    const [personDetected, setPersonDetected] = useState(true);
    const [latitude, setLatitude] = useState(17.374107667554952);
    const [longitude, setLongitude] = useState(78.5214);
    const [altitude, setAltitude] = useState(120); // Default altitude
    const [notification, setNotification] = useState('');

    // Simulate detecting a person and triggering the notification
    useEffect(() => {
        if (personDetected) {
            // Set up a countdown for payload drop notification
            const timer = setTimeout(() => {
                setNotification('Drone is going to drop the payload in 1 minute!');
            }, 60000); // After 1 minute

            return () => clearTimeout(timer); // Cleanup timer when component unmounts
        }
    }, [personDetected]);

    const togglePersonDetection = () => {
        setPersonDetected((prev) => !prev);
    };

    return (
        <div className="live-feed-container">
            {/* Heading */}
            <h2 className="heading">Live Feed</h2>

            {/* Main Content: Left and Right Side */}
            <div className="content-container">
                {/* Left side: Drone Info */}
                <div className="left-side">
                    <h3>Drone Info:</h3>
                    <p>Altitude: {altitude} meters</p>
                    <p>Latitude: {latitude}</p>
                    <p>Longitude: {longitude}</p>
                </div>

                {/* Right side: Live Feed Video */}
                {personDetected && (
                    <div className="right-side">
                        <div className="live-feed">
                            <video
                                width="400"
                                height="300"
                                controls
                                autoPlay
                                muted
                            >
                                {/* Placeholder for live feed video */}
                                <source
                                    src="your-live-feed-url.mp4"
                                    type="video/mp4"
                                />
                                Your browser does not support the video tag.
                            </video>
                        </div>
                    </div>
                )}
            </div>

            {/* Notification */}
            {notification && <div className="notification">{notification}</div>}

            {/* Button to toggle detection */}
            <button className="toggle-btn" onClick={togglePersonDetection}>
                {personDetected ? 'Stop Detection' : 'Detect Person'}
            </button>
        </div>
    );
};

export default LiveFeedPage;
