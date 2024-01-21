from __future__ import print_function
from __future__ import division
from builtins import input

import smbus

def get_voltage():

    try:
        bus = smbus.SMBus(1)        # SMBUS 1 because we're using greater than V1.
        address = 0x48
        # read data from i2c bus. the 0 command is mandatory for the protocol but not used in this chip.
        data = bus.read_word_data(address, 0)

        # from this data we need the last 4 bits and the first 6.
        last_4 = data & 0b1111 # using a bit mask
        first_6 = data >> 10 # left shift 10 because data is 16 bits

        # together they make the voltage conversion ratio
        # to make it all easier the last_4 bits are most significant :S
        vratio = (last_4 << 6) | first_6

        # Now we can calculate the battery voltage like so:
        ratio = 0.01818     # this is 0.1/5.5V Still have to find out why...
        voltage = vratio * ratio

        return "{:.3F}".format(voltage)

    except Exception as e:
        print(e)
        return False
