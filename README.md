TM1652 4x7-Segments LED Display with Micropython
=========================================================================================


Micropython example code for [WeActStudio Digital Tube Module](https://github.com/WeActStudio/WeActStudio.DigitalTubeModule) (TM1652) 4x7 segments LED display.

The module uses serial communication to control the LEDs. Connect the provided red cable (labeled with SDA) with the TX port of your MCU, the yellow cable with VCC (3.3 or 5V) and GND to ground (black cable).
Color coding is misleading but just follow the labeling on the module.

Important notes:

1. *communication with the tm1652 uses UART and needs to be set to parity odd.*
2. *brightness value is 4 bits reversed order (data sheet page 6)*
3. *default brightness is 0, therefore you have to set brightness to see anything. In tm1652.py 3 is set as default*

Mimimal code to display the numbers 0 to 3 on the display is:

```code
from machine import UART
import time

uart = UART(1, 19200)
uart.init(19200, bits=8, parity=1, stop=1, timeout=50)
uart.write(bytearray(b'\x18\x1c')) # set brightness to 3
time.sleep(0.006)
uart.write(bytearray(b'\x08\x3f\x06\x5B\x4f')) # display numbers
```

More convenient way using `tm1652.py`:

```code 
from machine import UART

uart = UART(1, 19200)
display = TM1652(uart)
display.show_text("0123")
```

See `tm1652_exmaple.py` for more.

### Resources
Compiled from the following resource:

- [Mike Causer TM1638 driver](https://github.com/mcauser/micropython-tm1637) (most code borrowed from there)
- WeActStudio Python / Arduino examples