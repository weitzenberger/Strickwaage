#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on 16.02.2021 13:40

In diesem Modul ist die API definiert.


@author: L.We
E-Mail: lennart29.9@gmail.com

"""


import flask
from flask import request, jsonify
import strickwaage

HOST = '0.0.0.0'
PORT = 80

app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/scale/', methods=['GET'])
def get_weight():
    """Gibt die angefragte Waage zurück.

    :return: [{scale: int,
               weight: float}]
    """
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        raise ValueError('Keine WaagenID für GET-Request angegeben.')
    result = strickwaage.get_weight(scale_number=id)
    return jsonify(result)


@app.route('/scale/all', methods=['GET'])
def get_all():
    """Gibt eine Liste aller definierten Waagen zurück.

    :return: [{scale: int,
               weight: float},
               ...]
    """
    result = strickwaage.get_all()
    return jsonify(result)

if __name__ == '__main__':
    strickwaage.init()
    app.run(host=HOST, port=PORT)



