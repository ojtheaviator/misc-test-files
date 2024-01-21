import brickpi3
import time
import sys

#CONFIG:
power_setting = 100 #%
refresh_frequency = 2 #s
#END CONFIG:

try:

    BP = brickpi3.BrickPi3()
    BP.set_motor_power(BP.PORT_A,0)
    BP.set_motor_power(BP.PORT_B,0)

    orig_time = time.time()
    file_time = int(orig_time)
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
        
        bat_volt = BP.get_voltage_battery()
        if (bat_volt < 6.3): #dangerously low battery level: turn off
            BP.set_motor_power(BP.PORT_A, 0)
            BP.set_motor_power(BP.PORT_B, 0)
            run = False
        
        time_elapsed = time.time() - orig_time
        
        outputStr = f"{encoder_A}\t{encoder_B}\t{bat_volt}\t{time_elapsed}"
        print(outputStr)
        with open(f"motor_log_{orig_time}.csv", "a") as fid:
            fid.write(outputStr+"\n")
        
        if run:
            time.sleep(refresh_frequency)
        
except KeyboardInterrupt:
    BP.set_motor_power(BP.PORT_A, 0)
    BP.set_motor_power(BP.PORT_B, 0)
    sys.exit()
    

