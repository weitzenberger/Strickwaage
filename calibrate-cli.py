#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""

Created on 16.02.2021 14:12

Modul zur Ansteuerung von HX711 Sensoren.

@author: L.We
E-Mail: lennart29.9@gmail.com

"""
import RPi.GPIO as GPIO  # import GPIO
from HX711.HX711_Python3.hx711 import HX711  # import the class HX711

try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    dout_pin = input('Definiere DOUT_PIN')
    pd_sck_pin = input('Definiere PD_SCK_PIN')

    hx = HX711(dout_pin=int(dout_pin), pd_sck_pin=int(pd_sck_pin))
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Bestimmung des Taragewichts nicht erfolgreich')

    offset = hx.get_raw_data_mean()

    if offset:  # always check if you get correct value or only False
        # now the value is close to 0
        print('Offset als raw data',
              offset)
    else:
        print('invalid data', offset)

    # In order to calculate the conversion ratio to some units, in my case I want grams,
    # you must have known weight.
    input('Bekanntes Gewicht auf die Waage legen und Enter drücken.')
    reading = hx.get_data_mean()
    if reading:
        print('Raw data unter Berücksichtung des Offsets', reading)
        known_weight_grams = input(
            'Schreib wie viel Gramm auf der Waage liegen: ')
        try:
            value = float(known_weight_grams)
            print(value, 'Gramm')
        except ValueError:
            print('Expected integer or float and I have got:',
                  known_weight_grams)

        # set scale ratio for particular channel and gain which is
        # used to calculate the conversion to units. Required argument is only
        # scale ratio. Without arguments 'channel' and 'gain_A' it sets
        # the ratio for current channel and gain.
        ratio = reading / value  # calculate the ratio for channel A and gain 128
        hx.set_scale_ratio(ratio)  # set ratio for current channel
        print('Ratio is set.')
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

    print('Zusammenfassung:'
          'dout_pin: {}'.format(dout_pin),
          'pd_sck_pin: {}'.format(pd_sck_pin),
          'ratio: {}'.format(ratio),
          'offset: {}'.format(offset),
          'Parameter müssen in strickwaage.py/SCALES manuell gesetzt werden')


    # Read data several times and return mean value
    # subtracted by offset and converted by scale ratio to
    # desired units. In my case in grams.
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    input('Press Enter to begin reading')
    print('Current weight on the scale in grams is: ')
    while True:
        print(hx.get_weight_mean(20), 'g')

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()
