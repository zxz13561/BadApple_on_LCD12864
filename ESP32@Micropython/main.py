import uos
import machine
import sdcard

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(15, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(14),
                  mosi=machine.Pin(13),
                  miso=machine.Pin(12))

if __name__ == '__main__':
    print("Program Start")

    # Initialize SD card
    sd = sdcard.SDCard(spi, cs)

    # Mount filesystem
    vfs = uos.VfsFat(sd)
    print("Start mount sdcard")

    uos.mount(vfs, "/sd")
    print(uos.listdir("/sd"))

    f = open("sd/test.txt")
    for _l in f.readlines():
        print(_l)
