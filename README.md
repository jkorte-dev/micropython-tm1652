TM1562 4x7-Segments LED Display with Micropython
=========================================================================================


Micropython example code for [WeActStudio Digital Tube Module](https://github.com/WeActStudio/WeActStudio.DigitalTubeModule) (TM1562) 4x7 segments LED display.

Important notes:

1. *communication with the tm1562 uses UART and needs to be set to parity odd.*
2. *setting brightness needs >>4 bit shift, bits reversed order*

### Resources
Compiled from the following resource:

- [Mike Causer TM1638 driver](https://github.com/mcauser/micropython-tm1637) (most code borrowed from there)
- WeActStudio Python / Arduino examples