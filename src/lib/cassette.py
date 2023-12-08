from machine import SPI, Pin
from vs1053 import *
import uasyncio as asyncio
from lib.screen import Screen
import _thread,framebuf
from button import Button
import machine
import gc,st7789,tft_config
import ujson,struct


class CASSETTE:
    def __init__(self):
        #screen
        self.screen=Screen()
        #button
        btn_pre=Button(15,pull=Pin.PULL_UP,trigger=Pin.IRQ_FALLING)
        btn_next=Button(14,pull=Pin.PULL_UP,trigger=Pin.IRQ_FALLING)
        btn_play=Button(5,pull=Pin.PULL_UP,trigger=Pin.IRQ_FALLING)
        btn_mode=Button(4,pull=Pin.PULL_UP,trigger=Pin.IRQ_FALLING)
        btn_list=[btn_pre,btn_next,btn_play,btn_mode]
        for btn in btn_list:
            btn.connect(self.bt_callback)
            btn.setEnable(True)
        self.btcb=0
        #vs1053 
        xcs = Pin(20, Pin.OUT, value=1)  
        reset = Pin(21, Pin.OUT, value=1)  
        xdcs = Pin(26, Pin.OUT, value=1)  
        dreq = Pin(27, Pin.IN)  
        sdcs = Pin(17, Pin.OUT, value=1)  
        spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.player = VS1053(spi, reset, dreq, xdcs, xcs, sdcs, mp='/sd')
        #self.player.patch()   #Patch if you need
        #self.player.mode_set(SM_EARSPEAKER_HI | SM_EARSPEAKER_HI)  # You decide. 
        #self.player.response(bass_freq=100, bass_amp=10)  # This is extreme.
        self.volume=4
        self.song_list=[]
        self.song_num=0
        self.effect=0
        self.bl=4
        self.bass=0
        self.load()
        self.player.volume(self.volume)
        self.screen.bl_set(self.bl)
        self.player.response(bass_freq=150, bass_amp=self.bass)
        self.cover=True
        self.search_music()
        
    async def main(self):
        asyncio.create_task(self.screen.animation())
        asyncio.create_task(self.button_control())
        self.player.play_speed(1)
        self.player.volume(self.volume) 
        while 1:
            await asyncio.sleep(1)
            print(self.player.read_mp3(), self.player.decode_time(),self.player.seek_position)
            if self.player.decode_time()!=0:
                self.player._speed=int(self.player.seek_position/self.player.decode_time()/32/20)
            if self.player._end:
                self.player._pause=False
                await self.player.cancel()
                self.player.soft_reset()
                if self.song_num==len(self.song_list)-1:
                    self.song_num=0
                else:
                    self.song_num+=1
                self.player._end=False
                asyncio.create_task(self.play(self.song_list[self.song_num]))
            
    async def button_control(self):
        while 1:
            btcb=self.btcb
            if btcb!=0:
                print(btcb)
                if btcb==1:  #REVERSE
                    self.screen.fast_reverse()
                    self.player._pause=True
                    self.player._reverse=True
                elif btcb==2:  #FORWARD
                    self.screen.fast_forward()
                    self.player.play_speed(4)
                elif btcb==3:  #PLAY
                    self.screen.play()
                    self.player.play_speed(1)
                    self.player._reverse=False
                    self.player._pause=False
                    if self.player._playing ==False:
                        self.player.soft_reset()
                        asyncio.create_task(self.play(self.song_list[self.song_num]))
                    self.player._playing=True
                elif btcb==4:  #STOP
                    if self.player._playing ==True:
                        self.screen.stop()
                        self.player._pause=True
                    self.save()
                elif btcb==22:   #NEXT SONG
                    print('next song')
                    self.player._pause=False
                    await self.player.cancel()
                    self.player.soft_reset()
                    if self.song_num==len(self.song_list)-1:
                        self.song_num=0
                    else:
                        self.song_num+=1
                    print(self.song_num,self.song_list[self.song_num])
                    asyncio.create_task(self.play(self.song_list[self.song_num]))
                elif btcb==21:   #PREV SONG
                    print('prev song')
                    self.player._pause=False
                    await self.player.cancel()
                    self.player.soft_reset()
                    if self.song_num==0:
                        self.song_num=len(self.song_list)-1
                    else:
                        self.song_num-=1
                    print(self.song_num,self.song_list[self.song_num])
                    asyncio.create_task(self.play(self.song_list[self.song_num]))
                elif btcb==11:   #VOLUME-
                    print('VOL-')
                    if self.volume<=0:
                        self.volume=0
                    else:
                        self.volume-=1
                    self.player.volume(self.volume) 
                elif btcb==12:   #VOLUME+
                    print('VOL+')
                    if self.volume>=7:
                        self.volume=7
                    else:
                        self.volume+=1
                    self.player.volume(self.volume)
                elif btcb==23:   #SETTING
                    #self.mp3_jump_to(10)
                    await self.setting()
                elif btcb==13:   #COVER/SONGNAME
                    self.show_cover(change=True)
                elif btcb==24:   #SELECT SONG
                    await self.select_song()
                self.btcb=0
            await asyncio.sleep_ms(20)
                    
        
    async def play(self,filename):
        self.player.volume(self.volume)
        self.player.response(bass_freq=150, bass_amp=self.bass)
        re=self.get_cover()
        if re==None:
            self.screen.tft.jpg('img/fantasy.jpg',0,0,st7789.SLOW)
            if len(filename)<20:
                self.screen.song_name(filename[4:-4])
            else:
                self.screen.song_name(filename[4:20])
            
        try:
            header=self.mp3_header(filename)
        except:
            header=0
        self.player.seek_position=0
        with open(filename, 'rb') as f:
            f.seek(header)
            try:
                await self.player.play(f)
            except:
                self.player.soft_reset()
    

    def bt_callback(self,pin,msg):
        #0:short press 1:long press 2:hold 3:release
        #1:pre 2:next 3:play 4:stop
        btcb=0
        if msg == 0 or msg==1 or msg==2 or msg==3: 
            if pin==15:  #button left
                btcb=1+msg*10
            elif pin==14:  #button middle
                btcb=2+msg*10
            elif pin==5:  #button right
                btcb=3+msg*10
            elif pin==4:  #button boot
                btcb=4+msg*10
        self.btcb=btcb
    
    def search_music(self):
        try:
            songs = sorted([('/sd/'+x[0]) for x in os.ilistdir('sd') if x[1] != 0x4000 ])
        except UnicodeError:
            self.screen.error('SD卡含中文',extra='尝试使用转换工具')
        except OSError:
            self.screen.error('SD未插入或损坏')
        support_file = ('mp3', 'wav')
        slist=[]
        for s in songs:
            if s[-3:] in support_file:
                slist.append(s)
        print(slist)
        self.song_list=slist
    
    def mp3_header(self,filename):
        head=''
        with open(filename, 'rb') as f:
            head=f.read(10)
            print(head[0:3])
        if head[0:3]!=b'ID3':
            size=0
        elif head[3]==1:
                size=128+10
        elif head[3]==3:
            size =  head[9] & 0x7f | ((head[8] & 0x7f) << 7) | ((head[7] & 0x7f) << 14) | ((head[6] & 0x7f) << 21)
        else:
            print('error')
            size=3096
        return size

    def mp3_jump_to(self,time):
        btl=self.player.read_mp3()[0]
        position=int(self.mp3_header(self.song_list[self.song_num])+btl*1000*time/8)
        self.player.jump_to=position
        self.player.write_decode_time(time)
    
    def save(self):
        setting_dict={'volume':self.volume,'position':self.player.seek_position,'number':self.song_num,'bl':self.bl,'bass':self.bass}
        s=ujson.dumps(setting_dict)
        print(s)
        with open('setting.txt', 'w') as f:
            f.write(s)
        print('save setting')
    
    def load(self):
        try:
            s=''
            with open('setting.txt', 'r') as f:
                s=f.read()
            print(s)
            setting_dict=ujson.loads(s)
            self.volume=setting_dict['volume']
            self.song_num=setting_dict['number']
            self.player.jump_to=setting_dict['position']
            self.player.seek_position=setting_dict['position']
            self.bl=setting_dict['bl']
            self.bass=setting_dict['bass']
        except:
            print('load error')
            
    async def setting(self):
        print('setting')
        gray=st7789.color565(40,40,44)
        choose=0
        self.btcb=0
        self.screen.tft.fill_rect(0, 0, 240,75, gray)
        self.screen.setting(choose,self.volume,self.bl,self.bass)
        i_choose=choose
        i_vol=self.volume
        i_bl=self.bl
        i_bass=self.bass
        while 1:
            if self.btcb==23:
                break
            if self.btcb==1:
                if choose==0:
                    choose=2
                else:
                    choose-=1
            if self.btcb==2:
                if choose==2:
                    choose=0
                else:
                    choose+=1
            if self.btcb==3:
                if choose==0:
                    if self.volume<7:
                        self.volume+=1
                elif choose==1:
                    if self.bl<7:
                        self.bl+=1
                elif choose==2:
                    if self.bass<7:
                        self.bass+=1
            if self.btcb==4:
                if choose==0:
                    if self.volume>0:
                        self.volume-=1
                elif choose==1:
                    if self.bl>0:
                        self.bl-=1
                elif choose==2:
                    if self.bass>0:
                        self.bass-=1
            if choose!=i_choose or self.volume!=i_vol or self.bl!=i_bl or self.bass!=i_bass:
                i_choose=choose
                i_vol=self.volume
                i_bl=self.bl
                i_bass=self.bass
                self.screen.setting(choose,self.volume,self.bl,self.bass)
                self.player.volume(self.volume)
                self.screen.bl_set(self.bl)
                self.player.response(bass_freq=150, bass_amp=self.bass)
            self.btcb=0
            await asyncio.sleep_ms(20)
        print('setting done')
        self.show_cover()
            
    def get_cover(self):  
        with open(self.song_list[self.song_num], "rb") as mp3_file:
            header = mp3_file.read(10)
            if header[:3] == b"ID3":
                tag_size = struct.unpack("!I", b"\x00" + header[6:9])[0]
                print(tag_size)
                #tag_data = mp3_file.read(tag_size)
                tag_data = mp3_file.read(1000)
                if b"APIC" in tag_data:
                    apic_index = tag_data.index(b"APIC")
                    #print(apic_index)
                    apic_data = tag_data[apic_index:]
                    #print(apic_data)
                    mime_type = apic_data[10:apic_data.index(b'\x00', 10)]
                    if mime_type==b'':
                        data_len=int.from_bytes(apic_data[4:8], 'big')
                        header_len=10+apic_index+24
                    else:
                        data_len=int.from_bytes(apic_data[4:8], 'big')
                        header_len=10+apic_index+27
                    if data_len<20000:
                        with open(self.song_list[self.song_num], "rb") as mf:
                            mf.seek(header_len)
                            image_data = mf.read(5000)
                            with open("cover.jpg", "wb") as f:
                                f.write(image_data)
                            gc.collect()
                            image_data = mf.read(data_len-5000)
                            with open("cover.jpg", "ab") as f:
                                f.write(image_data)
                            self.screen.tft.jpg('cover.jpg',0,0,st7789.SLOW)
                            return header_len,data_len
                            
                else:
                    print("NO COVER")
            else:
                print("NO ID3")
        gc.collect()
    
    def show_cover(self,change=False):
        if self.cover:
            try:
                self.screen.tft.jpg('cover.jpg',0,0,st7789.SLOW)
            except:
                print("no cover")
            if change:
                self.cover=not self.cover
        else:
            filename=self.song_list[self.song_num]
            self.screen.tft.jpg('img/fantasy.jpg',0,0,st7789.SLOW)
            if len(filename)<20:
                self.screen.song_name(filename[4:-4])
            else:
                self.screen.song_name(filename[4:20])
            if change:
                self.cover=not self.cover
            
    async def select_song(self):
        play=False
        self.screen.ani=False
        self.screen.menu_items=[item[4:] for item in self.song_list]
        bg=st7789.color565(226,225,218)
        self.screen.tft.fill(bg)
        self.screen.song_select()
        self.btcb=0
        while 1:
            if self.btcb==4:
                break
            elif self.btcb==1:
                self.screen.scroll_down()
            elif self.btcb==2:
                self.screen.scroll_up()
            elif self.btcb==3:
                print('play')
                play=True
                break    
            elif self.btcb==21:
                while self.btcb!=31:
                    self.screen.scroll_down()
                    await asyncio.sleep_ms(100)
            elif self.btcb==22:
                while self.btcb!=32:
                    self.screen.scroll_up()
                    await asyncio.sleep_ms(100)
            self.btcb=0
            await asyncio.sleep_ms(0)
        self.btcb=0
        if play:
            self.player._pause=False
            await self.player.cancel()
            self.player.soft_reset()
            self.song_num=self.screen.current_index+self.screen.select_index
            asyncio.create_task(self.play(self.song_list[self.screen.current_index+self.screen.select_index]))        
        self.show_cover()
        self.screen.ani=True
        self.screen.tft.jpg('../img/time.jpg',60,75,st7789.SLOW)
           
                    
 #print(image_data[:20])

        
        
   


