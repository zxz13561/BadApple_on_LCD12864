import os
from time import perf_counter
import serial
from datetime import datetime
import hex_arr1
import hex_arr2
import hex_arr3
import hex_arr4
import hex_arr5
import hex_arr6
import hex_arr7
import hex_arr8

# Function by board type
board_list = ["STM32F1", "ESP32"]
board_type = board_list[0]

# Init Serial
port = "/dev/tty.usbserial-1120"
ser = serial.Serial(port, baudrate=230400, bytesize=8, parity=serial.PARITY_NONE, stopbits=1)

# Setup index range
f_idx = 0
file_list = (hex_arr1, hex_arr2, hex_arr3, hex_arr4, hex_arr5, hex_arr6, hex_arr7, hex_arr8)
range_list = [0]
for f in file_list:
    range_list.append(len(f.all_frame) + range_list[-1])

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
            # time.sleep(0.0005)

    # Check receive is REQ and send frame bytes array
    if recv != b'' and recv.decode() == "REQ":
        # Record time usage
        time_usage.append(perf_counter() - tmr)
        tmr = perf_counter()
        # print(f"{datetime.now()} Get board message: {recv.decode()}")

        # Select frame file by index
        if f_idx < range_list[1]:
            _f = file_list[0].all_frame[f_idx]
        elif f_idx < range_list[2]:
            _f = file_list[1].all_frame[f_idx - range_list[1]]
        elif f_idx < range_list[3]:
            _f = file_list[2].all_frame[f_idx - range_list[2]]
        elif f_idx < range_list[4]:
            _f = file_list[3].all_frame[f_idx - range_list[3]]
        elif f_idx < range_list[5]:
            _f = file_list[4].all_frame[f_idx - range_list[4]]
        elif f_idx < range_list[6]:
            _f = file_list[5].all_frame[f_idx - range_list[5]]
        elif f_idx < range_list[7]:
            _f = file_list[6].all_frame[f_idx - range_list[6]]
        elif f_idx < range_list[8]:
            _f = file_list[7].all_frame[f_idx - range_list[7]]
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
                # time.sleep(0.0005)
        else:
            ser.write(bytearray(_f))

        # Print out frame index number and start waiting next frame
        print(f"{datetime.now()} Send frame: {f_idx}")
        f_idx += 1

# Calculate FPS
_total = sum(time_usage[1:])  # Skip first
_avg_t = round(_total / (len(time_usage) - 2), 3)
print(f"Average time usage: {_avg_t}")
print(f"Average FPS: {round(1 / _avg_t, 2)}")
