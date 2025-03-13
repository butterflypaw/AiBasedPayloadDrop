import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

function DroneFeed() {
    const [videoFeed, setVideoFeed] = useState(true);

    useEffect(() => {
        const socket = io('http://localhost:5000');
        socket.on('video-feed', (feedData) => {
            setVideoFeed(feedData);
        });

        return () => socket.disconnect();
    }, []);

    return (
        <div>
            <h2>Live Drone Feed</h2>
            {videoFeed ? <img src={videoFeed} alt="Drone Live Feed" /> : <p>No live feed available</p>}
        </div>
    );
}

export default DroneFeed;
