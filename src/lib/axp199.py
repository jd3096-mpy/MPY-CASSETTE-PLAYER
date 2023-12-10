from micropython import const
# REG MAP
AXP202_STATUS = const(0x00)
AXP202_MODE_CHGSTATUS = const(0x01)
AXP202_OTG_STATUS = const(0x02)
AXP202_IC_TYPE = const(0x03)
AXP202_OFF_CTL = const(0x32)
AXP202_LDO234_DC23_CTL = const(0x12)
AXP202_VREF_TEM_CTRL = const(0xF3)
AXP202_BATT_PERCENTAGE = const(0xB9)

# AXP202 LED CONTROL
AXP20X_LED_OFF = const(0)
AXP20X_LED_BLINK_1HZ = const(1)
AXP20X_LED_BLINK_4HZ = const(2)
AXP20X_LED_LOW_LEVEL = const(3)

# axp 20 adc data register
AXP202_BAT_AVERVOL_H8 = const(0x78)
AXP202_BAT_AVERVOL_L4 = const(0x79)
AXP202_BAT_AVERCHGCUR_H8 = const(0x7A)
AXP202_BAT_AVERCHGCUR_L4 = const(0x7B)
AXP202_BAT_VOL_H8 = const(0x50)
AXP202_BAT_VOL_L4 = const(0x51)

# Signal Capture
AXP202_BATT_VOLTAGE_STEP = const(1.1)
AXP202_BATT_DISCHARGE_CUR_STEP = const(0.5)
AXP202_BATT_CHARGE_CUR_STEP = const(0.5)

AXP202_BAT_POWERH8 = const(0x70)
AXP202_BAT_POWERM8 = const(0x71)
AXP202_BAT_POWERL8 = const(0x72)
AXP202_BAT_AVERDISCHGCUR_H8 = const(0x7C)
AXP202_BAT_AVERDISCHGCUR_L5 = const(0x7D)


import gc
from machine import Pin, SoftI2C
import micropython
from ustruct import unpack

default_pin_scl = 1
default_pin_sda = 0
default_pin_intr = 2
default_chip_type = 3


class PMU(object):
    def __init__(self, scl=None, sda=None,
                 intr=None, address=None):
        self.device = None
        self.scl = scl if scl is not None else default_pin_scl
        self.sda = sda if sda is not None else default_pin_sda
        self.intr = intr if intr is not None else default_pin_intr
        self.chip = default_chip_type
        self.address = address if address else 0x34

        self.buffer = bytearray(16)
        self.bytebuf = memoryview(self.buffer[0:1])
        self.wordbuf = memoryview(self.buffer[0:2])
        self.irqbuf = memoryview(self.buffer[0:5])

        self.init_pins()
        self.init_i2c()
        self.chip = 3

    def init_i2c(self):
        print('* initializing i2c')
        self.bus = SoftI2C(scl=self.pin_scl,sda=self.pin_sda)

    def init_pins(self):
        print('* initializing pins')
        self.pin_sda = Pin(self.sda)
        self.pin_scl = Pin(self.scl)
        self.pin_intr = Pin(self.intr, mode=Pin.IN)

    def write_byte(self, reg, val):
        self.bytebuf[0] = val
        self.bus.writeto_mem(self.address, reg, self.bytebuf)

    def read_byte(self, reg):
        self.bus.readfrom_mem_into(self.address, reg, self.bytebuf)
        return self.bytebuf[0]

    def read_word(self, reg):
        self.bus.readfrom_mem_into(self.address, reg, self.wordbuf)
        return unpack('>H', self.wordbuf)[0]

    def read_word2(self, reg):
        self.bus.readfrom_mem_into(self.address, reg, self.wordbuf)
        return unpack('>h', self.wordbuf)[0]

    def enablePower(self, ch):
        data = self.read_byte(AXP202_LDO234_DC23_CTL)
        data = data | (1 << ch)
        self.write_byte(AXP202_LDO234_DC23_CTL, data)

    def disablePower(self, ch):
        data = self.read_byte(AXP202_LDO234_DC23_CTL)
        data = data & (~(1 << ch))
        self.write_byte(AXP202_LDO234_DC23_CTL, data)

    def __BIT_MASK(self, mask):
        return 1 << mask

    def __get_h8_l5(self, regh8, regl5):
        hv = self.read_byte(regh8)
        lv = self.read_byte(regl5)
        return (hv << 5) | (lv & 0x1F)

    def __get_h8_l4(self, regh8, regl5):
        hv = self.read_byte(regh8)
        lv = self.read_byte(regl5)
        return (hv << 4) | (lv & 0xF)

    def isCharging(self):
        data = self.read_byte(AXP202_MODE_CHGSTATUS)
        return data & self.__BIT_MASK(6)
    
    def isBatteryConnect(self):
        data = self.read_byte(AXP202_MODE_CHGSTATUS)
        return data & self.__BIT_MASK(5)

    def getAcinCurrent(self):
        data = self.__get_h8_l4(AXP202_ACIN_CUR_H8, AXP202_ACIN_CUR_L4)
        return data * AXP202_ACIN_CUR_STEP

    def getAcinVoltage(self):
        data = self.__get_h8_l4(AXP202_ACIN_VOL_H8, AXP202_ACIN_VOL_L4)
        return data * AXP202_ACIN_VOLTAGE_STEP

    def getVbusVoltage(self):
        data = self.__get_h8_l4(AXP202_VBUS_VOL_H8, AXP202_VBUS_VOL_L4)
        return data * AXP202_VBUS_VOLTAGE_STEP

    def getVbusCurrent(self):
        data = self.__get_h8_l4(AXP202_VBUS_CUR_H8, AXP202_VBUS_CUR_L4)
        return data * AXP202_VBUS_CUR_STEP

    def getTemp(self):
        hv = self.read_byte(AXP202_INTERNAL_TEMP_H8)
        lv = self.read_byte(AXP202_INTERNAL_TEMP_L4)
        data = (hv << 8) | (lv & 0xF)
        return data / 1000

    def getTSTemp(self):
        data = self.__get_h8_l4(AXP202_TS_IN_H8, AXP202_TS_IN_L4)
        return data * AXP202_TS_PIN_OUT_STEP

    def getGPIO0Voltage(self):
        data = self.__get_h8_l4(AXP202_GPIO0_VOL_ADC_H8,
                                AXP202_GPIO0_VOL_ADC_L4)
        return data * AXP202_GPIO0_STEP

    def getGPIO1Voltage(self):
        data = self.__get_h8_l4(AXP202_GPIO1_VOL_ADC_H8,
                                AXP202_GPIO1_VOL_ADC_L4)
        return data * AXP202_GPIO1_STEP

    def getBattInpower(self):
        h8 = self.read_byte(AXP202_BAT_POWERH8)
        m8 = self.read_byte(AXP202_BAT_POWERM8)
        l8 = self.read_byte(AXP202_BAT_POWERL8)
        data = (h8 << 16) | (m8 << 8) | l8
        return 2 * data * 1.1 * 0.5 / 1000

    def getBattVoltage(self):
        data = self.__get_h8_l4(AXP202_BAT_AVERVOL_H8, AXP202_BAT_AVERVOL_L4)
        return data

    def getBattChargeCurrent(self):
        data = 0
        data = self.__get_h8_l5(
            AXP202_BAT_AVERCHGCUR_H8, AXP202_BAT_AVERCHGCUR_L4) * AXP202_BATT_CHARGE_CUR_STEP
        return data

    def getBattDischargeCurrent(self):
        data = self.__get_h8_l4(
            AXP202_BAT_AVERDISCHGCUR_H8, AXP202_BAT_AVERDISCHGCUR_L5) * AXP202_BATT_DISCHARGE_CUR_STEP
        return data

    def getSysIPSOUTVoltage(self):
        hv = self.read_byte(AXP202_APS_AVERVOL_H8)
        lv = self.read_byte(AXP202_APS_AVERVOL_L4)
        data = (hv << 4) | (lv & 0xF)
        return data

    def enableADC(self, ch, val):
        if(ch == 1):
            data = self.read_byte(AXP202_ADC_EN1)
            data = data | (1 << val)
            self.write_byte(AXP202_ADC_EN1, data)
        elif(ch == 2):
            data = self.read_byte(AXP202_ADC_EN2)
            data = data | (1 << val)
            self.write_byte(AXP202_ADC_EN1, data)
        else:
            return

    def disableADC(self, ch, val):
        if(ch == 1):
            data = self.read_byte(AXP202_ADC_EN1)
            data = data & (~(1 << val))
            self.write_byte(AXP202_ADC_EN1, data)
        elif(ch == 2):
            data = self.read_byte(AXP202_ADC_EN2)
            data = data & (~(1 << val))
            self.write_byte(AXP202_ADC_EN1, data)
        else:
            return

    def enableIRQ(self, val):
        if(val & 0xFF):
            data = self.read_byte(AXP202_INTEN1)
            data = data | (val & 0xFF)
            self.write_byte(AXP202_INTEN1, data)

        if(val & 0xFF00):
            data = self.read_byte(AXP202_INTEN2)
            data = data | (val >> 8)
            self.write_byte(AXP202_INTEN2, data)

        if(val & 0xFF0000):
            data = self.read_byte(AXP202_INTEN3)
            data = data | (val >> 16)
            self.write_byte(AXP202_INTEN3, data)

        if(val & 0xFF000000):
            data = self.read_byte(AXP202_INTEN4)
            data = data | (val >> 24)
            self.write_byte(AXP202_INTEN4, data)

    def disableIRQ(self, val):
        if(val & 0xFF):
            data = self.read_byte(AXP202_INTEN1)
            data = data & (~(val & 0xFF))
            self.write_byte(AXP202_INTEN1, data)

        if(val & 0xFF00):
            data = self.read_byte(AXP202_INTEN2)
            data = data & (~(val >> 8))
            self.write_byte(AXP202_INTEN2, data)

        if(val & 0xFF0000):
            data = self.read_byte(AXP202_INTEN3)
            data = data & (~(val >> 16))
            self.write_byte(AXP202_INTEN3, data)

        if(val & 0xFF000000):
            data = self.read_byte(AXP202_INTEN4)
            data = data & (~(val >> 24))
            self.write_byte(AXP202_INTEN4, data)
        pass

    def readIRQ(self):
        if(self.chip == AXP202_CHIP_ID):
            for i in range(5):
                self.irqbuf[i] = self.read_byte(AXP202_INTSTS1 + i)
        elif(self.chip == AXP192_CHIP_ID):
            for i in range(4):
                self.irqbuf[i] = self.read_byte(AXP192_INTSTS1 + i)

            self.irqbuf[4] = self.read_byte(AXP192_INTSTS5)

    def clearIRQ(self):
        if(self.chip == AXP202_CHIP_ID):
            for i in range(5):
                self.write_byte(AXP202_INTSTS1 + i, 0xFF)
                self.irqbuf[i] = 0
        elif(self.chip == AXP192_CHIP_ID):
            for i in range(4):
                self.write_byte(AXP192_INTSTS1 + i, 0xFF)
            self.write_byte(AXP192_INTSTS5, 0xFF)

    def isVBUSPlug(self):
        data = self.read_byte(AXP202_STATUS)
        return data & self.__BIT_MASK(5)

    # Only can set axp192
    def setDC1Voltage(self, mv):
        if(self.chip != AXP192_CHIP_ID):
            return
        if(mv < 700):
            mv = 700
        elif(mv > 3500):
            mv = 3500
        val = (mv - 700) / 25
        self.write_byte(AXP192_DC1_VLOTAGE, int(val))

    def setDC2Voltage(self, mv):
        if(mv < 700):
            mv = 700
        elif(mv > 2275):
            mv = 2275
        val = (mv - 700) / 25
        self.write_byte(AXP202_DC2OUT_VOL, int(val))

    def setDC3Voltage(self, mv):
        if(mv < 700):
            mv = 700
        elif(mv > 3500):
            mv = 3500
        val = (mv - 700) / 25
        self.write_byte(AXP202_DC3OUT_VOL, int(val))

    def setLDO2Voltage(self, mv):
        if(mv < 1800):
            mv = 1800
        elif(mv > 3300):
            mv = 3300
        val = (mv - 1800) / 100
        prev = self.read_byte(AXP202_LDO24OUT_VOL)
        prev &= 0x0F
        prev = prev | (int(val) << 4)
        self.write_byte(AXP202_LDO24OUT_VOL, int(prev))

    def setLDO3Voltage(self, mv):
        if self.chip == AXP202_CHIP_ID and mv < 700:
            mv = 700
        elif self.chip == AXP192_CHIP_ID and mv < 1800:
            mv = 1800

        if self.chip == AXP202_CHIP_ID and mv > 3500:
            mv = 3500
        elif self.chip == AXP192_CHIP_ID and mv > 3300:
            mv = 3300

        if self.chip == AXP202_CHIP_ID:
            val = (mv - 700) / 25
            prev = self.read_byte(AXP202_LDO3OUT_VOL)
            prev &= 0x80
            prev = prev | int(val)
            self.write_byte(AXP202_LDO3OUT_VOL, int(prev))
            # self.write_byte(AXP202_LDO3OUT_VOL, int(val))
        elif self.chip == AXP192_CHIP_ID:
            val = (mv - 1800) / 100
            prev = self.read_byte(AXP192_LDO23OUT_VOL)
            prev &= 0xF0
            prev = prev | int(val)
            self.write_byte(AXP192_LDO23OUT_VOL, int(prev))

    def setLDO4Voltage(self, arg):
        if self.chip == AXP202_CHIP_ID and arg <= AXP202_LDO4_3300MV:
            data = self.read_byte(AXP202_LDO24OUT_VOL)
            data = data & 0xF0
            data = data | arg
            self.write_byte(AXP202_LDO24OUT_VOL, data)

    def setLDO3Mode(self, mode):
        if(mode > AXP202_LDO3_DCIN_MODE):
            return
        data = self.read_byte(AXP202_LDO3OUT_VOL)
        if(mode):
            data = data | self.__BIT_MASK(7)
        else:
            data = data & (~self.__BIT_MASK(7))
        self.write_byte(AXP202_LDO3OUT_VOL, data)

    def shutdown(self):
        data = self.read_byte(AXP202_OFF_CTL)
        data = data | self.__BIT_MASK(7)
        self.write_byte(AXP202_OFF_CTL, data)

    def getSettingChargeCurrent(self):
        data = self.read_byte(AXP202_CHARGE1)
        data = data & 0b00000111
        curr = 300 + data * 100
        return curr

    def isChargeingEnable(self):
        data = self.read_byte(AXP202_CHARGE1)
        if(data & self.__BIT_MASK(7)):
            return True
        return False

    def enableChargeing(self):
        data = self.read_byte(AXP202_CHARGE1)
        data = data | self.__BIT_MASK(7)
        self.write_byte(AXP202_CHARGE1, data)

    def setChargingTargetVoltage(self, val):
        targetVolParams = (
            0b00000000,
            0b00100000,
            0b01000000,
            0b01100000)
        if(val > AXP202_TARGET_VOL_4_36V):
            return
        data = self.read_byte(AXP202_CHARGE1)
        data = data & (~targetVolParams[3])
        data = data | targetVolParams[val]
        self.write_byte(AXP202_CHARGE1, data)

    def getBattPercentage(self):
        data = self.read_byte(AXP202_BATT_PERCENTAGE)
        mask = data & self.__BIT_MASK(7)
        if(mask):
            return 0
        return data & (~self.__BIT_MASK(7))

    def setChgLEDChgControl(self):
        data = self.read_byte(AXP202_OFF_CTL)
        data = data & 0b111110111
        self.write_byte(AXP202_OFF_CTL, data)

    def setChgLEDMode(self, mode):
        data = self.read_byte(AXP202_OFF_CTL)
        data |= self.__BIT_MASK(3)
        if(mode == AXP20X_LED_OFF):
            data = data & 0b11001111
        elif(mode == AXP20X_LED_BLINK_1HZ):
            data = data & 0b11001111
            data = data | 0b00010000
        elif(mode == AXP20X_LED_BLINK_4HZ):
            data = data & 0b11001111
            data = data | 0b00100000
        elif(mode == AXP20X_LED_LOW_LEVEL):
            data = data & 0b11001111
            data = data | 0b00110000
        self.write_byte(AXP202_OFF_CTL, data)
    
    