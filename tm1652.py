import time

# WeActStudio.DigitalTubeModule (TM1652) micropython example

# 0-9, a-z, blank, dash, star
SEGMENTS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')

_DOT = const(0x80) # 1<<7
_CTLCMD = const(0x18)
_ADRCMD = const(0x08)


class TM1652:

    def __init__(self, uart, brightness=3):
        uart.init(19200, bits=8, parity=1, stop=1, timeout=50)
        self.uart = uart
        self.set_brightness(brightness)
        self.clear()

    def _write_cmd(self, cmd):
        self.uart.write(cmd)
        time.sleep(0.006)

    def set_brightness(self, brightness):
        def reverse(b):
            b = (b & 0b11110000) >> 4 | (b & 0b00001111) << 4
            b = (b & 0b11001100) >> 2 | (b & 0b00110011) << 2
            b = (b & 0b10101010) >> 1 | (b & 0b01010101) << 1
            return b

        if brightness < 0 or brightness > 7:
            return
        else:
            bright_value = reverse(brightness) >> 4 & 0x0F
            self._write_cmd(bytearray([0x18, 0x10 | bright_value]))

    def _write_dig(self, dig1, dig2, dig3, dig4):
        self._write_cmd(bytearray([0x08, dig1, dig2, dig3, dig4]))

    def display_clock(self, hour, minute, second):
        dot = '.' if second % 2 else ''
        clock = f'{hour//10}{hour%10}{dot}{minute//10}{minute%10}'
        self.show_text(clock)

    def clear(self):
        self._write_dig(0, 0, 0, 0)

    def close(self):
        self.clear()
        self.uart.close()
    
    # stolen from https://github.com/mcauser/micropython-tm1638/blob/master/tm1638.py    
    def encode_char(self, char):
        """Convert a character 0-9, a-z, space, dash or star to a segment."""
        o = ord(char)
        if o == 32:
            return SEGMENTS[36]  # space
        if o == 42:
            return SEGMENTS[38]  # star/degrees
        if o == 45:
            return SEGMENTS[37]  # dash
        if 65 <= o <= 90:
            return SEGMENTS[o - 55]  # uppercase A-Z
        if 97 <= o <= 122:
            return SEGMENTS[o - 87]  # lowercase a-z
        if 48 <= o <= 57:
            return SEGMENTS[o - 48]  # 0-9
        print("Character out of range: {:d} '{:s}'".format(o, chr(o)))
        return 0x00

    def encode_string(self, string):
        """Convert string containing 0-9, a-z, space, dash, star to an array of
        segments, matching the length of the source string excluding dots, which
        are merged with previous char."""
        segments = bytearray(len(string.replace('.', '')))
        j = 0
        for i in range(len(string)):
            if string[i] == '.' and j > 0:
                segments[j-1] |= _DOT
                continue
            segments[j] = self.encode_char(string[i])
            j += 1
        return segments

    def scroll(self, string, delay=250):
        """Display a string, scrolling from the right to left, speed adjustable.
        String starts off-screen right and scrolls until off-screen left."""
        segments = string if isinstance(string, list) or isinstance(string, bytearray) else self.encode_string(string)
        
        data = [0] * 16
        data[4:0] = list(segments)
        for i in range(len(segments) + 5):
            self._write_dig(*tuple(data[0+i:4+i]))
            time.sleep_ms(delay)
    
    def show_text(self, text):
        data = self.encode_string(f'{text:>4}')
        if len(data) == 4:
            self._write_dig(*tuple(data))
        else:
            self.scroll(data)
