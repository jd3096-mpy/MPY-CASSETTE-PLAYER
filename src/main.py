from machine import Pin
b=Pin(4,Pin.IN,Pin.PULL_UP)

def boot_mode():
    import machine
    import st7789
    import time
    from machine import Pin
    import tft_config
    bl=Pin(6,Pin.OUT)
    bl.value(0)
    tft=tft_config.config(1)
    tft.init()
    tft.fill(0xffff)
    tft.jpg('img/update.jpg',0,0,st7789.SLOW)
    time.sleep(2)
    s=Pin(5,Pin.IN,Pin.PULL_UP)
    while s.value()==1:
        pass
    machine.bootloader(True)
    
if b.value()==0:
    boot_mode()
#----------------------MAIN-------------------------
import gc
gc.enable()
import uasyncio as asyncio
from lib.cassette import CASSETTE
gc.collect()
tape=CASSETTE()
asyncio.run(tape.main())