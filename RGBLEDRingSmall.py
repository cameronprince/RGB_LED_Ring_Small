from machine import I2C, Pin

ISSI3746_PAGE0 = 0x00
ISSI3746_PAGE1 = 0x01

ISSI3746_COMMANDREGISTER = 0xFD
ISSI3746_COMMANDREGISTER_LOCK = 0xFE
ISSI3746_ID_REGISTER = 0xFC
ISSI3746_ULOCK_CODE = 0xC5

ISSI3746_CONFIGURATION = 0x50
ISSI3746_GLOBALCURRENT = 0x51
ISSI3746_PULLUPDOWM = 0x52
ISSI3746_OPENSHORT = 0x53
ISSI3746_TEMPERATURE = 0x5F
ISSI3746_SPREADSPECTRUM = 0x60
ISSI3746_RESET_REG = 0x8F
ISSI3746_PWM_FREQUENCY_ENABLE = 0xE0
ISSI3746_PWM_FREQUENCY_SET = 0xE2

class RGBLEDRingSmall:
    def __init__(self, i2c, address):
        self.i2c = i2c
        self.address = address
        self.issi_led_map = [
            [0x48, 0x36, 0x24, 0x12, 0x45, 0x33, 0x21, 0x0F, 0x42, 0x30, 0x1E, 0x0C, 0x3F, 0x2D, 0x1B, 0x09, 0x3C, 0x2A, 0x18, 0x06, 0x39, 0x27, 0x15, 0x03],
            [0x47, 0x35, 0x23, 0x11, 0x44, 0x32, 0x20, 0x0E, 0x41, 0x2F, 0x1D, 0x0B, 0x3E, 0x2C, 0x1A, 0x08, 0x3B, 0x29, 0x17, 0x05, 0x38, 0x26, 0x14, 0x02],
            [0x46, 0x34, 0x22, 0x10, 0x43, 0x31, 0x1F, 0x0D, 0x40, 0x2E, 0x1C, 0x0A, 0x3D, 0x2B, 0x19, 0x07, 0x3A, 0x28, 0x16, 0x04, 0x37, 0x25, 0x13, 0x01]
        ]

    def select_bank(self, bank):
        self.write_register8(ISSI3746_COMMANDREGISTER_LOCK, ISSI3746_ULOCK_CODE)
        self.write_register8(ISSI3746_COMMANDREGISTER, bank)

    def write_register8(self, reg, data):
        self.i2c.writeto_mem(self.address, reg, bytearray([data]))

    def read_register8(self, reg):
        return self.i2c.readfrom_mem(self.address, reg, 1)[0]

    def pwm_mode(self):
        self.select_bank(ISSI3746_PAGE0)

    def configuration(self, conf):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(ISSI3746_CONFIGURATION, conf)

    def set_scaling(self, led_n, scal):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(led_n, scal)

    def set_scaling_all(self, scal):
        self.select_bank(ISSI3746_PAGE1)
        for i in range(1, 73):
            self.write_register8(i, scal)

    def global_current(self, curr):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(ISSI3746_GLOBALCURRENT, curr)

    def pullup_down(self, pull):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(ISSI3746_PULLUPDOWM, pull)

    def temperature(self):
        self.select_bank(ISSI3746_PAGE1)
        return self.read_register8(ISSI3746_TEMPERATURE)

    def spread_spectrum(self, spread):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(ISSI3746_SPREADSPECTRUM, spread)

    def reset(self):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(ISSI3746_RESET_REG, 0xAE)

    def pwm_frequency_enable(self, enable):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(ISSI3746_PWM_FREQUENCY_ENABLE, enable)

    def pwm_frequency_setting(self, freq):
        self.select_bank(ISSI3746_PAGE1)
        self.write_register8(ISSI3746_PWM_FREQUENCY_SET, freq)

    def set_rgb(self, led_n, color):
        if led_n < len(self.issi_led_map[0]):
            self.write_register8(self.issi_led_map[0][led_n], (color >> 16) & 0xFF)
            self.write_register8(self.issi_led_map[1][led_n], (color >> 8) & 0xFF)
            self.write_register8(self.issi_led_map[2][led_n], color & 0xFF)

    def set_red(self, led_n, color):
        if led_n < len(self.issi_led_map[0]):
            self.write_register8(self.issi_led_map[0][led_n], color)

    def set_green(self, led_n, color):
        if led_n < len(self.issi_led_map[1]):
            self.write_register8(self.issi_led_map[1][led_n], color)

    def set_blue(self, led_n, color):
        if led_n < len(self.issi_led_map[2]):
            self.write_register8(self.issi_led_map[2][led_n], color)

    def clear_all(self):
        self.pwm_mode()
        for i in range(1, 73):
            self.write_register8(i, 0)
