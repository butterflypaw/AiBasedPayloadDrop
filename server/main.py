import socket
from dronekit import connect, VehicleMode, LocationGlobal
from geofence import calculate_square_geofence, is_within_square_geofence, generate_grid_points
from camera import adjust_drone_position
from time import sleep
from servo import activate_servo, reset_servo_overrides

# Connect to the drone
connection_string = "COM3"
vehicle = connect(connection_string, baud=57600, wait_ready=False, heartbeat_timeout=60)

def arm_and_takeoff(target_altitude):
    """
    Arms the drone and takes off to the target altitude.
    """
    print("Pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        sleep(1)

    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        sleep(1)

    print("Taking off...")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(f" Altitude: {vehicle.location.global_relative_frame.alt:.2f}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Target altitude reached.")
            break
        sleep(1)

# Socket for communication with human detection code
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 65432))  # Bind to localhost and port 65432
server_socket.listen(1)
print("Waiting for connection from human detection script...")
conn, addr = server_socket.accept()
print(f"Connected to human detection script at {addr}")

# Geofence parameters
GEOFENCE_CENTER_LAT = 17.123456  # Example latitude
GEOFENCE_CENTER_LON = 78.123456  # Example longitude
SQUARE_SIDE_LENGTH_METERS = 3
STEP_SIZE = 0.00001  # Approx. ~1.11 meters

# Calculate geofence and grid points
geofence_edges = calculate_square_geofence(GEOFENCE_CENTER_LAT, GEOFENCE_CENTER_LON, SQUARE_SIDE_LENGTH_METERS)
grid_points = generate_grid_points(geofence_edges, STEP_SIZE)

print("Geofence edges:", geofence_edges)
print("Generated grid points:", grid_points)

# Arm and take off
arm_and_takeoff(10)  # Take off to 10 meters altitude

# Grid search
human_detected = False
for point in grid_points:
    target_location = LocationGlobal(point[0], point[1], 10)
    vehicle.simple_goto(target_location)

    # Wait until drone reaches the target location
    while True:
        current_lat = vehicle.location.global_frame.lat
        current_lon = vehicle.location.global_frame.lon
        print(f"Drone moving to grid point: {point}. Current position: {current_lat}, {current_lon}")

        if is_within_square_geofence(current_lat, current_lon, geofence_edges):
            print(f"Reached grid point: {point}")
            break
        sleep(1)

    # Receive detection data from the human detection script
    try:
        data = conn.recv(1024).decode()
        if data.startswith("Human Detected"):
            print(f"Human detected: {data}")
            bbox = data.split("bbox=")[1].strip("()")
            bbox_center_x, bbox_center_y = map(int, bbox.split(","))
            roll, pitch = adjust_drone_position(bbox_center_x, bbox_center_y)

            if roll == 0 and pitch == 0:  # Drone is centered over the bounding box
                print("Human detected and drone aligned.")

                # Lower the drone using LAND mode
                print("Lowering the drone to 5 meters using LAND mode...")
                vehicle.mode = VehicleMode("LAND")

                while vehicle.location.global_relative_frame.alt > 5.0:
                    print(f" Altitude: {vehicle.location.global_relative_frame.alt:.2f}")
                    sleep(1)

                print("Drone reached 5 meters.")

                # Activate the servo to release the payload
                print("Activating servo for payload release...")
                activate_servo(vehicle, channel=7, pwm=2000)  # Fully open servo
                sleep(2)  # Wait for payload to be released
                reset_servo_overrides(vehicle)  # Reset servo to default control


                # Return to launch
                print("Payload released. Returning to launch.")
                vehicle.mode = VehicleMode("RTL")
                human_detected = True
                break
    except socket.error as e:
        print(f"Socket error: {e}")
        break

if not human_detected:
    print("No human detected in the geofence.")

# Close sockets and return to launch
conn.close()
server_socket.close()
print("Returning to launch...")
vehicle.mode = VehicleMode("RTL")
vehicle.close()