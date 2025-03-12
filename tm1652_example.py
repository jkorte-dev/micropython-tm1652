from machine import UART, Pin
import time
from tm1652 import TM1652, SEGMENTS


class FakeUART:

    def __init__(self, sda_pin, delay=None):
        self.sda_pin = sda_pin
        sda_pin.init(Pin.OUT)
        self.delay = delay

    def write(self, buf):
        for data in buf:
            self.writechar(data)

    def writechar(self, data):
        # Send a byte to the chip the way the TM1652 likes it (LSB-first, UART serial 8E1 - 8 bits,
        # parity bit set to 0 when odd, one stop bit)
        #  - start bit, 8x data bits, parity bit, stop bit; 52 us = 19200bps
        t = time.ticks_us()
        bit_delay = self.delay
        parity = True
        r = range(8)
        gpio = self.sda_pin.value
        idle = time.sleep_us

        # state = machine.disable_irq() # todo noInterrupts();

        # start - low
        gpio(0)
        idle(bit_delay)

        for _ in r:
            if data & 1:
                parity = not parity
            gpio(data & 1)
            data >>= 1
            idle(bit_delay)

        # parity - low when odd
        gpio(int(parity))
        idle(bit_delay)

        # stop - high
        gpio(1)

        # machine.enable_irq(state) #todo interrupts();
        idle(bit_delay)

        # idle - remain high
        idle(bit_delay)
        return time.ticks_diff(time.ticks_us(), t)

    def init(self, baudrate=19200, bits=8, parity=None, stop=1, timeout=0):
        if not self.delay:
            timing = 1 / baudrate * 1e6  # µs
            target_t = timing * 12  # 11 waits per byte
            sample = bytearray([0x0d])
            for d in range(4, timing):  # delay in µs
                self.delay = d
                t = self.writechar(sample[0])  # µs
                if target_t < t < (target_t + 75):
                    print(f"calibrated.  {target_t} µs, ∂:{t-target_t} µs, delay:{d} µs")
                    break

    def close(self):
        pass  # nothing to do


def test_display():
    # uart = FakeUART(Pin('B1', Pin.OUT)) # stm32f411 using gpio pin B1 instead of uart tx
    # uart = UART(2, 19200) # stm32f411 tx=PA2
    uart = UART(1, 19200)  # esp8266 tx=D4 (gpio2)

    display = TM1652(uart)

    display.clear()
    # display.set_brightness(3)  # 5V(3) 3.3V (7)
    display.show_text("BEEF")
    time.sleep(1)
    display.show_text("AC")
    time.sleep(1)
    display.show_text("-1000*")
    # text scroll
    display.scroll("Hello World")
    time.sleep(1)
    # clock example
    for _ in range(0, 10):
        hms = time.localtime()[3:6]
        display.display_clock(*hms)
        time.sleep(1)
        display.display_clock(*hms)
    time.sleep(1)
    # show float
    display.show_text(f'{15.3:05.1f}')
    time.sleep(1)
    # counter int
    for n in range(250, -1, -1):
        time.sleep(0.05)
        display.show_text(f'{n:04d}')
    # each led segment
    dig = 0
    for n in range(0, 8):
        dig |= 1 << n
        time.sleep(0.5)
        display._write_dig(dig, dig, dig, dig)
    time.sleep(1)
    # all fonts
    display.scroll(list(SEGMENTS))
    display.clear()
    display.show_text("End")
    for v in range(3, 8):
        display.set_brightness(v)
        time.sleep(0.2)
    for v in range(7, -1, -1):
        time.sleep(0.2)
        display.set_brightness(v)


if __name__ == "__main__":
    test_display()
