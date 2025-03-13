from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dronekit import connect, VehicleMode
import socket
import time

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/Drone"  # Change to your database name
mongo = PyMongo(app)

# Socket for human detection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 65432))  # Bind to localhost and port 65432
server_socket.listen(1)

# Drone connection
connection_string = "COM3"
vehicle = connect(connection_string, baud=57600, wait_ready=False, heartbeat_timeout=60)

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    password = request.json.get('password')

    # Check if the user already exists
    existing_user = mongo.db.users.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'User already exists!'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = {
        'full_name': full_name,
        'email': email,
        'password': hashed_password
    }

    # Insert the new user into the database
    mongo.db.users.insert_one(new_user)
    return jsonify({'message': 'User registered successfully!'}), 201

# Drone endpoints
@app.route('/launch', methods=['POST'])
def launch_drone():
    """Arm the drone and initiate takeoff."""
    target_altitude = request.json.get('altitude', 10)  # Default altitude: 10m
    arm_and_takeoff(target_altitude)
    return jsonify({'message': f'Drone launched to {target_altitude} meters'}), 200

def arm_and_takeoff(target_altitude):
    """Arm the drone and take off to the target altitude."""
    print("Pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off...")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(f" Altitude: {vehicle.location.global_relative_frame.alt:.2f}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Target altitude reached.")
            break
        time.sleep(1)

@app.route('/human-detection', methods=['POST'])
def human_detection():
    """Check for human detection via socket communication."""
    conn, addr = server_socket.accept()
    print(f"Connected to human detection script at {addr}")

    try:
        data = conn.recv(1024).decode()
        if "Human detected" in data:
            print(f"Human detected: {data}")
            bbox = data.split("bbox=")[1].strip("()")
            bbox_center_x, bbox_center_y = map(int, bbox.split(","))
            roll, pitch = adjust_drone_position(bbox_center_x, bbox_center_y)

            if roll == 0 and pitch == 0:  # Aligned over human
                conn.close()
                return jsonify({'message': 'Human detected and drone aligned.'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/drop-payload', methods=['POST'])
def drop_payload():
    """Drop the payload if a human is detected within range."""
    while True:
        distance = read_tof_sensor()
        if distance is not None:
            print(f"ToF Distance: {distance} mm")
            if distance <= 3000:  # 3 meters
                print("Human detected within range. Activating payload drop.")
                activate_servo(vehicle, channel=7, pwm=2000)
                time.sleep(2)
                reset_servo_overrides(vehicle)
                return jsonify({'message': 'Payload dropped successfully.'}), 200
    return jsonify({'message': 'No human detected within range.'}), 400

@app.route('/return', methods=['POST'])
def return_to_launch():
    """Command the drone to return to launch."""
    print("Returning to launch...")
    vehicle.mode = VehicleMode("RTL")
    vehicle.close()
    return jsonify({'message': 'Drone returning to launch.'}), 200

# Utilities for drone control
def adjust_drone_position(bbox_center_x, bbox_center_y):
    """Adjust drone roll and pitch based on bounding box center."""
    x_center = 640 // 2  # Assuming a 640x480 frame
    y_center = 480 // 2
    roll = (bbox_center_x - x_center) // 10
    pitch = (bbox_center_y - y_center) // 10
    print(f"Adjusting roll: {roll}, pitch: {pitch}")
    return roll, pitch

def read_tof_sensor():
    """Mock function to simulate ToF sensor reading."""
    return 2000  # Example distance in mm

def activate_servo(vehicle, channel, pwm):
    """Activate servo for payload drop."""
    print(f"Activating servo on channel {channel} with PWM {pwm}")
    vehicle.channels.overrides[channel] = pwm

def reset_servo_overrides(vehicle):
    """Reset all servo overrides."""
    print("Resetting servo overrides")
    vehicle.channels.overrides = {}

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, port=8000)
