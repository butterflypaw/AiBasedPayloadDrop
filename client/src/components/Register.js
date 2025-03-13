import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import './Register.css'; // Import the CSS file
import { useNavigate } from 'react-router-dom';

function Register() {
    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const navigate= useNavigate();

    const handleRegister = async () => {
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        // Prepare the data to be sent to the backend
        const userData = {
            full_name: fullName,
            email: email,
            password: password,
        };

        try {
            // Send a POST request to the Flask backend
            console.log(userData);
            const response = await axios.post('http://localhost:8000/register', userData);
            alert(`Registration successful: ${response.data.message}`);
            navigate("/LandingPage");
        } catch (error) {
            console.error('There was an error registering!', error);
            alert('Registration failed. Please try again.');
        }
    };

    return (
        <div className="center-container">
            <div className="form-container">
                <h2>Register</h2>
                <input
                    type="text"
                    placeholder="Full Name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button onClick={handleRegister}>Register</button>
            </div>
        </div>
    );
}

export default Register;