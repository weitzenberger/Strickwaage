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

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def get_weight(waage):
    """Gibt die angefragte Waage zurück.

    :param waage: int | Nummer der anzusteuerenden Waage
    :return: [{waage: int,
               weight: float}]
    """
    if 'waage' in request.args:
        id = int(request.args['waage'])
    else:
        raise ValueError('Keine WaagenID für GET-Request angegeben.')
    result = strickwaage.get_weight(scale_number=id)
    return jsonify(result)


@app.route('/all', methods=['GET'])
def get_all():
    """Gibt eine Liste aller definierten Waagen zurück.

    :return: [{waage: int,
               weight: float},
               ...]
    """
    result = strickwaage.get_all()
    return jsonify(result)

app.run()