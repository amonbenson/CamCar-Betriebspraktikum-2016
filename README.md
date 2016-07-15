# Betriebspraktikum 2016 - CamCar

"CamCar" ist der Entwicklungsname des Roboters, den ich über die Zeit des Praktikums gebaut habe.
Die beiden Ordner "camcar" müssen jewails für den Raspberry Pi und für den EV3 in das Benutzer-
verzeichnis kopiert werden (auf den EV3 habe ich ev3dev benutzt, auf dem Raspberry Pi ein ganz
normales Raspbian Image).

Zunächst müssen beide Geräte mit dem WLAN verbunden werden (es funktioniert natürlich auch per LAN,
aber so brauch man keinerlei Verbindungskabel). Der Raspberry Pi muss mit einem Display und einer
Tastatur versorgt werden, oder per LAN Kabel und SSH verbunden werden, sodass die Netzwerkdateien
auf die WLAN Verbindung angepasst werden können. Auf dem EV3 kann das ganze mit einem WLAN Stick
und über die graphische Benutzeroberfläche geschehen.

Die Datei "CamCar.py" muss (mit Python 2.7) auf dem EV3 gestartet werden,
um die Kommunikation zu ermöglichen. In dieser Datei könne außerdem die angeschlossenen Sensoren
angepasst werden (das Programm wird nicht funktionieren, wenn andere Sensoren angeschlossen sind.
Dem Raspberry Pi muss der Hostname "ev3dev" als die IP-Addresse des EV3 bekannt sein, sollte dies
nicht der Fall sein, muss die Datei "/etc/hosts" entsprechend editiert werden.

Um den Raspberry Pi mit dem EV3 kommunizieren lassen zu können, gibt es eine Bibliothek "RemoteEV3",
welche einige Befehle zum senden von Motorbefehlen und empfangen von Sensordaten sowie ein kleines
Test-Script beinhaltet. Die Datei CamCar ist eine Erweiterung von RemoteEV3 und ist spezialisiert
auf diesen Roboter. Außerdem benutzt sie die ServoControl.py Datei, um mit den beiden Servos an der
Kamera zu kommunizieren. Die Dateien Ball.py und EmotionTest.py sind Beispiele, welche einfach mit
python3.4 ausgeführt werden können.
