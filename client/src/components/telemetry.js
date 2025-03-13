import React, { useEffect, useState } from 'react';
import './Telemetry.css';

const Telemetry = ({ coordinates, onCoordinatesChange }) => {
    const [data, setData] = useState({
        altitude: 'N/A',
        speed: 'N/A',
        battery: 'N/A',
        gpsStatus: 'N/A'
    });

    const [manualCoordinates, setManualCoordinates] = useState({
        latitude: coordinates?.latitude || 0, // Default to 0 if undefined
        longitude: coordinates?.longitude || 0
    });

    const [error, setError] = useState('');

    useEffect(() => {
        const fetchTelemetryData = async () => {
            try {
                const response = await fetch('/api/telemetry');
                if (!response.ok) {
                    throw new Error(`HTTP Error: ${response.status}`);
                }
                const telemetryData = await response.json();
                setData(telemetryData);
            } catch (error) {
                console.error('Error fetching telemetry data:', error);
                setData({
                    altitude: 'Error',
                    speed: 'Error',
                    battery: 'Error',
                    gpsStatus: 'Error'
                });
            }
        };

        fetchTelemetryData();
        const intervalId = setInterval(fetchTelemetryData, 5000);

        return () => clearInterval(intervalId);
    }, []);

    const handleSetCoordinates = () => {
        const { latitude, longitude } = manualCoordinates;
        if (latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180) {
            setError('Invalid coordinates. Latitude must be between -90 and 90, and longitude between -180 and 180.');
            return;
        }
        setError('');
        onCoordinatesChange(manualCoordinates);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setManualCoordinates((prevCoords) => ({
            ...prevCoords,
            [name]: value === '' ? '' : parseFloat(value) // Handle empty input gracefully
        }));
    };

    return (
        <div className="telemetry">
            <h2 className="telemetry-heading">Telemetry Data</h2>
            <div className="telemetry-item">
                <h3 className="telemetry-subheading">Altitude:</h3>
                <p className="telemetry-value">{data.altitude} m</p>
            </div>
            <div className="telemetry-item">
                <h3 className="telemetry-subheading">Speed:</h3>
                <p className="telemetry-value">{data.speed} m/s</p>
            </div>
            <div className="telemetry-item">
                <h3 className="telemetry-subheading">Battery:</h3>
                <p className="telemetry-value">{data.battery}%</p>
            </div>
            <div className="telemetry-item">
                <h3 className="telemetry-subheading">GPS Status:</h3>
                <p className="telemetry-value">{data.gpsStatus}</p>
            </div>

            <h3 className="telemetry-subheading">Manual Coordinates</h3>
            {error && <p className="error-message">{error}</p>}
            <div className="telemetry-coordinates">
                <label>
                    Latitude:
                    <input
                        type="number"
                        name="latitude"
                        value={manualCoordinates.latitude || ''}
                        placeholder="Enter latitude"
                        onChange={handleInputChange}
                        className="telemetry-input"
                    />
                </label>
                <label>
                    Longitude:
                    <input
                        type="number"
                        name="longitude"
                        value={manualCoordinates.longitude || ''}
                        placeholder="Enter longitude"
                        onChange={handleInputChange}
                        className="telemetry-input"
                    />
                </label>
            </div>

            <button onClick={handleSetCoordinates} className="telemetry-button">
                Set Coordinates
            </button>
        </div>
    );
};

export default Telemetry;
