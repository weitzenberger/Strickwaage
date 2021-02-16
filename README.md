# RESTful API zur Auslesung von HX711 Sensoren



webapp.py:

Modul um den Web Service zu starten. Host und Port sind hart in webapp.py/HOST und webapp.py/PORT geschrieben

Web Service starten:
- cd usr/local/bin/Strickwaage
- python3 webapp.py

Web Service Methoden:
- /?waage=id | id ist vom Typ integer und definiert die Waage
- /all | gibt alle definierten Waagen zurück

Response Datenstruktur:
[
  {
    "scale": 1, 
    "weight": xxx
  },
  ... ,
  {
    "scale": n, 
    "weight": yyy
  },
  ]

---

calibrate-cli.py:

Modul um Waage zu kalibrieren. Die Waage muss beim Start angeschlossen sein. Es soll kein Gewicht aufliegen bzw. nur das Offsetgewicht.
Die GPIO-PIN Nummern DOUT_PIN und PD_SCK_PIN an denen die Waage angeschlossen ist, müssen bekannt sein.

- cd usr/local/bin/Strickwaage
- python3 calibrate-cli.py
- Anleitung befolgen
- Am Ende muss die "Zusammenfassung" manuell in strickwaage.py/SCALES übertragen werden. Ggf. muss eine neue WaagenID definiert werden.

___

Probleme & Ausblick:

Der Web Service brauch recht lange um zu reagieren. Etwa 2 Sekunden. Da müsste man nochmal schauen, ob man das reduzieren kann.
Ab und zu gibt die Waage einen absurd hohen Wert zurück (bspw.: 270kg für die Bierflasche). Anscheinend liegt das an kurzzeitigen Spannungsspitzen
an den GPIO-Pins liegt. Das Modul hx711.py versucht eigentlich diese Werte rauszufiltern. Klappt aber anscheinend nicht so gut. 
Wenn man einen sinnvollen Wertebereich für das Gewicht definiert, könnte man diese Werte abfangen und eine Messung wiederholen.

Es sollen zukünftig 32 bzw. 64 Waagen an den RPI angeschlossen werden. Es ist zu klären, ob das technisch umsetzbar ist.
- GPIO-Pin-Erweiterung
- wie lange dauert /all GET-Request? Evtl. multi-Threading einführen.
- Reicht die Hardware aus? (Raspberry PI 3 1 GB RAM)
