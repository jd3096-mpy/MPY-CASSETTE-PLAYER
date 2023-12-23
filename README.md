# MPY-CASSETTE-PLAYER

![](show.gif)

2023年最后一个项目啦，今年尝试了画PCB和3d建模，已经达到了HELLO WORLD水平，可喜可贺！

由于mpy操蛋的系统，中文不支持，要用工具转成乱码才能正常识别，都在文件夹工具脚本下面

可识别的封面需要手动添加，主打一个情怀，分辨率要求240x75，添加工具也在文件夹工具脚本下面

img下所有素材都是我用ps一点一点抠的

首发DF论坛，参加树莓派活动！

## 按键功能简介

|      | MODE     | PLAY          | N/V+     | N/V-     | POWER    |
| ---- | -------- | ------------- | -------- | -------- | -------- |
| 短按 | 暂停     | 播放          | 有声快进 | 无声快退 | 屏幕开关 |
| 中按 |          | 切换封面/歌名 | 音量加   | 音量减   | 关机     |
| 长按 | 歌曲选择 | 设置菜单      | 下一首   | 上一首   | 强制关机 |

## 引脚分布

| 引脚名称                 | GPIO |
| ------------------------ | ---- |
| xcs（VS1053）            | 20   |
| x_reset（VS1053）        | 21   |
| xdcs（VS1053）           | 26   |
| dreq（VS1053）           | 27   |
| sck（VS1053和tf卡公用）  | 18   |
| mosi（VS1053和tf卡公用） | 19   |
| miso（VS1053和tf卡公用） | 16   |
| cs（tf卡）               | 17   |
| reset（屏幕）            | 9    |
| cs（屏幕）               | 7    |
| dc（屏幕）               | 8    |
| bl（屏幕）               | 6    |
| sck（屏幕）              | 10   |
| mosi（屏幕）             | 11   |
| next（按键）             | 14   |
| prev（按键）             | 15   |
| play（按键）             | 4    |
| mode（按键）             | 5    |
| SCL（AXP199）            | 1    |
| SDA（AXP199）            | 0    |
| IRQ（AXP199）            | 2    |

## ~~硬件模块选购（为测试阶段用，现已废弃）~~

| ~~1~~ | ~~主芯片合宙RP2040~~                   | ~~9.9~~  | ~~https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=732690270351&ns=1&abbucket=6#detail~~ |
| ----- | -------------------------------------- | :------- | :----------------------------------------------------------- |
| ~~2~~ | ~~音频解码VS1053+耳机口+咪头（主板）~~ | ~~26.5~~ | ~~[https://item.taobao.com/item.htm?spm=a21n57.1.0.0.557f523cVZK7de&id=734405324623&ns=1&abbucket=6#detail](https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=614439239772&ns=1&abbucket=6#detail)~~ |
| ~~3~~ | ~~锂电充放模块 输出5v~~                | ~~4~~    | ~~[https://detail.tmall.com/item.htm?abbucket=0&id=676644707711&ns=1&spm=a21n57.1.0.0.69cf523cG91SIy&skuId=5029890950425](https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=681466242060&ns=1&abbucket=6#detail)~~ |
| ~~4~~ | ~~屏幕（模块）st7789 1.14 240x135~~    | ~~12~~   | ~~[https://item.taobao.com/item.htm?spm=a21n57.1.0.0.557f523cVZK7de&id=719186035447&ns=1&abbucket=6#detail](https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=669510720856&ns=1&abbucket=6#detail)~~ |
| ~~5~~ | ~~四按键（理想情况是设计到侧面）~~     | ~~4~~    | ~~https://detail.tmall.com/item.htm?abbucket=6&id=728912784550&ns=1&spm=a21n57.1.0.0.3ade523cSs678f&skuId=5056891289142~~ |