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
import concurrent.futures
import time



# In SCALES werden alle benötigten Parameter gesammelt. SCALES ist mithilfe von calibrate-cli.py händisch zu pflegen.
SCALES = {
    1: {  # Waagennummer als Key-Value
        "hx711": {
            "dout_pin": 0b00000001,  # Raspberry PI DOUT_PIN Nummer oder wenn "device_adress" definiert Binärcode für den PIN im Extensionboard
            "pd_sck_pin": 0b00000001,  # Raspberry PI PD_SCK_PIN Nummer
            "gain_channel_A": 128,  # Der gain ist optional. Default: 128
            "select_channel": 'A',  # Der Channel ist optional. Default: 'A'
            "device_address": 0x27,  # Device Adresse von dem ExpansionBoard in Hexadezimal


        },
        "offset": 107154,  # Offset wird mithilfe von calibrate-cli.py berechnet
        "ratio": 513.8683333333333  # ratio wird mithilfe von calibrate-cli.py berechnet
    }

}

def get_weight(scale_number):
    GPIO.setmode(GPIO.BCM)

    scale = SCALES.get(scale_number, None)
    if not scale:
        raise ValueError("Waage mit der Nummer {} ist in {}/@SCALES nicht definiert'".format(scale_number, __file__))
    kwargs = scale['hx711']
    hx = HX711(**kwargs)

    hx.set_offset(scale['offset'])
    hx.set_scale_ratio(scale['ratio'])
    weight = hx.get_weight_mean()

    return [
        {
            "weight": weight,
            "scale": scale_number
        }
    ]

def get_all():
    ls = []
    threads = []
    with concurrent.futures.ThreadPoolExecutor as executor:
        for scale_number in SCALES.keys():
            thread = executor.submit(get_weight, scale_number)
            threads.append(thread)

        for f in concurrent.futures.as_completed(threads):
            ls += f.result()
    return ls

if __name__ == '__main__':
    while True:
        print('start')
        print(get_weight(1))
        time.sleep(1)