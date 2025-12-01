# Retro.I
![Radio](./assets/splashscreen/splash.png) \
Ein Projekt der Klasse "FWI1" des BSZ-Wiesau\
Einem **Grundig Type 5088**, Baujahr **1957/1958**, wird neues Leben eingehaucht!\
Dazu werden folgende Technologien verwendet:
* Raspberry PI 4 (4GB)
* Python
* Flet
* EasyEffects

Folgende Hardware wurde verwendet:
* WS2812B LED-Streifen
* Rotary Drehregler
* 4 Passive-Lautsprecher
* Touch-Display
* Verstärker-Platine
* 24V Schaltnetzteil

## Setup
Für das Setup existiert eine eigene [Doku-Seite](https://docs.retroi.de/setup/). \
Hier kann alles nötige und Wissenswerte rund um das Aufsetzen der Software nachgelesen werden.

## Bedienung
Auch für die Bedienung existiert eine [Doku-Seite](https://docs.retroi.de/user-manual/).
Hier sind alle nötigen Infos für die Bedienung der Software nachzulesen.

<!--
### Lautstärke
Die Lautstärkenregelung erfolgt über den original Drehknopf des Radios!\
Der Rotary Drehregler gibt sein Signal an den Raspberry weiter und steuert somit die Lautstärke des Geräts.

### Stummschaltung
Der Wechsel von Stummschaltung/Aufhebung erfolgt über Drücken des gleichen Drehreglers wie zur Veränderung der Lautstärke.

### Bass/Höhen
Die Veränderung von Bass/Höhen ist über weitere Rotary-Drehregler möglich! Hierzu wird die Software `EasyEffects` verwendet:\
`sudo apt install easyeffects`

### WS2812B LED-Streifen
TODO - Setup-Skript erweitern, dass die Anzahl der LED's beim Setup angegeben werden kann

Der LED-Streifen mit `62` LED's wird ebenfalls über den Raspberry angesteuert.\
Jeder Radiosender verfügt über eine Farbe, welche den Radiosender repräsentiert. Diese Farbe wird bei Auswahl des jeweiligen Radiosenders auf dem Streifen in einer Animation angezeigt.
-->

<!--
## Features/Software
### Radio
![Radio](./assets/doc/readme-images/radio_page.png) \
Auf dieser Seite können die voreingestellten Radiosender abgespielt, gelöscht und neu hinzugefügt werden.\
Um einen Sender von der Favoriten-Seite zu entfernen, muss lange auf den Sender gedrückt werden.\
Um neue Sender zu suchen und hinzuzufügen, muss nach diesem im Such-Dialog (Sendersuche, oben rechts) gesucht werden

### Bluetooth
![Bluetooth](./assets/doc/readme-images/bluetooth_page.png) \
Möchte man den Radio als **Bluetooth-Box** verwenden, ist dies in diesem Tab möglich.\
Dabei stoppt der aktuell spielende Radiosender und Bluetooth wird aktiviert.\
Wechselt man wieder zurück zum Radio-Tab, werden alle Bluetooth-Verbindungen gekappt und Bluetooth systemweit deaktiviert. Dies verhindert das ungewollte Verbinden, während des Radio-Betriebs!

Wenn du ein neues Gerät mit dem Radio verbinden möchtest, musst du **Bluetooth-Discovery** aktivieren! (Bluetooth sichtbar/nicht sichbar)

### Soundboard
![Soundboard](./assets/doc/readme-images/soundboard_page.png) \
Hier befindet sich ein komplett konfigurierbares Soundboard.
Es kann nach Sounds gesucht und diese zum eigenen Soundboard hinzugefügt werden.

### Einstellungen
![Einstellungen](./assets/doc/readme-images/settings_page.png) \
Über diese Seite kann der Radio unter folgenden Punkten konfiguriert werden:
* Helligkeit des LED-Streifen bzw. generell leuchten/nicht leuchten
* Helligkeit des Touch-Bildschirms

Zusätzlich können weitere Informationen wie z.B. WLAN-Konfiguration entnommen werden.

Nicht zuletzt, werden die Personen aufgeführt, dank Ihnen dieses Projekt zu einem großen Erfolg wurde!

## Anzeige Lautstärke
Die Lautstärke wird über einen Rotary-Drehregler gesteuert.\
Durch den verbauten LED-Streifen wird bei Änderung der Lautstärke eine Animation angezeigt.\
Bei Stummschaltung (durch Druck des Drehreglers) erscheint der LED-Streifen in der Farbe Rot.\
Beides wird ebenfalls in der oberen Taskleiste als Icon dargestellt.

### Auswahl WLAN-Netzwerk
Ebenfalls ist über das WLAN-Icon in der oberen Taskleiste die Auswahl des WLAN-Netzwerks möglich:
![WLAN](./assets/doc/readme-images/wifi_networks.png)

### Aktuell spielender Radiosender
Erkennbar ist der aktuell spielende Radiosender über ein passendes [GIF](./assets/party.gif) ;D
![Bluetooth](./assets/doc/readme-images/radio_playing.png) \
Jeder Radiosender wird auf dem LED-Streifen und in der Software mit einer entsprechenden Farbe dargestellt. \
Wie im Beispiel zu sehen "Bayern 1" wird mit der Farbe Hellblau dargestellt.

## Verwendung der GPIO-Pin's
### Rotary Drehregler (Lautstärke)
* `5` - SW-PIN: Stummschaltung/Aufhebung Stummschaltung
* `6` - DT-PIN: Leiser
* `13` - CLK-PIN: Lauter

### Rotary Drehregler (Bass Anhebung/Absenkung Frequenzbereich ##hz - ##hz)
* `8` - DT-PIN: weniger Bass'
* `7` - CLK-PIN: mehr Bass'

### Rotary Drehregler (Höhen Anhebung/Absenkung Frequenzbereich ##hz - ##hz)
* `24` - DT-PIN: weniger Höhen
* `23` - CLK-PIN: mehr Höhen

### LED-Streifen
* `10` - Datenpin für Ansteuerung des WS2812B LED-Streifens

> Eine genaue Beschreibung der belegten GPIO-Pins kann im Projekt unter `assets/doc` entnommen werden

-->