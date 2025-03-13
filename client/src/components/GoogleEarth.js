import React, { useEffect, useRef } from 'react';

const GoogleEarth = ({ coordinates }) => {
    const mapRef = useRef(null);

    useEffect(() => {
        if (mapRef.current && coordinates) {
            const { latitude, longitude } = coordinates;

            // Update map pointer logic here
            const map = mapRef.current;

            // Assuming a function `setMapPointer` exists in your map library to update the pointer
            if (map.setView) {
                map.setView([latitude, longitude], 13); // Adjust zoom level as needed
            }
        }
    }, [coordinates]);

    return (
        <div
            id="map"
            style={{
                height: '100%',
                width: '100%'
            }}
            ref={mapRef}
        >
            {/* Map will render here */}
        </div>
    );
};

export default GoogleEarth;
