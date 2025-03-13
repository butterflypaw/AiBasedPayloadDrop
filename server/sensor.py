import Jetson.GPIO as GPIO
import serial
import time
import socket
import sys

# Constants for ToF sensor
TOF_length = 16
TOF_header = (87, 0, 255)
TOF_distance = 0

# Setup serial communication for ToF sensor
ser = serial.Serial('/dev/ttyTHS1', 115200)  # Adjust to your Jetson serial port
ser.flushInput()

# Socket for communication with human detection system (main system)
HOST = '127.0.0.1'  # Change to your receiving system IP
PORT = 65432        # Port to send data to

# Verify checksum function
def verifyCheckSum(data, length):
    TOF_check = 0
    for k in range(0, length - 1):
        TOF_check += data[k]
    TOF_check = TOF_check % 256
    return TOF_check == data[length - 1]

# Function to read ToF sensor data
def read_tof_sensor():
    global TOF_distance
    TOF_data = ()
    if ser.inWaiting() >= 32:
        for i in range(0, 16):
            TOF_data = TOF_data + (ord(ser.read(1)), ord(ser.read(1)))
        for j in range(0, 16):
            if ((TOF_data[j] == TOF_header[0] and TOF_data[j + 1] == TOF_header[1] and TOF_data[j + 2] == TOF_header[2]) and
                    verifyCheckSum(TOF_data[j:j + TOF_length], TOF_length)):
                if (((TOF_data[j + 12]) | (TOF_data[j + 13] << 8)) == 0):
                    break
                else:
                    TOF_distance = (TOF_data[j + 8]) | (TOF_data[j + 9] << 8) | (TOF_data[j + 10] << 16)
                    return TOF_distance
    return None

# Main execution
try:
    # Setup socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to receiving system")

        # Wait for human detection signal (from main system)
        while True:
            # Receive human detection signal with bounding box info
            data = s.recv(1024).decode()
            if data:
                # Check if human detected
                if "Human detected" in data:
                    print("Human detected. Starting ToF sensor readings.")

                    # Continuously read ToF sensor data
                    while True:
                        distance = read_tof_sensor()
                        if distance is not None:
                            print(f"ToF Distance: {distance} mm")

                            # If distance <= 3000 mm (3 meters), drop payload and RTL
                            if distance <= 3000:
                                print("Human detected within 3 meters, activating payload drop.")
                                # Activate servo to drop payload (Assumed servo function exists)
                                # activate_servo()
                                # Initiate RTL (Return to Launch) mode (Assumed drone control exists)
                                # vehicle.mode = VehicleMode("RTL")
                                
                                # Stop further execution if distance is within 3 meters
                                break

                        time.sleep(0.1)  # Small delay before reading again

            time.sleep(1)  # Small delay to avoid excessive CPU usage

except KeyboardInterrupt:
    print("Exiting program.")
    GPIO.cleanup()
    ser.close()
    sys.exit()

except Exception as e:
    print(f"Error: {e}")
    GPIO.cleanup()
    ser.close()
    sys.exit()