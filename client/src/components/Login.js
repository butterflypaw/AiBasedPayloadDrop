import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import './Login.css'; // Import the CSS file
import { useNavigate } from 'react-router-dom';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();


    const handleLogin = async () => {
        // Prepare the data to be sent to the backend
        const loginData = {
            username: username,
            password: password,
        };

        try {
            // Send a POST request to the Flask backend
            const response = await axios.post('http://localhost:8000/login', loginData);
            alert(`Login successful: ${response.data.message}`);
            navigate("/LandingPage");
            
        } catch (error) {
            console.error('There was an error logging in!', error);
            alert('Login failed. Please check your credentials and try again.');
        }
    };

    return (
        <div className="center-container">
            <div className="form-container">
                <h2>Login</h2>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button onClick={handleLogin}>Login</button>
            </div>
        </div>
    );
}

export default Login;