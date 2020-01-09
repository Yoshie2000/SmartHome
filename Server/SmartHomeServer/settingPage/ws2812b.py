import time
from RF24 import *
import RPi.GPIO as GPIO

# RPi Alternate, with SPIDEV - Note: Edit RF24/arch/BBB/spi.cpp and  set 'this->device = "/dev/spidev0.0";;' or as listed in /dev
radio = RF24(22, 0)
 
payload_size = 16
millis = lambda: int(round(time.time() * 1000))
 
radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5,15)

pipes = [0xF0E1, 0xF0D2]

time.sleep(1)
 
radio.openWritingPipe(pipes[0]) # Address of the Arduino
radio.openReadingPipe(1,pipes[1]) # Address of the Raspberry

def send_profile(profile):

    for code in profile.setting_codes().split(";"):
            
        while send_code(code) == False:
            if radio.failureDetected:
                radio.begin()
                radio.failureDetected = 0
                radio.openWritingPipe(pipes[0])
                radio.openReadingPipe(1,pipes[1])
                print('failure')
            
            print("Failed: ", code)
            time.sleep(0.1)
        print("Sent: ", code)
                
        # cooldown
        time.sleep(0.3)

def send_code(code):
    # The payload will always be the same, what will change is how much of it we send.
 
    # First, stop listening so we can talk.
    radio.stopListening()
 
    # Take the time, and send it.  This will block until complete
    radio.write(bytearray(code, 'utf-8'))
 
    # Now, continue listening
    radio.startListening()
 
    # Wait here until we get a response, or timeout
    started_waiting_at = millis()
    timeout = False
    while (not radio.available()) and (not timeout):
        if (millis() - started_waiting_at) > 500:
            timeout = True
 
    # Describe the results
    if timeout:
        return False
    else:
        # Grab the response, compare, and send to debugging spew
        len = radio.getDynamicPayloadSize()
        receive_payload = radio.read(len)
        return True