import time
from machine import Pin, SPI


class LCD12864(object):
    def __init__(self, lcd_spi: SPI, reset_pin):
        self.spi = lcd_spi
        self.rst = Pin(reset_pin, Pin.OUT, Pin.PULL_DOWN)

        self.init()

    def send_bytes(self, comm_list):
        self.spi.write(bytearray(comm_list))

    def send_command(self, comm):
        _comm_list = [
            0xF8,
            comm & 0xF0,
            (comm << 4) & 0xF0
        ]
        self.send_bytes(_comm_list)

    def print_char(self, char_hex):
        _comm_list = [
            0xFA,
            char_hex & 0xF0,
            (char_hex << 4) & 0xF0
        ]
        self.send_bytes(_comm_list)

    def print_line(self, msg):
        for c in msg:
            self.print_char(ord(c))

    def init(self):
        # Toggle reset pin
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

        # Send init command
        self.send_command(0x30)
        self.send_command(0x0C)
        self.send_command(0x01)
        self.send_command(0x06)

    def on(self):
        self.send_command(0x0C)

    def clean(self):
        self.send_command(0x01)
        time.sleep_ms(1)

    def cursor_home(self):
        self.send_command(0x02)

    def draw(self, pixel_arr):
        for y_line in range(64):
            if y_line < 32:
                x = 0x80
                y = y_line + 0x80
            else:
                x = 0x88
                y = y_line - 32 + 0x80

            self.send_command(0x36)
            self.send_command(y)
            self.send_command(x)
            self.send_command(0x32)

            tmp = y_line * 16

            for i in range(16):
                pixel_val = pixel_arr[tmp + i]
                self.print_char(pixel_val)

            self.send_command(0x34)
            self.send_command(0x36)
