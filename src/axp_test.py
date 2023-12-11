import lib.axp199 as axp
power=axp.PMU()
power.write_byte(0x36, 0x40)   #开机512ms 长按键1s 按键大于关机on 电源启动后pwrok信号延迟64ms 关机4s
power.write_byte(0x43, 0xc1)   #开关机irq使能
power.write_byte(0x42, 0x3b)   #开关机irq使能
print(power.getBattVoltage())