import time
from time import perf_counter
import serial
from datetime import datetime
import hex_arr
import hex_arr2
import hex_arr3
import hex_arr4
import hex_arr5
import hex_arr6

# Function by board type
board_list = ["STM32F1", "ESP32"]
board_type = board_list[0]

# Init Serial
port = "/dev/tty.usbserial-1120"
ser = serial.Serial(port, baudrate=230400, bytesize=8, parity=serial.PARITY_NONE, stopbits=1)

# Setup index range
f_idx = 0
range1 = len(hex_arr.all_frame)
range2 = len(hex_arr2.all_frame2) + range1
range3 = len(hex_arr3.all_frame3) + range2
range4 = len(hex_arr4.all_frame4) + range3
range5 = len(hex_arr5.all_frame5) + range4
range6 = len(hex_arr6.all_frame6) + range5

# FPS counter
time_usage = []

# Start Program
tmr = perf_counter()
while True:
    # Receive REQ message from board
    recv = b''
    if ser.in_waiting:
        while ser.in_waiting:
            recv += ser.read(1)
            time.sleep(0.005)

    # Check receive is REQ and send frame bytes array
    if recv != b'' and recv.decode() == "REQ":
        # Record time usage
        time_usage.append(perf_counter() - tmr)
        tmr = perf_counter()
        print(f"{datetime.now()} Get board message: {recv.decode()}")

        # Select frame file by index
        if f_idx < range1:
            _f = hex_arr.all_frame[f_idx]
        elif f_idx < range2:
            _f = hex_arr2.all_frame2[f_idx - range2]
        elif f_idx < range3:
            _f = hex_arr3.all_frame3[f_idx - range3]
        elif f_idx < range4:
            _f = hex_arr4.all_frame4[f_idx - range4]
        elif f_idx < range5:
            _f = hex_arr5.all_frame5[f_idx - range5]
        elif f_idx < range6:
            _f = hex_arr6.all_frame6[f_idx - range6]
        else:
            # Finish and break
            break

        # Select send method by board type
        if board_type == "STM32F1":
            _head = 0
            _tail = 64
            for i in range(16):
                _len = 64 + (64 * i)
                ser.write(bytearray(_f[_head:_tail]))
                _head = _tail
                _tail += 64
                time.sleep(0.0005)
        else:
            ser.write(bytearray(_f))

        # Print out frame index number and start waiting next frame
        print(f"{datetime.now()} Send frame: {f_idx}")
        f_idx += 1

# Calculate FPS
_total = sum(time_usage[1:])  # Skip first
_avg_t = round(_total / (len(time_usage)-2), 3)
print(f"Average time usage: {_avg_t}")
print(f"Average FPS: {round(1/_avg_t, 2)}")
