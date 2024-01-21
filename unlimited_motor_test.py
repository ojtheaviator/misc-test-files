import brickpi3
import time
import cmdgui
import smbus
import sys
import time

def get_voltage(): #Function from https://forum.dexterindustries.com/t/read-voltage-from-brickpi/985/3
    """
    Reads the digital output code of the MCP3021 chip on the BrickPi+ over i2c.
    Some bit operation magic to get a voltage floating number.
    If this doesnt work try this on the command line: i2cdetect -y 1
    The 1 in there is the bus number, same as in bus = smbus.SMBus(1)
    Google the resulting error.
    :return: voltage (float)
    """
    try:
            bus = smbus.SMBus(1)            # SMBUS 1 because we're using greater than V1.
            address = 0x48
            # time.sleep(0.1) #Is this necessary?
    
            # read data from i2c bus. the 0 command is mandatory for the protocol but not used in this chip.
            data = bus.read_word_data(address, 0)

            # from this data we need the last 4 bits and the first 6.
            last_4 = data & 0b1111 # using a bit mask
            first_6 = data >> 10 # right shift 10 because data is 16 bits

            # together they make the voltage conversion ratio
            # to make it all easier the last_4 bits are most significant :S
            vratio = (last_4 << 6) | first_6

            # Now we can calculate the battery voltage like so:
            ratio = 0.0179     # This is an emperical value based on several different batteries
            voltage = vratio * ratio

            return voltage

    except:
            return 0.0


#CONFIG:
power_setting = 100 #%
refresh_frequency = 2 #s
#END CONFIG:

try:

    BP = brickpi3.BrickPi3()
    BP.set_motor_power(BP.PORT_A,0)
    BP.set_motor_power(BP.PORT_B,0)

    orig_time = time.time()
    prevenc = 0
    run = True

    outputStr = f"Encoder A:\tEncoder B:\tBattery Voltage:\tUnix Time:\n"
    print(outputStr)
    with open(f"motor_log_{orig_time}.csv", "w") as fid:
        fid.write(outputStr)

    BP.set_motor_power(BP.PORT_A, power_setting)
    BP.set_motor_power(BP.PORT_B, power_setting)


    while run:
        encoder_A = BP.get_motor_encoder(BP.PORT_A)
        encoder_B = BP.get_motor_encoder(BP.PORT_B)
        
        bat_volt = get_voltage()
        if (bat_volt < 6.3): #dangerously low battery level: turn off
            BP.set_motor_power(BP.PORT_A, 0)
            BP.set_motor_power(BP.PORT_B, 0)
            run = False
        
        time_elapsed = time.time() - orig_time
        
        outputStr = f"{encoder_A}\t{encoder_B}\t{bat_volt}\t{time_elapsed}"
        print(outputStr)
        with open(f"motor_log_{orig_time}.csv", "a") as fid:
            fid.write(outputStr+"\n")
        
        time.sleep(refresh_frequency)
except KeyboardInterrupt:
    BP.set_motor_power(BP.PORT_A, 0)
    BP.set_motor_power(BP.PORT_B, 0)
    sys.exit()
    


