from machine import Pin, SPI
import st7789

TFA = 0
BFA = 0

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(0, baudrate=60000000, sck=Pin(18), mosi=Pin(19)),
        135,
        240,
        reset=Pin(20, Pin.OUT),
        cs=Pin(22, Pin.OUT),
        dc=Pin(21, Pin.OUT),
        backlight=Pin(26, Pin.OUT),
        color_order=st7789.RGB,
        inversion=True,
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)