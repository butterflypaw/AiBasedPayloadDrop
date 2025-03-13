import React from 'react';
import Login from './Login'; // Import your Login component
import Register from './Register'; // Import your Register component
import './AuthComponent.css'; // Import the CSS file for styling

const AuthComponent = () => {
  return (
    <div className="auth-container">
      <div className="login-section">
        <Login />
      </div>
      <div className="register-section">
        <Register />
      </div>
    </div>
  );
};

export default AuthComponent;