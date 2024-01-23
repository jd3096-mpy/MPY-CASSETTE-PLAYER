import sdcard
from machine import SPI, Pin
import os
mp='/sd'
sdcs = Pin(17, Pin.OUT, value=1)  
spi = SPI(0,baudrate=2000000,sck=Pin(18), mosi=Pin(19), miso=Pin(16))
sd = sdcard.SDCard(spi, sdcs)
vfs = os.VfsFat(sd)
os.mount(vfs, mp)
import os
os.sync()
print(os.statvfs('/sd'))

# import os
# def diskfree(d=''):
#     try:
#         a = os.statvfs(d)
#         return a[0]*a[3]
#     except:
#         return 0
#     
# def disksize(d=''):
#     try:
#         a = os.statvfs(d)
#         return a[0]*a[2]
#     except:
#         return 0
#     
# a=diskfree('/sd')
# b=disksize('/sd')
# print(a,b)

import os

def list_mp3_files(directory):
    mp3_files = []
    for item in os.listdir(directory):
        item_path = directory+'/'+item
        if os.stat(item_path)[0] & 0o100000 != 0:
            if item.lower().endswith('.mp3'):
                mp3_files.append(item_path[])
        elif os.stat(item_path)[0] & 0o040000 != 0:
            mp3_files.extend(list_mp3_files(item_path))
    
    return mp3_files

# 指定目录
target_directory = '/sd'

# 获取MP3文件列表
mp3_files_list = list_mp3_files(target_directory)

# 打印文件名列表
for mp3_file in mp3_files_list:
    print(mp3_file)
    


