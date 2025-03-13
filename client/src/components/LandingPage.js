import React, { useState } from 'react';
import Telemetry from './telemetry.js';
import MapComponent from './map.js';
import LiveFeed from './liveFeed.js';
import axios from 'axios'; // Import Axios for making HTTP requests
import './LandingPage.css'; // Import the CSS f

const LandingPage = () => {
    const [coordinates, setCoordinates] = useState({
        latitude: 17.374107667554952,
        longitude: 78.5214,
    });

    const [isLiveFeedVisible, setIsLiveFeedVisible] = useState(false);

    const handleCoordinatesChange = (newCoordinates) => {
        setCoordinates(newCoordinates);
    };

    const toggleLiveFeed = () => {
        setIsLiveFeedVisible((prev) => !prev);
    };

    const handleLaunch = async () => {
        try {
            console.log(coordinates)
            const response = await axios.post('http://localhost:8000/launch', coordinates);
            alert(`Launch successful: ${response.data.message}`);
        } catch (error) {
            console.error('There was an error launching!', error);
            alert('Launch failed. Please try again.');
        }
    };

    return (
        <div className="landing-page">
            {/* Top Bar */}
            <div className="top-bar">
                <h1 className="title">Drone Dashboard</h1>
                <button className="toggle-button" onClick={toggleLiveFeed}>
                    {isLiveFeedVisible ? 'Hide Drone Camera' : 'Show Drone Camera'}
                </button>
            </div>

            {/* Main Content */}
            <div className="main-content">
                {/* Sidebar */}
                <div className="sidebar">
                    <Telemetry coordinates={coordinates} onCoordinatesChange={handleCoordinatesChange} />
                </div>

                {/* Map and Conditional LiveFeed */}
                <div className="map-container">
                    <MapComponent coordinates={coordinates} />
                    
                    {isLiveFeedVisible && (
                        <div className="live-feed">
                            <LiveFeed />
                        </div>
                    )}

                    {/* Launch Button */}
                    <div className="text-right mt-3"> {/* Aligns the button to the right */}
                        <button style={{background:"#b3ffb3", border: "0.5px solid #84e4a8", padding:"10px 20px" ,borderRadius:"5px"}} onClick={handleLaunch}>
                            Launch
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;