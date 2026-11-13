import RPi.GPIO as GPIO
from time import sleep
import encoding


class LCD:

    # Instructions
    _CLEARDISPLAY = 0b000_00001
    _RETURNHOME = 0b0000_0010
    _ENTRYMODE = 0b0000_0100
    _DISPLAYSETTING = 0b0000_1000
    _CURSORSHIFT = 0b0001_0000
    _FUNCTIONSET = 0b0010_0000
    _SETCGRAM = 0b0100_0000
    _SETDDRAM = 0b1000_0000

    # Entry Mode Set
    _MOVERIGHT = 0b10
    _MOVELEFT = 0b00
    _SHIFTDISPLAYON = 0b01
    _SHIFTDISPLAYOFF = 0b00

    # Display Settings
    _DISPLAYON = 0b100
    _DISPLAYOFF = 0b000
    _CURSORON = 0b010
    _CURSOROFF = 0b000
    _CURSORBLINKON = 0b001
    _CURSORBLINKOFF = 0b000

    # Cursor Shift
    _CURSORSHIFTLEFT = 0b0000
    _CURSORSHIFTRIGHT = 0b0100
    _DISPLAYSHIFTLEFT = 0b1000
    _DISPLAYSHIFTRIGHT = 0b1100

    # Function Set
    _8BITMODE = 0b10000
    _4BITMODE = 0b00000
    _1LINE = 0b00000
    _2LINE = 0b01000
    _5x8 = 0b00000
    _5x11 = 0b00100


    def __init__(self, rs_pin, e_pin, data_pins):
        # PIN Mode auf BCM
        GPIO.setmode(GPIO.BCM)

        self.rs_pin = rs_pin
        self.e_pin = e_pin
        self.data_pins = data_pins
        if len(data_pins) == 4: self.mode = self._4BITMODE
        if len(data_pins) == 8: self.mode = self._8BITMODE

        # PIN Outputs/Inputs
        GPIO.setup(self.rs_pin, GPIO.OUT, initial=0)
        GPIO.setup(self.e_pin, GPIO.OUT, initial=0)
        GPIO.setup(self.data_pins, GPIO.OUT, initial=0)

        # Initialization
        self.sleepMicro(50000)

        # FUNCTION SET
        _funcset = self._FUNCTIONSET + self.mode + self._2LINE + self._5x8
        self.function_set(_funcset)

        # DISPLAY CONTROL
        _displayset = self._DISPLAYSETTING + self._DISPLAYON + self._CURSOROFF + self._CURSORBLINKOFF
        self.instruction(_displayset)

        # CLEAR and HOME
        self.clear()
        #self.instruction(self._RETURNHOME)
        self.sleepMicro(2000)

        # ENTRY MODE
        _entrymode = self._ENTRYMODE + self._MOVERIGHT + self._SHIFTDISPLAYOFF
        self.instruction(_entrymode)



    def function_set(self, *args):
        GPIO.output(self.rs_pin, 0)
        self.write4bit(self._FUNCTIONSET + self._8BITMODE)
        self.sleepMicro(4500)
        self.instruction(sum(args))
        self.sleepMicro(150)
        self.instruction(sum(args))

    def clear(self):
        self.instruction(self._CLEARDISPLAY)

    def home(self):
        self.instruction(self._RETURNHOME)

    def shift_display(self):
        self.instruction(self._CURSORSHIFT + self._DISPLAYSHIFTLEFT)



    def create_char(self, tupel, address):
        self.set_cgram(address)
        for col in tupel:
            self.data(col)

    def write_string(self, string):
        for char in string:
            self.write_char(char)

    def write_char(self, char):
        self.data(encoding.character[char])

    def set_cgram(self, address):
        self.instruction(self._SETCGRAM + (address << 3))

    def set_ddram(self, address):
        self.instruction(self._SETDDRAM + address)



    def instruction(self, value):
        GPIO.output(self.rs_pin, 0)
        self.write(value)

    def data(self, value):
        GPIO.output(self.rs_pin, 1)
        self.write(value)


    def write(self, value):
        if self.mode == self._8BITMODE:
            self.write8bit(value)
        if self.mode == self._4BITMODE:
            self.write4bit(value >> 4)
            self.write4bit(value)

    def write4bit(self, value):
        for i in range(4):
            pin_mode = (value >> i) & 1
            GPIO.output(self.data_pins[i], pin_mode)
        self.pulse()

    def write8bit(self, value):
        for i in range(8):
            pin_mode = (value >> i) & 1
            GPIO.output(self.data_pins[i], pin_mode)
        self.pulse()

    def pulse(self):
        GPIO.output(self.e_pin, 0)
        self.sleepMicro(1)
        GPIO.output(self.e_pin, 1)
        self.sleepMicro(1)
        GPIO.output(self.e_pin, 100)



    def sleepMicro(self, time):
        sleep(time / 1000000.0)
