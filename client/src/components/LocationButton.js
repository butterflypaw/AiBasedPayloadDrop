import React, { useState } from 'react';
import axios from 'axios';

const LocationButton = () => {
    const [message, setMessage] = useState('');

    // Function to handle the button click
    const handleSaveLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    // Send data to the backend
                    const now = new Date();
                    const time = now.toTimeString().split(' ')[0];

                    try {
                        const response = await axios.post('http://localhost:5001/save-location', {
                            latitude,
                            longitude,
                        });
                        setMessage(response.data.message);
                    } catch (error) {
                        setMessage('Error saving location: ' + (error.response?.data?.message || error.message));
                    }
                },
                (error) => {
                    setMessage('Error retrieving location: ' + error.message);
                }
            );
        } else {
            setMessage('Geolocation is not supported by this browser.');
        }
    };

    return (
        <div>
            <h2>Save Location</h2>
            <button onClick={handleSaveLocation}>Save Current Location</button>
            <p>{message}</p>
        </div>
    );
};

export default LocationButton;