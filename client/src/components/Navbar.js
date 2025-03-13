import React from 'react';
import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <h1>Drone Mission Planner</h1>
            <div className="navbar-right">
                <button className="simulation-button">Simulation</button>
                <button className="login-button">Login</button>
            </div>
        </nav>
    );
};

export default Navbar;
