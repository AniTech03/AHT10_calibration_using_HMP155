###### Using HMP Sensor for Tin & RHin logging (1-min interval) ######

import serial
import os
import time
import re
from datetime import datetime

# =============== SETTINGS ===============
SERIAL_PORT = '/dev/ttyACM0'   # Change to /dev/ttyUSB0 if needed
BAUDRATE = 4800
DATA_DIR = "/home/aniket03/Desktop/IITG_Project_Raspi/HMP/HMP_data"

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# =============== FILE SETUP ===============
today = datetime.now().strftime("%Y-%m-%d")
csv_file = os.path.join(DATA_DIR, f"HMP_{today}.csv")
error_file = os.path.join(DATA_DIR, "HMP_error_log.txt")

# Create file with header if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, "w") as f:
        f.write("Date,Time,Tin,RHin\n")

# =============== SERIAL CONNECTION ===============
try:
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=2
    )
except Exception as e:
    with open(error_file, "a") as f:
        f.write(f"{datetime.now()}  Serial open error: {e}\n")
    raise SystemExit(f"Serial open error: {e}")

# =============== READ DATA ===============
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M")

try:
    # Some HMP sensors require a SEND command; comment out if unnecessary
    ser.write(b"SEND\r")
    time.sleep(0.5)

    line = ser.readline().decode(errors="ignore").strip()

    # Expected: RH= 56.4 %RH  T= 25.7
    match = re.search(r"RH=\s*([\d.]+).*?T=\s*([\d.]+)", line)
    if match:
        RHin = float(match.group(1))
        Tin = float(match.group(2))

        with open(csv_file, "a") as f:
            f.write(f"{date_str},{time_str},{Tin:.2f},{RHin:.2f}\n")

        print(f"{date_str} {time_str}  Tin={Tin:.2f}°C  RHin={RHin:.2f}%")

    else:
        raise ValueError(f"Unexpected data format: '{line}'")

except Exception as e:
    with open(error_file, "a") as f:
        f.write(f"{date_str} {time_str}  Failed to read from HMP: {e}\n")
    print(f"{date_str} {time_str}  Failed to read from HMP: {e}")

finally:
    ser.close()
