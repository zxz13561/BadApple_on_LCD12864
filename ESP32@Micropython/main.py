import time
import uos
import machine
from machine import Pin
import sdcard
from lib_LCD12864 import LCD12864
import _thread

# Assign chip select (CS) pin (and start it high)
cs = Pin(15, Pin.OUT)

# Initialize SPI peripheral (start with 1 MHz)
spi_sd = machine.SPI(1,
                     baudrate=20_000_000,
                     polarity=0,
                     phase=0,
                     bits=8,
                     firstbit=machine.SPI.MSB,
                     sck=Pin(14),
                     mosi=Pin(13),
                     miso=Pin(12))

spi_lcd = machine.SPI(2,
                      baudrate=20_000_000,
                      polarity=0,
                      phase=0,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=Pin(18),
                      mosi=Pin(23),
                      miso=Pin(19))

# Initialize SD card
sd = sdcard.SDCard(spi_sd, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
print("Start mount sdcard")

uos.mount(vfs, "/sd")
# print(uos.listdir("/sd"))

lcd = LCD12864(spi_lcd, 22)
lcd.cursor_home()
lcd.print_line("LCD ON")
time.sleep(1)

lock = _thread.allocate_lock()

frame_data = ()


def read_frame():
    global frame_data
    for idx in range(120):
        frame_show = False
        print(f"Loading frame: {idx}")
        file_name = f"f{idx:03d}"
        f = open("/sd/" + file_name, 'r')
        data_str = f.readline()[1:-1]
        if lock.acquire():
            frame_data = [int(h) for h in data_str.split(',')]
            lock.release()
        f.close()
    _thread.exit()


def show_frame():
    global frame_data
    time.sleep(0.1)
    while True:
        # lcd.clean()
        if lock.acquire():
            lcd.draw(frame_data)
            lock.release()
        time.sleep_ms(80)


if __name__ == '__main__':
    print("Program Start")
    _thread.start_new_thread(read_frame, ())
    _thread.start_new_thread(show_frame, ())
