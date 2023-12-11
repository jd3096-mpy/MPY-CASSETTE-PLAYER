import st7789,tft_config
import framebuf,time
import uasyncio as asyncio
import gc
import vga8x8 as font
from machine import Pin,PWM
#import dance as ff

class Screen:
    
    def __init__(self):
        self.tft=tft_config.config(1)
        self.tft.init()
        self.tft.fill(0)
        self.tft.jpg('img/logo1.jpg',65,10,st7789.SLOW)
        self.tft.jpg('img/logo2.jpg',20,80,st7789.SLOW)
        time.sleep(1)
        self.fblist=[]
        #load tape rotation animation
        print(gc.mem_free())
        for i in range(1,16):
            fb=self.tft.jpg_decode('img/'+str(i)+'.jpg')
            fbuf = framebuf.FrameBuffer((fb[0]), 60, 60, framebuf.RGB565)
            self.fblist.append(fbuf)
            del fbuf
        gc.collect()
        print(gc.mem_free())
        self.ani=False
        self.ani_num=1
        self.ani_max=15
        self.reverse=False
        self.speed=20
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
        
        self.tft.jpg('img/fantasy.jpg',0,0,st7789.SLOW)
        self.tft.jpg('../img/time.jpg',60,75,st7789.SLOW)
        self.tft.blit_buffer(self.fblist[0], 0, 74, 60, 60)
        self.tft.blit_buffer(self.fblist[0], 180, 74, 60, 60)
        
        self.current_index=0
        self.items_per_page=5
        self.select_index=0
        self.menu_items=[]
        
    async def animation(self):
        while 1:
            if self.ani:
                if self.reverse:
                    if self.ani_num==1:
                        self.ani_num=self.ani_max
                    else:
                        self.ani_num-=1
                else:
                    if self.ani_num==self.ani_max:
                        self.ani_num=1
                    else:
                        self.ani_num+=1
                self.tft.blit_buffer(self.fblist[self.ani_num-1], 0, 75, 60, 60)
                self.tft.blit_buffer(self.fblist[self.ani_num-1], 180, 75, 60, 60)
                await asyncio.sleep_ms(self.speed)
            else:
                await asyncio.sleep_ms(10)
        
    def play(self):
        self.ani=True
        self.speed=20
        self.reverse=False
    def song_name(self,name):
        self.ch_fb.fill(0xffff)
        self.ch_fb.text(name,0,0,0x0)
        self.tft.blit_buffer(self.ch_buffer, 30, 36, 200,24)
#         self.tft.fill_rect(15, 31, 215, 32, st7789.WHITE)
#         self.tft.write(ff, name, 15, 31,st7789.BLACK,st7789.WHITE)
                
    def stop(self):
        self.ani=False
        self.reverse=False
        
    def fast_forward(self):
        self.ani=True
        self.speed=5
        self.reverse=False
        
    def fast_reverse(self):
        self.ani=True
        self.speed=5
        self.reverse=True
        
    def setting(self,choose,s1,s2,s3):
        gray=st7789.color565(40,40,44)
        blue=st7789.color565(184,212,254)
        white=st7789.color565(222,222,222)
        self.tft.jpg('img/spin'+str(s1)+'.jpg',15,2,st7789.FAST)
        self.tft.jpg('img/spin'+str(s2)+'.jpg',90,2,st7789.FAST)
        self.tft.jpg('img/spin'+str(s3)+'.jpg',165,2,st7789.FAST)
        if choose==0:
            self.tft.text(font, 'VOLUME', 20, 63,blue,gray)
        else:
            self.tft.text(font, 'VOLUME', 20, 63,white,gray)
        if choose==1: 
            self.tft.text(font, 'BRIGHT', 97, 63,blue,gray)
        else:
            self.tft.text(font, 'BRIGHT', 97, 63,white,gray)
        if choose==2:
            self.tft.text(font, 'BASS', 182, 63,blue,gray)
        else:
            self.tft.text(font, 'BASS', 182, 63,white,gray)
            
    def bl_set(self,b):  #0-7 brightness
        #bl_list=[4000,12000,20000,30000,40000,48000,56000,65534]
        bl_list=[65534,56000,48000,40000,30000,20000,12000,4000]
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
        ch_fb=framebuf.FrameBuffer(self.ch_buffer, 200, 24, framebuf.RGB565SW)
        ch_fb.font_load("GB2312-24.fon")
        ch_fb.font_set(0x13,0,1,0)
        if select:
            ch_fb.fill(fg)
            ch_fb.text(song_name,0,0,bg)
            self.tft.blit_buffer(self.ch_buffer, 40,y,200,24)
            self.tft.fill_rect(0, y, 40, 24, fg)
        else:
            ch_fb.fill(bg)
            ch_fb.text(song_name,0,0,fg)
            self.tft.blit_buffer(self.ch_buffer, 40,y,200,24)
            self.tft.fill_rect(0, y, 40, 24, bg)
            
    def song_select(self):
        bg=st7789.color565(226,225,218)
        fg=st7789.color565(88,89,89)
        menu_list=[]
        for i in range(self.current_index, min(self.current_index + self.items_per_page, len(self.menu_items))):
            if i == self.current_index:
                menu_list.append(self.menu_items[i])
            else:
                menu_list.append(self.menu_items[i])
        self.fb_select(self.select_index==0,menu_list[0],5)
        self.fb_select(self.select_index==1,menu_list[1],30)
        self.fb_select(self.select_index==2,menu_list[2],55)
        self.fb_select(self.select_index==3,menu_list[3],80)
        self.fb_select(self.select_index==4,menu_list[4],105)

    def scroll_up(self):
        if self.select_index!=0:
            self.select_index-=1
        else:
            if self.current_index > 0:
                self.current_index -= 1
                if self.current_index < self.current_index % self.items_per_page:
                    self.current_index = self.current_index % self.items_per_page
        self.song_select()

    def scroll_down(self):
        #print(self.current_index+self.select_index ,(len(self.menu_items) - 1))
        if self.select_index!=self.items_per_page-1:
            self.select_index+=1
        else:
            if self.current_index+self.select_index < len(self.menu_items) - 1:
                if self.current_index % self.items_per_page == self.items_per_page - 1:
                    self.current_index += 1
                else:
                    self.current_index = min(self.current_index + 1, len(self.menu_items) - 1)
        self.song_select()



        
        
        
            
    
        

    