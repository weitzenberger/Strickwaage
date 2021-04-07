#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on 16.02.2021 13:40

Modul zur Ansteuerung von HX711 Sensoren.

@author: L.We
E-Mail: lennart29.9@gmail.com

"""


import wiringpi
from HX711.HX711_Python3.hx711 import HX711

PIN_BASE_1 = 65
EXPANSION_BOARD_1 = 0x27

# In SCALES werden alle benötigten Parameter gesammelt. SCALES ist mithilfe von calibrate-cli.py händisch zu pflegen.
SCALES = {
    1: {  # Waagennummer als Key-Value
        "hx711": {
            "dout_pin": 2,  # Raspberry PI DOUT_PIN Nummer oder wenn "device_adress" definiert Binärcode für den PIN im Extensionboard
            "pd_sck_pin": 6,  # Raspberry PI PD_SCK_PIN Nummer
            "gain_channel_A": 128,  # Der gain ist optional. Default: 128
            "select_channel": 'A',  # Der Channel ist optional. Default: 'A'
            "pin_base": PIN_BASE_1
        },
        "offset": 107256,  # Offset wird mithilfe von calibrate-cli.py berechnet
        "ratio": 499.10877192982457  # ratio wird mithilfe von calibrate-cli.py berechnet
    },
    2: {
        "hx711": {
            "dout_pin": 1,
            "pd_sck_pin": 6,
            "gain_channel_A": 128,
            "select_channel": 'A',
            "pin_base": PIN_BASE_1

        },
        "offset": 231005,
        "ratio": 516.6733333333333
    },
    3: {
        "hx711": {
            "dout_pin": 0,
            "pd_sck_pin": 6,
            "gain_channel_A": 128,
            "select_channel": 'A',
            "pin_base": PIN_BASE_1

        },
        "offset": -9418,
        "ratio": 448.98833333333334
    }

}

def init():
    wiringpi.wiringPiSetup()
    wiringpi.mcp23017Setup(PIN_BASE_1, EXPANSION_BOARD_1)
    wiringpi.wiringPiSetupGpio()

def get_weight(scale_number):
    scale = SCALES.get(scale_number, None)
    if not scale:
        raise ValueError("Waage mit der Nummer {} ist in {}/@SCALES nicht definiert'".format(scale_number, __file__))
    kwargs = scale['hx711']
    hx = HX711(**kwargs)

    hx.set_offset(scale['offset'])
    hx.set_scale_ratio(scale['ratio'])

    weight = hx.get_weight_mean()
    while hx.get_current_scale_ratio(kwargs['select_channel'], kwargs['gain_channel_A']) == 1:
        # nochmal versuchen solange gain_channel nicht korrekt gesetzt werden konnte
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
    for scale_number in SCALES.keys():
        ls += get_weight(scale_number)
    return ls


if __name__ == '__main__':
    init()
    while True:
        print('start')
        print(get_weight(1))
        print(get_weight(1))
        print(get_weight(1))
        print(get_weight(2))
        print(get_weight(3))
        print(get_all())



