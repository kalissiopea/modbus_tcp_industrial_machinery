from pyModbusTCP.client import ModbusClient

import argparse
import logging
import sys
import time
import RPi.GPIO as GPIO
import Adafruit_DHT



#implementare funzioni: accensione servo motor in base all'angolo (90 e 180), accensione step motor (vedere i parametri), lettura parametri sensore (temperatura, umidità)

#funzione servo motor
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False
    
    start = 4
    end = 12.5
    ratio = (end - start)/180
    
    angle_as_percent = angle * ratio
    
    return start + angle_as_percent

def register_move_servo(reg_addr, reg_nb):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pwm_gpio = 35
    frequence = 50
    GPIO.setup(pwm_gpio, GPIO.OUT)
    pwm = GPIO.PWM(pwm_gpio, frequence)
    pwm.start(angle_to_percent(0))
    time.sleep(1)
    
    client1 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)
    regs_list1 = client1.read_holding_registers(reg_addr, reg_nb)

    for regs_1 in regs_list1:
       pwm.ChangeDutyCycle(angle_to_percent(regs_1))
       time.sleep(1)
       pwm.ChangeDutyCycle(angle_to_percent(0))
       pwm.stop()

#funzione step motor (direzione 1=dex 2=sinix)
def registers_move_step(reg_addr, reg_nb):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    aMotorPins = [12, 15, 11, 13]
    for pin in aMotorPins:
       GPIO.setup(pin, GPIO.OUT)
       GPIO.output(pin, False)
    
    aSequence = [
        [1,0,0,1],
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
    ]

    iNumSteps = len(aSequence)
    
    client1 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)
    regs_list2 = client1.read_holding_registers(reg_addr, reg_nb)
    print(regs_list2)
    regs_list2.insert(0, 0)
    r = regs_list2
    print(r)

    if r[3] == 1:
      iDirection = -1
    else:
      iDirection = 1
   
    fWaitTime = int(regs_list2[1]) / float(1000)

    iDeg = int(int(regs_list2[2]) * 11.377777777777)

       
    iSeqPos = 0

    #If the fourth argument is present, it means that the motor should start at a specific position from the aSequence list
    if len(r) > 4:
       iSeqPos = int(r[4])
    
    
    for step in range(0, iDeg):
       
       for iPin in range(0, 4):
          iRealPin = aMotorPins[iPin]
          if aSequence[iSeqPos][iPin] != 0:
             GPIO.output(iRealPin, True)
          else:
             GPIO.output(iRealPin, False)
       iSeqPos += iDirection
    
       if (iSeqPos >= iNumSteps):
          iSeqPos = 0
       if (iSeqPos < 0):
          iSeqPos = iNumSteps + iDirection
    
       #Time to wait between steps
       time.sleep(fWaitTime)
    
       for pin in aMotorPins:
          GPIO.output(pin, False)
    
       #print(iSeqPos)

#funzione per il sensore DHT11
def give_data(reg_addr, reg_nb):
    client1 = ModbusClient(host='localhost', port=1502, unit_id=1, timeout=60.0, debug=False, auto_open=True, auto_close=False)
    regs_list3 = client1.read_holding_registers(reg_addr, reg_nb)
    if regs_list3[0] is not None and regs_list3[1] is not None:
	    #return ('Temperatura={0:0.1f}*C Umidità={1:0.1f}%'.format(regs_list3[1], regs_list3[0]))
       return regs_list3
    else:
	    return ('Errore nella acquisizione valori') 












