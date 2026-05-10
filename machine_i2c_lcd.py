import time
from lcd_api import LcdApi

class I2cLcd(LcdApi):
    MASK_RS = 0x01
    MASK_RW = 0x02
    MASK_E = 0x04
    SHIFT_BACKLIGHT = 3
    SHIFT_DATA = 4

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = 1
        self.i2c.writeto(self.i2c_addr, bytes([0]))
        time.sleep_ms(20)
        self.hal_write_init_nibble(self.LCD_FUNCTION_8BIT)
        time.sleep_ms(5)
        self.hal_write_init_nibble(self.LCD_FUNCTION_8BIT)
        time.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_8BIT)
        time.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep_ms(1)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) & 0x0f) << self.SHIFT_DATA
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))

    def hal_backlight_on(self):
        self.backlight = 1
        self.i2c.writeto(self.i2c_addr, bytes([1 << self.SHIFT_BACKLIGHT]))

    def hal_backlight_off(self):
        self.backlight = 0
        self.i2c.writeto(self.i2c_addr, bytes([0]))

    def hal_write_command(self, cmd):
        byte = ((self.backlight << self.SHIFT_BACKLIGHT) | (((cmd >> 4) & 0x0f) << self.SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        byte = ((self.backlight << self.SHIFT_BACKLIGHT) | ((cmd & 0x0f) << self.SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        if cmd <= 3:
            time.sleep_ms(5)

    def hal_write_data(self, data):
        byte = (self.MASK_RS | (self.backlight << self.SHIFT_BACKLIGHT) | (((data >> 4) & 0x0f) << self.SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        byte = (self.MASK_RS | (self.backlight << self.SHIFT_BACKLIGHT) | ((data & 0x0f) << self.SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))