######Using AHT10 from 21st Oct 2025#######

import time
import board
import adafruit_ahtx0
import os

# =============== SENSOR SETUP ===============
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

# =============== CALIBRATION BIASES ===============
HUMIDITY_BIAS = -2.2783460736622656  # measured bias (to remove)
TEMP_BIAS = 0.3407435719249478       # measured bias (to remove)

# =============== FILE PATHS ===============
data_folder = "/home/aniket03/Desktop/IITG_Project_Raspi/AHT10/AHT10_data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

today = time.strftime("%Y-%m-%d")
csv_file = os.path.join(data_folder, f"humidity_log_{today}.csv")
error_file = os.path.join(data_folder, "humidity_error_log.txt")

if not os.path.exists(csv_file):
    with open(csv_file, "w") as f:
        f.write("Time,Humidity,Temperature\n")

# =============== READ AND LOG ===============
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

try:
    temperature_c = sensor.temperature
    humidity = sensor.relative_humidity
    # Applying calibration correction
    corrected_humidity = humidity + HUMIDITY_BIAS  
    corrected_temp = temperature_c + TEMP_BIAS
    
    if corrected_humidity is not None and corrected_temp is not None:
        with open(csv_file, "a") as f:
            f.write(f"{timestamp},{corrected_humidity:.2f},{corrected_temp:.2f}\n")
        print(f"{timestamp}  Humidity={corrected_humidity:.2f}%  Temp={corrected_temp:.2f}°C")
    else:
        raise ValueError("Invalid AHT10 reading")

except Exception as e:
    error_message = f"{timestamp}  Failed to read from AHT10: {e}\n"
    with open(error_file, "a") as f:
        f.write(error_message)
    print(error_message)
