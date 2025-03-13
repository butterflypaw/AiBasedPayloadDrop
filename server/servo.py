import time

def activate_servo(vehicle, channel, pwm):
    """
    Activates a servo motor on the specified channel with the given PWM value.
    
    :param vehicle: The vehicle object connected to Pixhawk.
    :param channel: The channel number (e.g., 7 for the servo).
    :param pwm: The PWM value to send to the servo (typically between 1000-2000).
    """
    print(f"Activating servo on channel {channel} with PWM value {pwm}...")
    # Set the PWM value for the servo on the specified channel
    vehicle.channels.overrides[channel] = pwm
    time.sleep(1)  # Wait for the servo action to complete
    print(f"Servo on channel {channel} activated with PWM: {pwm}")


def reset_servo_overrides(vehicle):
    """
    Resets all servo overrides to restore normal control.
    
    :param vehicle: The vehicle object connected to Pixhawk.
    """
    print("Resetting all servo overrides...")
    vehicle.channels.overrides = {}
    print("Servo overrides reset.")
