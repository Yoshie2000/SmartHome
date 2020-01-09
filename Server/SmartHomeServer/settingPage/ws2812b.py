import time
from RF24 import *
import RPi.GPIO as GPIO
 
payload_size = 16
millis = lambda: int(round(time.time() * 1000))
pipes = [0xF0E1, 0xF0D2]

r = init_radio()

def init_radio():
    r = RF24(22, 0)
    r.begin()
    r.enableDynamicPayloads()
    time.sleep(1)
    r.openWritingPipe(pipes[0])
    r.openReadingPipe(1,pipes[1])
    return radio

def send_profile(profile):

    for code in profile.setting_codes().split(";"):
            
        while send_code(code) == False:
            if radio.failureDetected:
                r = init_radio()
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