ll=['/sd/Hotel California.mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u4e00\u5934\u5076\u50cf.mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u8fd9\u4e2a\u4e16\u754c\u4f1a\u597d\u5417 (2016 unplugged).mp3', '/sd/\u903c\u54e5/\u674e\u5fd7,\u6731\u683c\u4e50,\u5f20\u6021\u7136 - \u70ed\u6cb3 (2016 unplugged).mp3', '/sd/\u903c\u54e5/\u5899\u4e0a\u7684\u5411\u65e5\u8475 (2014i-O\u73b0\u573a\u7248).mp3', '/sd/\u903c\u54e5/\u5c71\u9634\u8def\u7684\u590f\u5929 (2014i-O\u73b0\u573a\u7248).mp3', '/sd/\u903c\u54e5/\u9001\u522b.mp3', '/sd/\u903c\u54e5/\u8fd9\u4e2a\u4e16\u754c\u4f1a\u597d\u5417 (2014i-O\u73b0\u573a\u7248).mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u5899\u4e0a\u7684\u5411\u65e5\u8475.mp3', '/sd/\u903c\u54e5/Hey Jude.mp3', '/sd/\u903c\u54e5/\u5b9a\u897f (2014i-O\u73b0\u573a\u7248).mp3', '/sd/\u903c\u54e5/\u5170\u82b1\u8349.mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u6625\u672b\u7684\u5357\u65b9\u57ce\u5e02 (2016 unplugged).mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u5b9a\u897f (2016 unplugged).mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u5b9a\u897f.mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u5173\u4e8e\u90d1\u5dde\u7684\u8bb0\u5fc6 (2016 unplugged).mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u548c\u4f60\u5728\u4e00\u8d77.mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u9ed1\u8272\u4fe1\u5c01 (2016 unplugged).mp3', '/sd/\u903c\u54e5/\u674e\u5fd7 - \u9ed1\u8272\u4fe1\u5c01.mp3', '/sd/\u8bb8\u5dcd/\u8bb8\u5dcd - \u6545\u4e61(Live).mp3', '/sd/\u8bb8\u5dcd/\u8bb8\u5dcd - \u84dd\u83b2\u82b1(Live).mp3', '/sd/\u8bb8\u5dcd/\u8bb8\u5dcd - \u65c5\u884c(Live).mp3', '/sd/\u8bb8\u5dcd/\u8bb8\u5dcd - \u90a3\u4e00\u5e74(Live).mp3', '/sd/\u8bb8\u5dcd/\u8bb8\u5dcd - \u6e29\u6696(Live).mp3', '/sd/\u8bb8\u5dcd/\u8bb8\u5dcd - \u661f\u7a7a(Live).mp3', '/sd/\u6c6a\u5cf0/\u6625\u5929\u91cc (Live).mp3', '/sd/\u6c6a\u5cf0/\u5b58\u5728 (Live).mp3', '/sd/\u6c6a\u5cf0/\u82b1\u706b (Live).mp3', '/sd/\u6c6a\u5cf0/\u50cf\u4e2a\u5b69\u5b50 (Live).mp3', '/sd/\u5176\u4ed6/\u559c\u6b22\u4f60(Live).mp3', '/sd/\u5176\u4ed6/\u5149\u8f89\u5c81\u6708(Live).mp3', '/sd/\u5176\u4ed6/\u8389\u8389\u5b89.mp3', '/sd/\u5176\u4ed6/\u79e6\u7687\u5c9b.mp3', '/sd/\u5176\u4ed6/\u8c01\u4f34\u6211\u95ef\u8361(Live).mp3', '/sd/\u5176\u4ed6/\u7f51\u6613\u4e91/\u6ee5\u4fd7\u7684\u6b4c.mp3']

import sdcard
from machine import SPI, Pin
import os
mp='/sd'
sdcs = Pin(17, Pin.OUT, value=1)  
spi = SPI(0,baudrate=2000000,sck=Pin(18), mosi=Pin(19), miso=Pin(16))
sd = sdcard.SDCard(spi, sdcs)
vfs = os.VfsFat(sd)
os.mount(vfs, mp)

class FILEMENU:
    def __init__(self):
        self.root='/sd'
        self.nowcwd='/sd'
        self.nowlist=[]
        self.nowlist=os.listdir(self.root)
        self.nowmax=len(self.nowlist)
        self.folder='sd'
        self.cursor=0
        self.num=0
        self.display()

    def add_option(self, option, callback):
        self.options[option] = callback

    def display(self):
        show_list = self.nowlist[self.num:self.num+4]
        while len(show_list) < 4:
            show_list.append('')
        print(show_list)
        print(self.cursor)

    def up(self):
        if self.cursor!=0:
            self.cursor-=1
        else:
            if self.num!=0:
                self.num-=1
    
    def down(self):
        if self.cursor!=3:
            self.cursor+=1
        else:
            if self.num+4<self.nowmax:
                self.num+=1
    
    def ok(self):
        filenum=self.num+self.cursor
        print(ll[filenum])

menu=FILEMENU()
for i in range(0,8):
    menu.down()
    menu.display()

for i in range(0,2):
    menu.up()
    menu.display()

menu.ok()





