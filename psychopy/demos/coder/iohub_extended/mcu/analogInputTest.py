 # -*- coding: utf-8 -*-
"""
Simple example of how to enable ioSync analog input reading. The demo starts
the iosync with analog input events enabled. Analog input events are printed
to the console and saved to the ioHub Data Store file.

ioSync supports 8 single ended analog inputs. All channels are sampled at 
1000 Hz (each channel is read sequentially, with a read time of about 20 usec 
each with curent internal ioSync settings). Analog inputs are 16 bit at a HW 
level, but realistically only expect ~ 12 bit effective resolution. 
More testing is needed to really quantify this.  

Data is currently output in raw form for each channel, with a value range 
of 0 (0.0 V) to 2**16 (3.3 V).

IMPORTANT: Input voltage to an analog input pin must be between 0.0 V and 3.3 V 
or you may damage the Teensy 3. 

Connect analog input lines to ioSync inputs AI_0 to AI_7; connect grounds to the
AGND pin.

Analog input channels which are not connected to anything 'float'. If you want
unused channels to be fixed at ground, connect each unused channel to the GND
pin.
"""

import numpy as np    
import time
from psychopy import core
from psychopy.iohub import launchHubServer,Computer
getTime=core.getTime

io=None
mcu=None

try:
    psychopy_mon_name='testMonitor'
    exp_code='events'
    sess_code='S_{0}'.format(long(time.mktime(time.localtime())))
    
    iohub_config={
    "psychopy_monitor_name":psychopy_mon_name,
    "mcu.iosync.MCU":dict(serial_port='COM8',monitor_event_types=['AnalogInputEvent',]),#['DigitalInputEvent']),
    "experiment_code":exp_code, 
    "session_code":sess_code
    }
    
    io=launchHubServer(**iohub_config)
    
    display=io.devices.display
    mcu=io.devices.mcu
    kb=io.devices.keyboard
    experiment=io.devices.experiment
        
    mcu.enableEventReporting(True)
    
    io.clearEvents("all")   
    i=0
    while not kb.getEvents():   
        mcu_events=  mcu.getEvents()  
        for mcu_evt in mcu_events:
            print'{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}'.format(mcu_evt.time,
                                                                 mcu_evt.device_time,
                                                                 mcu_evt.AI_0,
                                                                 mcu_evt.AI_1,
                                                                 mcu_evt.AI_2,
                                                                 mcu_evt.AI_3,
                                                                 mcu_evt.AI_4,
                                                                 mcu_evt.AI_5,
                                                                 mcu_evt.AI_6,
                                                                 mcu_evt.AI_7,
                                                                 )
            
    io.clearEvents('all')
except:
    import traceback
    traceback.print_exc()    
finally:
    if mcu:    
        mcu.enableEventReporting(False)   
    if io:
        io.quit() 
