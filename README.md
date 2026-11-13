# RasPiLCD
RaspberryPi Treiber für ein LCD-Display in Python und API-Zugriff auf Spotify.


## LCD-Treiber
Der LCD-Treiber richtet die Pins am RaspberryPi ein, wählt entsprechende Modi aus und sendet bitweise die Daten. <br>
<br>
Buchstaben werden zunächst in eine passende Bitfolge konvertiert. Die richtigen Werte stehen in *encoding.py* als dictionary bereit.
Die Bitfolge wird dann an die richtigen Pins angelegt (8 Pins im 8-Bit Mode, 4 Pins im 4-Bit Mode) und per Pulse an das Display gesendet.<br>
<br>
Für Befehle muss ein extra Mode-Pin auf *0* gesetzt werden.

## Spotify-Api
In *spotify_api.py* werden die Authentification-Tokens angefragt und aktuell gehalten. Zusätzlich werden Anfragen zum Track, Artist und gespielten Zeit gestellt.<br>
Die Tokens werden in einer separaten Datei gespeichert.

## Anzeige
Treiber und API kommen in *display.py* zusammen und zeigen den gespielten Song mit Artist und Dauer an.
