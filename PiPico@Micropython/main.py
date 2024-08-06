import time

import micropython
from machine import Pin, UART
from LCD12864 import LCD12864Parallel

pLED = Pin("LED", Pin.OUT)

uart = UART(0, 230400, rx=Pin(17), tx=Pin(16))


def datetime():
    _t = time.localtime()
    return f"{_t[0]}-{_t[1]}-{_t[2]} {_t[3]}:{_t[4]}:{_t[5]}"


@micropython.native
def main():
    pLED.off()
    time.sleep(1)
    print("Program start")
    pLED.on()

    # Init a LCD 2004 object
    lcd = LCD12864Parallel(
        8,  # RS pin
        9,  # R/W pin
        10,  # E pin
        [0, 1, 2, 3, 4, 5, 6, 7]  # Data pins number
    )
    lcd.clean()

    # Turn on the cursor
    lcd.cursor_home()
    lcd.write_string(datetime())
    lcd.on()

    _tmr = time.time()
    uart.write(b'REQ')

    while time.time() - _tmr < 5:
        if uart.any():
            _tmr = time.time()
            uart.readinto(lcd.draw_buf, 1024)

            # print(len(_recv))
            lcd.clean()
            lcd.draw_frame_progressive()
            # lcd.draw_frame_interlaced()
            # time.sleep_ms(200)
            uart.write(b'REQ')
    print("Program stop")
    pLED.off()


if __name__ == '__main__':
    main()
