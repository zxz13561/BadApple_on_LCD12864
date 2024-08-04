import time
from machine import Pin, SPI


class LCD12864_parallel(object):
    def __init__(self, rst, RS, RW, E, DataPin: list):
        self.rst = Pin(rst, Pin.OUT, Pin.PULL_DOWN)
        self.RS = Pin(RS, Pin.OUT, Pin.PULL_DOWN)
        self.RW = Pin(RW, Pin.OUT, Pin.PULL_DOWN)
        self.E = Pin(E, Pin.OUT, Pin.PULL_DOWN)
        self.D0 = Pin(DataPin[0], Pin.OUT, Pin.PULL_DOWN)
        self.D1 = Pin(DataPin[1], Pin.OUT, Pin.PULL_DOWN)
        self.D2 = Pin(DataPin[2], Pin.OUT, Pin.PULL_DOWN)
        self.D3 = Pin(DataPin[3], Pin.OUT, Pin.PULL_DOWN)
        self.D4 = Pin(DataPin[4], Pin.OUT, Pin.PULL_DOWN)
        self.D5 = Pin(DataPin[5], Pin.OUT, Pin.PULL_DOWN)
        self.D6 = Pin(DataPin[6], Pin.OUT, Pin.PULL_DOWN)
        self.D7 = Pin(DataPin[7], Pin.OUT, Pin.PULL_DOWN)

    def send_bytes(self, vRS, vRW, val):
        self.RS.value(vRS)
        self.RW.value(vRW)
        self.D0.value(val & 1)
        self.D1.value((val & 2) >> 1)
        self.D2.value((val & 4) >> 2)
        self.D3.value((val & 8) >> 3)
        self.D4.value((val & 16) >> 4)
        self.D5.value((val & 32) >> 5)
        self.D6.value((val & 64) >> 6)
        self.D7.value((val & 128) >> 7)
        self.E.value(1)
        time.sleep_ms(1)
        self.E.value(0)

    def send_command(self, comm):
        self.send_bytes(0, 0, comm)

    def print_char(self, comm):
        self.send_bytes(1, 0, comm)

    def print_line(self, msg):
        for c in msg:
            self.print_char(ord(c))

    def init(self):
        self.RS.value(0)
        self.RW.value(0)
        self.D0.value(0)
        self.D1.value(0)
        self.D2.value(0)
        self.D3.value(0)
        self.D4.value(0)
        self.D5.value(0)
        self.D6.value(0)
        self.D7.value(0)
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
