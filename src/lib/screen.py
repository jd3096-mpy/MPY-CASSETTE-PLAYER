import st7789,tft_config
import framebuf,time
import uasyncio as asyncio
import gc
import vga8x8 as font
from machine import Pin,PWM
import wheel

class Screen:
    
    def __init__(self):
        self.tft=tft_config.config(1)
        self.tft.init()
        self.tft.fill(0)
        self.tft.jpg('img/logo1.jpg',65,10,st7789.SLOW)
        self.tft.jpg('img/logo2.jpg',20,80,st7789.SLOW)
        time.sleep(1)
        self.fblist=[]
        print(gc.mem_free())
        self.ani=False
        self.ani_num=1
        self.ani_max=15
        self.reverse=False
        self.speed=22
        self.bl=PWM(Pin(6))
        self.bl.freq(1000)
        self.bl.duty_u16(60000)
        ch_height=24
        ch_width=200
        self.ch_buffer = bytearray(ch_height * ch_width*2)
        self.ch_fb=framebuf.FrameBuffer(self.ch_buffer, ch_width, ch_height, framebuf.RGB565SW)
        self.ch_fb.font_load("GB2312-24.fon")
        self.ch_fb.font_set(0x13,0,1,0)
        self.ch_fb.fill(0xffff)
        self.menu_fb=framebuf.FrameBuffer(self.ch_buffer, 200, 24, framebuf.RGB565SW)
        self.menu_fb.font_load("GB2312-24.fon")
        self.menu_fb.font_set(0x13,0,1,0)
        
        self.tft.jpg('img/fantasy.jpg',0,0,st7789.SLOW)
        self.tft.jpg('img/b100.jpg',60,75,st7789.SLOW)
        self.tft.bitmap(wheel, 0, 75, 0)
        self.tft.bitmap(wheel, 180, 75, 0)
        
        self.current_index=0
        self.items_per_page=5
        self.select_index=0
        self.menu_items=[]
        
    async def animation(self):
        while 1:
            if self.ani:
                if not self.reverse:
                    if self.ani_num==1:
                        self.ani_num=self.ani_max
                    else:
                        self.ani_num-=1
                else:
                    if self.ani_num==self.ani_max:
                        self.ani_num=1
                    else:
                        self.ani_num+=1
                self.tft.bitmap(wheel, 0, 75, self.ani_num-1)
                self.tft.bitmap(wheel, 180, 75, self.ani_num-1)
                await asyncio.sleep_ms(self.speed)
            else:
                await asyncio.sleep_ms(1)
                
    def show_battery(self,b):
        if self.ani:
            if b==4:
                self.tft.jpg('img/b100.jpg',60,75)
            elif b==3:
                self.tft.jpg('img/b75.jpg',60,75)
            elif b==2:
                self.tft.jpg('img/b50.jpg',60,75)
            elif b==1:
                self.tft.jpg('img/b25.jpg',60,75)
        
    def play(self):
        self.ani=True
        self.speed=22
        self.reverse=False
    def song_name(self,name):
        self.ch_fb.fill(0xffff)
        self.ch_fb.text(name,0,0,0x0)
        self.tft.blit_buffer(self.ch_buffer, 30, 36, 200,24)
                
    def stop(self):
        self.ani=False
        self.reverse=False
        
    def fast_forward(self):
        self.ani=True
        self.speed=2
        self.reverse=False
        
    def fast_reverse(self):
        self.ani=True
        self.speed=2
        self.reverse=True
        
    def setting(self,choose,s1,s2,s3,shuffle):
        gray=st7789.color565(40,40,44)
        blue=st7789.color565(184,212,254)
        white=st7789.color565(222,222,222)
        self.tft.jpg('img/spin'+str(s1)+'.jpg',15,2,st7789.FAST)
        self.tft.jpg('img/spin'+str(s2)+'.jpg',90,2,st7789.FAST)
        self.tft.jpg('img/spin'+str(s3)+'.jpg',165,2,st7789.FAST)
        if choose==0:
            self.tft.text(font, 'TREBLE', 20, 63,blue,gray)
        else:
            self.tft.text(font, 'TREBLE', 20, 63,white,gray)
        if choose==1: 
            self.tft.text(font, 'BRIGHT', 97, 63,blue,gray)
        else:
            self.tft.text(font, 'BRIGHT', 97, 63,white,gray)
        if choose==2:
            self.tft.text(font, 'BASS', 182, 63,blue,gray)
        else:
            self.tft.text(font, 'BASS', 182, 63,white,gray)
        if shuffle:
            self.tft.jpg('img/shuffle.jpg',180,90)
        else:
            self.tft.jpg('img/circle.jpg',180,90)
            
    def bl_set(self,b):  #0-7 brightness
        bl_list=[61000,56000,48000,40000,30000,20000,12000,1000]
        self.bl.duty_u16(bl_list[b])
        
    def error(self,text,extra=''):
        gc.collect()
        blue=st7789.color565(31,103,179)
        self.tft.fill(blue)
        self.tft.jpg('img/bluescreen.jpg',25,10)
        ch_fb=framebuf.FrameBuffer(self.ch_buffer, 200, 24, framebuf.RGB565SW)
        ch_fb.font_load("GB2312-24.fon")
        ch_fb.font_set(0x11,0,2,0)
        ch_fb.fill(blue)
        ch_fb.text(text,0,0,0xffff)
        self.tft.blit_buffer(self.ch_buffer, 33,73,200,24)
        if extra!='':
            ch_fb.fill(blue)
            ch_fb.text(extra,0,0,0xffff)
            self.tft.blit_buffer(ch_buffer,31,102,200,24)
             
    def fb_select(self,select,song_name,y):
        bg=st7789.color565(226,225,218)
        fg=st7789.color565(88,89,89)

        if select:
            self.menu_fb.fill(fg)
            self.menu_fb.text(song_name,0,0,bg)
            self.tft.blit_buffer(self.ch_buffer, 20,y,200,24)
            #self.tft.fill_rect(0, y, 40, 24, fg)
        else:
            self.menu_fb.fill(bg)
            self.menu_fb.text(song_name,0,0,fg)
            self.tft.blit_buffer(self.ch_buffer, 20,y,200,24)
            #self.tft.fill_rect(0, y, 40, 24, bg)
            
    def show_menu(self,menu_data):
        menu_list=menu_data[0]
        cursor=menu_data[1]
        title=menu_data[2]
        print(menu_list)
        self.fb_select(False,title,5)
        self.fb_select(cursor==0,menu_list[0],30)
        self.fb_select(cursor==1,menu_list[1],55)
        self.fb_select(cursor==2,menu_list[2],80)
        self.fb_select(cursor==3,menu_list[3],105)
        
import sdcard
from machine import SPI, Pin
import os
import time
import re

class FILEMENU:
    def __init__(self):
        self.menu_num=4
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
        while len(show_list) < self.menu_num:
            show_list.append('')
        return show_list,self.cursor,self.nowcwd

    def up(self):
        if self.cursor!=0:
            self.cursor-=1
        else:
            if self.num!=0:
                self.num-=1
    
    def down(self):
        if self.cursor!=self.menu_num-1:
            self.cursor+=1
        else:
            if self.num+self.menu_num<self.nowmax:
                self.num+=1
    
    def ok(self):
        filenum=self.num+self.cursor
        now=self.nowcwd+'/'+self.nowlist[filenum]
        if os.stat(now)[0] & 0o040000 != 0:  #is folder
            self.nowcwd=now
            self.nowlist=self.nowlist=os.listdir(self.nowcwd)
            self.cursor=0
            self.num=0
            self.display()
        else:
            print('filemenu play')
            return now
        
        
    def back(self):
        if self.nowcwd=='/sd' or self.nowcwd=='sd':
            return 0
        else:
            print(self.nowcwd)
            pattern = r'(.+?)/[^/]+$'
            match = re.search(pattern, self.nowcwd)
            result = match.group(1)
            self.nowcwd=result
            print(self.nowcwd)
            self.nowlist=os.listdir(self.nowcwd)
            self.cursor=0
            self.num=0
            
        
    







        
        
        
            
    
        

    