import time
import micropython
from machine import Pin

code1 = const(0x32)
code2 = const(0x34)
code3 = const(0x36)


class LCD12864Parallel(object):
    def __init__(self, RS: int, RW: int, E: int, D: list):
        # Actual LCD block index mapping
        self.cursor_map = tuple(range(0, 20)) + tuple(range(40, 60)) + tuple(range(20, 40)) + tuple(range(60, 80))
        self.cursor_idx = 0
        self.draw_buf = bytearray(1024)
        self.frame_odd = True

        # Init pins
        self.pRS = Pin(RS, Pin.OUT)
        self.pRS = Pin(RS, Pin.OUT)
        self.pRW = Pin(RW, Pin.OUT)
        self.pE = Pin(E, Pin.OUT)

        self.pD0 = Pin(D[0], Pin.OUT)
        self.pD1 = Pin(D[1], Pin.OUT)
        self.pD2 = Pin(D[2], Pin.OUT)
        self.pD3 = Pin(D[3], Pin.OUT)
        self.pD4 = Pin(D[4], Pin.OUT)
        self.pD5 = Pin(D[5], Pin.OUT)
        self.pD6 = Pin(D[6], Pin.OUT)
        self.pD7 = Pin(D[7], Pin.OUT)

        # Init LCD
        self.init()

    @micropython.viper
    def parallel_write(self, rs: int, rw: int, val: int):
        _val = uint(val)
        self.pE.on()

        # Setup RS and R/W pins
        self.pRS.value(rs)
        self.pRW.value(rw)

        # Setup data pins
        self.pD0.value(_val & 1)
        self.pD1.value((_val & 2) >> 1)
        self.pD2.value((_val & 4) >> 2)
        self.pD3.value((_val & 8) >> 3)
        self.pD4.value((_val & 16) >> 4)
        self.pD5.value((_val & 32) >> 5)
        self.pD6.value((_val & 64) >> 6)
        self.pD7.value((_val & 128) >> 7)

        # pin E cycle minimum time is 1000ns
        # time.sleep(0.0015)
        self.pE.off()

    def write_command(self, comm):
        self.parallel_write(0, 0, comm)

    def init(self):
        self.write_command(0x30)
        self.write_command(0x0C)
        self.write_command(0x01)
        self.write_command(0x06)

    def clean(self):
        self.write_command(0b00000001)
        time.sleep_us(800)

    def cursor_home(self):
        self.cursor_idx = 0
        self.write_command(0b00000010)

    def on(self):
        self.write_command(0b00001100)

    def off(self):
        self.write_command(0b00001000)

    def cursor_on(self):
        self.write_command(0b00001111)

    def cursor_off(self):
        self.write_command(0b00001100)

    def cursor_move(self, direction: int):
        if direction >= 1:  # move right
            for _ in range(0, direction):
                self.write_command(0b00010100)

        elif direction <= -1:  # move left
            for _ in range(direction, 0):
                self.write_command(0b00010000)
        else:
            return

    def cursor_move_index(self, idx: int):
        # Move cursor to home position
        self.cursor_home()

        # Get real index from cursor index tuple
        _real_idx = self.cursor_map[idx]

        # Move cursor
        self.cursor_move(_real_idx)

    def cursor_change_line(self, line_num: int):
        # Move cursor to home position
        self.cursor_home()

        # Move cursor left by index
        _idx = self.cursor_map[line_num * 20]

        # Move cursor
        self.cursor_move(_idx)

    def write_char(self, c: chr):
        self.parallel_write(1, 0, ord(c))

    def write_string(self, s: str):
        for _c in s:
            self.write_char(_c)

    def write_line(self, line_num: int, s: str):
        self.cursor_change_line(line_num)

        # Slice string if it is over 20 character
        _print_s = s[:20]

        # Print string
        self.write_string(s)

    @micropython.viper
    def draw_frame_interlaced(self):
        _buf = ptr8(self.draw_buf)

        _st = 0 if self.frame_odd else 1

        for y_line in range(_st, 64, 2):
            if y_line < 32:
                x = 0x80
                y = y_line + 0x80
            else:
                x = 0x88
                y = y_line - 32 + 0x80

            self.write_command(code3)
            self.write_command(y)
            self.write_command(x)
            self.write_command(code1)

            tmp = y_line * 16

            for i in range(16):
                self.parallel_write(1, 0, _buf[tmp + i])

            self.write_command(code2)
            self.write_command(code3)

        self.frame_odd = not self.frame_odd

    @micropython.viper
    def draw_frame_progressive(self):
        _buf = ptr8(self.draw_buf)
        for y_line in range(64):
            if y_line < 32:
                x = 0x80
                y = y_line + 0x80
            else:
                x = 0x88
                y = y_line - 32 + 0x80

            self.write_command(code3)
            self.write_command(y)
            self.write_command(x)
            self.write_command(code1)

            tmp = y_line * 16

            for i in range(16):
                self.parallel_write(1, 0, _buf[tmp + i])

            self.write_command(code2)
            self.write_command(code3)
