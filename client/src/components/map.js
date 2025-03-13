import React, { useRef, useState, useEffect } from 'react';
import { GoogleMap, LoadScript } from '@react-google-maps/api';

const mapContainerStyle = {
  height: '100vh',
  width: '100%',
};

const defaultCenter = {
  lat: 17.374107667554952,
  lng: 78.5214,
};

const GeofenceMap = () => {
  const mapRef = useRef(null);
  const drawingManagerRef = useRef(null); // Reference to track DrawingManager
  const [activeGeofence, setActiveGeofence] = useState(null);
  const [isGeofenceFixed, setIsGeofenceFixed] = useState(false); // Track if geofence is fixed

  // Handle the geofence fix
  const handleFixGeofence = () => {
    if (activeGeofence) {
      activeGeofence.setEditable(false); // Lock the geofence from editing
      setIsGeofenceFixed(true); // Mark geofence as fixed
      alert('Geofence fixed!');
    } else {
      alert('No geofence to fix!');
    }
  };

  // Handle the removal of geofence
  const handleRemoveGeofence = () => {
    if (activeGeofence) {
      activeGeofence.setMap(null); // Remove geofence from map
      setActiveGeofence(null); // Clear active geofence state
      setIsGeofenceFixed(false); // Geofence is no longer fixed
      alert('Geofence removed!');
    } else {
      alert('No geofence to remove!');
    }
  };

  useEffect(() => {
    const initializeDrawingTools = () => {
      if (mapRef.current && window.google && !drawingManagerRef.current) {
        const drawingManager = new window.google.maps.drawing.DrawingManager({
          drawingMode: null, // No drawing mode initially
          drawingControl: true,
          drawingControlOptions: {
            position: window.google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['rectangle'], // Only rectangle mode enabled
          },
          rectangleOptions: {
            fillColor: '#0000FF',
            fillOpacity: 0.35,
            strokeWeight: 1,
            clickable: true,
            editable: true,
            zIndex: 1,
          },
        });

        drawingManager.setMap(mapRef.current);
        drawingManagerRef.current = drawingManager;

        // Handle new geofence creation
        window.google.maps.event.addListener(drawingManager, 'overlaycomplete', (event) => {
          if (activeGeofence) {
            alert('A geofence already exists. Remove it before drawing a new one.');
            event.overlay.setMap(null); // Remove the newly drawn geofence
            return;
          }
          setActiveGeofence(event.overlay); // Set the new geofence
          drawingManager.setDrawingMode(null); // Stop drawing mode
        });
      }
    };

    initializeDrawingTools();
  }, [activeGeofence]); // Update only when activeGeofence changes

  return (
    <div>
      <LoadScript
        googleMapsApiKey="AIzaSyBJyFrd8qkBZOaHD3MZuvGem1WJjGiCr5s" // Replace with your valid API Key
        libraries={['drawing']} // Ensure 'drawing' library is included
      >
        <GoogleMap
          mapContainerStyle={mapContainerStyle}
          center={defaultCenter}
          zoom={10}
          onLoad={(map) => (mapRef.current = map)}
        />
      </LoadScript>
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 1 }}>
        <button
          onClick={handleFixGeofence}
          disabled={!activeGeofence || isGeofenceFixed}
          style={{
            padding: '10px',
            margin: '5px',
            background: isGeofenceFixed ? '#ccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: isGeofenceFixed ? 'not-allowed' : 'pointer',
          }}
        >
          Fix Geofence
        </button>
        <button
          onClick={handleRemoveGeofence}
          style={{
            padding: '10px',
            margin: '5px',
            background: '#f44336',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Remove Geofence
        </button>
      </div>
    </div>
  );
};

export default GeofenceMap;
