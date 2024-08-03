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

    for idx in range(10):
        file_name = f"f{idx:03d}"
        f = open("/sd/" + file_name, 'r')
        data_str = f.readline()[1:-1]
        data_tuple = eval(data_str)
        print(data_tuple)
        f.close()


