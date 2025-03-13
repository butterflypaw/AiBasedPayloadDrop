import socket
from dronekit import connect, VehicleMode, LocationGlobal
from geofence import calculate_square_geofence, is_within_square_geofence, generate_grid_points
from camera import adjust_drone_position
from servo import activate_servo, reset_servo_overrides
from time import sleep
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Drone connection
connection_string = "COM3"  # Replace with the appropriate connection string for your drone
vehicle = connect(connection_string, baud=57600, wait_ready=False, heartbeat_timeout=60)

def arm_and_takeoff(target_altitude):
    """
    Arms the drone and takes off to the target altitude.
    """
    logging.info("Pre-arm checks...")
    while not vehicle.is_armable:
        logging.info("Waiting for vehicle to initialize...")
        sleep(1)

    logging.info("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        logging.info("Waiting for arming...")
        sleep(1)

    logging.info("Taking off...")
    vehicle.simple_takeoff(target_altitude)

    while True:
        logging.info(f"Altitude: {vehicle.location.global_relative_frame.alt:.2f}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            logging.info("Target altitude reached.")
            break
        sleep(1)

# Socket for ToF sensor communication
tof_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tof_socket.connect(('192.168.0.101', 65433))  # Replace with Jetson Xavier's IP and port

# Socket for human detection communication
human_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
human_socket.bind(('127.0.0.1', 65432))
human_socket.listen(1)
logging.info("Waiting for connection from human detection script...")
human_conn, human_addr = human_socket.accept()
logging.info(f"Connected to human detection script at {human_addr}")

# Geofence parameters
GEOFENCE_CENTER_LAT = 17.123456
GEOFENCE_CENTER_LON = 78.123456
SQUARE_SIDE_LENGTH_METERS = 3
STEP_SIZE = 0.00001

# Calculate geofence and grid points
geofence_edges = calculate_square_geofence(GEOFENCE_CENTER_LAT, GEOFENCE_CENTER_LON, SQUARE_SIDE_LENGTH_METERS)
grid_points = generate_grid_points(geofence_edges, STEP_SIZE)

# Arm and take off
arm_and_takeoff(10)

# Grid search
human_detected = False
for point in grid_points:
    target_location = LocationGlobal(point[0], point[1], 10)
    vehicle.simple_goto(target_location)

    while True:
        current_lat = vehicle.location.global_frame.lat
        current_lon = vehicle.location.global_frame.lon
        if is_within_square_geofence(current_lat, current_lon, geofence_edges):
            logging.info(f"Reached grid point: {point}")
            break
        sleep(1)

    # Receive detection data from the human detection script
    try:
        data = human_conn.recv(1024).decode()
        if data.startswith("Human Detected"):
            logging.info(f"Human detected: {data}")
            bbox = data.split("bbox=")[1].strip("()")
            bbox_center_x, bbox_center_y = map(int, bbox.split(","))
            roll, pitch = adjust_drone_position(bbox_center_x, bbox_center_y)

            if roll == 0 and pitch == 0:  # Drone is centered over bounding box
                logging.info("Human detected and drone aligned.")

                # Lower the drone using LAND mode while checking ToF sensor
                logging.info("Lowering drone using LAND mode...")
                vehicle.mode = VehicleMode("LAND")

                while True:
                    tof_socket.sendall(b"GET_TOF")
                    tof_data = tof_socket.recv(1024).decode()
                    tof_distance = int(tof_data.strip())
                    logging.info(f"ToF distance: {tof_distance} mm")

                    if tof_distance <= 3000:  # 3 meters
                        logging.info("Drone reached 3 meters. Activating payload release...")
                        print("Activating servo for payload release...")
                        activate_servo(vehicle, channel=7, pwm=2000)  # Fully open servo
                        sleep(2)  # Wait for payload to be released
                        reset_servo_overrides(vehicle)  # Reset servo to default control
                        logging.info("Payload released. Returning to launch.")
                        vehicle.mode = VehicleMode("RTL")
                        human_detected = True
                        break
                    sleep(1)

                break
    except socket.error as e:
        logging.error(f"Socket error: {e}")
        break

if not human_detected:
    logging.info("No human detected in the geofence.")

# Cleanup
tof_socket.close()
human_conn.close()
human_socket.close()
vehicle.close()
