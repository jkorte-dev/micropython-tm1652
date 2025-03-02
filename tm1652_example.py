from machine import UART
import time
from tm1652 import TM1652, SEGMENTS


def test_display():
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
