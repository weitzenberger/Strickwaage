#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on 16.02.2021 13:40

Modul zur Ansteuerung von HX711 Sensoren.

@author: L.We
E-Mail: lennart29.9@gmail.com

"""


import RPi.GPIO as GPIO
from HX711.HX711_Python3.hx711 import HX711


# In SCALES werden alle benötigten Parameter gesammelt. SCALES ist mithilfe von calibrate-bli.py händisch zu pflegen.
SCALES = {
    1: {  # Waagennummer als Key-Value
        "hx711": {
            "dout_pin": 6,  # Raspberry PI DOUT_PIN Nummer
            "pd_sck_pin": 5,  # Raspberry PI DOUT_PIN Nummer
            "gain_channel_A": 128,  # Der gain ist optional. Default: 128
            "select_channel": 'A'  # Der Channel ist optiona. Default: 'A'
        },
        "offset": 9999,  # Offset wird mithilfe von calibrate-bli.py berechnet
        "ratio": 9999  # ratio wird mithilfe von calibrate-bli.py berechnet
    }

}

def get_weight(scale_number):
    GPIO.setmode(GPIO.BCM)

    scale = SCALES.get(scale_number, None)
    if not scale:
        raise ValueError("Waage mit der Nummer '{} ist in {}/@SCALES nicht definiert'".format(scale_number, __file__))
    kwargs = scale['hx711']
    hx = HX711(**kwargs)

    hx.set_offset(scale['offset'])
    hx.set_scale_ratio(scale['ratio'])
    weight = hx.get_weight_mean()

    return [
        {
            "weight": weight,
            "waage": scale_number
        }
    ]

def get_all():
    ls = []
    for scale_number in SCALES.keys():
        ls += get_weight(scale_number)
    return ls

