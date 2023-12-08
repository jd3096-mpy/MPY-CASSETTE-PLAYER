from machine import Pin, SPI
import st7789

TFA = 0
BFA = 0

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11)),
        135,
        240,
        reset=Pin(9, Pin.OUT),
        cs=Pin(7, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(9, Pin.OUT),
        color_order=st7789.RGB,
        inversion=True,
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)