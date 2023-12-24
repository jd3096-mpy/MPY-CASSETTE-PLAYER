from machine import Pin
b=Pin(4,Pin.IN,Pin.PULL_UP)
if b.value()==0:
    import machine
    machine.bootloader(True)

import gc
gc.enable()
import uasyncio as asyncio
from lib.cassette import CASSETTE

tape=CASSETTE()

asyncio.run(tape.main())