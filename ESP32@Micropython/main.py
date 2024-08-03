import time
import uos
import machine
from machine import Pin
import sdcard

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(15, machine.Pin.OUT)

# Initialize SPI peripheral (start with 1 MHz)
spi_sd = machine.SPI(1,
                     baudrate=1000000,
                     polarity=0,
                     phase=0,
                     bits=8,
                     firstbit=machine.SPI.MSB,
                     sck=machine.Pin(14),
                     mosi=machine.Pin(13),
                     miso=machine.Pin(12))

spi_lcd = machine.SPI(2,
                      baudrate=1000000,
                      polarity=0,
                      phase=0,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=machine.Pin(18),
                      mosi=machine.Pin(23),
                      miso=machine.Pin(19))


class LCD12864(object):
    def __init__(self, lcd_spi, reset_pin):
        self.spi = lcd_spi
        self.rst = Pin(reset_pin, Pin.OUT, Pin.PULL_DOWN)

    def send_bytes(self, comm_list):
        self.spi.write(bytearray(comm_list))

    def send_command(self, comm):
        _comm_list = [
            0xF8,
            comm & 0xF0,
            (comm << 4) & 0xF0
        ]
        self.send_bytes(_comm_list)

    def send_char(self, char_hex):
        _comm_list = [
            0xFA,
            char_hex & 0xF0,
            (char_hex << 4) & 0xF0
        ]
        self.send_bytes(_comm_list)

    def print_line(self, msg):
        for c in msg:
            self.send_char(ord(c))

    def lcd_init(self):
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

    def lcd_on(self):
        self.send_command(0x0C)

    def lcd_clear(self):
        self.send_command(0x30)
        self.send_command(0x01)

    def cursor_home(self):
        self.send_command(0x02)


if __name__ == '__main__':
    print("Program Start")

    # Initialize SD card
    sd = sdcard.SDCard(spi_sd, cs)

    # Mount filesystem
    vfs = uos.VfsFat(sd)
    print("Start mount sdcard")

    uos.mount(vfs, "/sd")
    # print(uos.listdir("/sd"))

    # for idx in range(10):
    #     file_name = f"f{idx:03d}"
    #     f = open("/sd/" + file_name, 'r')
    #     data_str = f.readline()[1:-1]
    #     data_tuple = eval(data_str)
    #     print(data_tuple)
    #     f.close()

    lcd = LCD12864(spi_lcd, 22)
    lcd.lcd_init()
    lcd.cursor_home()
    lcd.print_line("Hello World!!")

