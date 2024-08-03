import time
import machine
from machine import Pin, UART
from lib_LCD12864 import LCD12864

uart = UART(2, 230400)

spi_lcd = machine.SPI(2,
                      baudrate=20_000_000,
                      polarity=0,
                      phase=0,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=Pin(18),
                      mosi=Pin(23),
                      miso=Pin(19))

lcd = LCD12864(spi_lcd, 22)
lcd.cursor_home()
lcd.print_line("LCD ON")
time.sleep(1)


def show_frame():
    time.sleep(0.1)
    while True:
        # lcd.clean()
        lcd.draw(frame_data)
        time.sleep_ms(80)


if __name__ == '__main__':
    print("Program Start")

    uart.write(b'REQ')
    while True:
        if uart.any():
            _recv = b''
            while uart.any():
                _recv += uart.readline()
                time.sleep_ms(10)

            print(len(_recv))
            uart.write(b'REQ')
