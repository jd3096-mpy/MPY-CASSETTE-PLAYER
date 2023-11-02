# MPY-CASSETTE-PLAYER

堵上中年男人私房钱的最后项目

目前仅为beta版

硬件模块选购

| 1    | 主芯片合宙RP2040                   | 9.9  | https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=732690270351&ns=1&abbucket=6#detail |
| ---- | ---------------------------------- | ---- | ------------------------------------------------------------ |
| 2    | 音频解码VS1053+耳机口+咪头（主板） | 26.5 | [https://item.taobao.com/item.htm?spm=a21n57.1.0.0.557f523cVZK7de&id=734405324623&ns=1&abbucket=6#detail](https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=614439239772&ns=1&abbucket=6#detail) |
| 3    | 锂电充放模块 输出5v                | 4    | [https://detail.tmall.com/item.htm?abbucket=0&id=676644707711&ns=1&spm=a21n57.1.0.0.69cf523cG91SIy&skuId=5029890950425](https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=681466242060&ns=1&abbucket=6#detail) |
| 4    | 屏幕（模块）st7789 1.14 240x135    | 12   | [https://item.taobao.com/item.htm?spm=a21n57.1.0.0.557f523cVZK7de&id=719186035447&ns=1&abbucket=6#detail](https://item.taobao.com/item.htm?spm=a21n57.1.0.0.3ade523cSs678f&id=669510720856&ns=1&abbucket=6#detail) |
| 5    | 四按键（理想情况是设计到侧面）     | 4    | https://detail.tmall.com/item.htm?abbucket=6&id=728912784550&ns=1&spm=a21n57.1.0.0.3ade523cSs678f&skuId=5056891289142 |

引脚分布

| 引脚名称 | GPIO |
| -------- | ---- |
| xcs      | 8    |
| x_reset  | 7    |
| xdcs     | 6    |
| dreq     | 5    |
| sck      | 10   |
| mosi     | 11   |
| miso     | 12   |
| cs       | 9    |
| reset    | 20   |
| cs       | 22   |
| dc       | 21   |
| bl       | 26   |
| sck      | 18   |
| mosi     | 19   |
| next     | 14   |
| prev     | 15   |
| play     | 17   |
| mode     | 16   |