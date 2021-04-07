# RESTful API zur Auslesung von HX711 Sensoren



webapp.py:

Modul um den Web Service zu starten. Host und Port sind hart in webapp.py/HOST und webapp.py/PORT geschrieben

Web Service starten:
- cd usr/local/bin/Strickwaage
- python3 webapp.py

Web Service Methoden:
- scale/?id=id | id ist vom Typ integer und definiert die Waage
- scale/all | gibt alle definierten Waagen zurück
- Mit Konsolenbefehl "sudo noip2" kann der DNS Service gestartet werden. Wenn nicht mehr benötigt gerne deinstallieren.

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
- Anleitung befolgen. Terminologie: 
  - PD_SCK PIN: INPUT PIN auf dem RaspberryPI. Hiermit wird die Waage angesteuert (BitBanging etc.)
  - DOUT PIN: PIN auf dem ExtensionBoard. Hier wird die Waage ausgelesen
  - Device Adresse: Die Device Adresse des ExtensionBoards ist 0x27. Wenn weitere Extensionboards hinzukommen, kann man mit Konsolenbefehl "i2cdetect -y 1" die Adresse ausleesen.
- Am Ende muss die "Zusammenfassung" manuell in strickwaage.py/SCALES übertragen werden. Ggf. muss eine neue WaagenID definiert werden.

---

Probleme & Ausblick:

Der Web Service braucht recht lange um zu reagieren. Etwa 2 Sekunden. Grund: Nach Initialisierung der Waage muss 0.5 Sekunden gewartet werden (HX711 Datenblatt).
Es werden 20 Messungen durchgeführt (jetzt reduziert auf 6). Eine Paralleliserung der Waagenabfragen kann nicht durch Multithreading realisiert werden. 
Das Timing der GPIO Pins wäre dann nicht mehr korrekt. Möglich wäre es für die Ansteuerung der GPIO im Code zu parallelisieren. Ich habe damit im Code angefangen, war dann aber doch etwas aufwendig :P. Also erstmal schauen ob es reicht.
Ab und zu gibt die Waage einen absurd hohen Wert zurück (bspw.: 270kg für die Bierflasche). Das Problem ist, dass in diesem Moment der GAIN nicht richtig gesetzt wird und damit auch keine "ratio". In diesem Fall wird die Waage neu initialisiert und die Messung wiederholt.
Falls es möglich ist ohne Doppelbelegung der PD_SCK PIN (also der INPUT Pin auf dem Raspberry) alle Waagen anzuschließen, könnte man auch alle Waagen beim Starten des Web Service initialisieren und dann nur noch bei einem Request auslesen. 
Das würde evtl etwas beschleunigen und stabilisieren.