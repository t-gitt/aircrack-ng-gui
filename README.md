# aircrack-ng GUI

A basic aircrack-ng gui interface using python-gtk3

## What can it do?
Initially, it is to support airmon-ng, where the user can start, stop and check the status of airmon-ng. | Completed

Access points scanning window using "iw" with automatic bssid and channel extraction after user chooses an ssid to be attacked. | Completed

Airodump-ng with a running timeout, user can choose the access point, specifiy for how long should airodump-ng listen to its trafic, and it will output the data in .cap format | In progress * also still looking for a way to autodetect the handshake and terminate

Aircrack-ng window where the user can select a wordlist and the cap file that has the handshake, then the script will try to bruteforce the ap using the wordlist | In progress


# Screenshots
## Main Window where users are to choose an interface (wlp4s0)
![Alt text](1.png?raw=true "ScreenShot 1")

## Airmon-ng Window where users can check|start|stop airmon-ng and disable|enable their NetworkManager.service 
![Alt text](2.png?raw=true "ScreenShot 2")

## Wifi Scanning Window (Scanning is done with iw instead of airodump-ng cause I wasn't successful in outputting airodump-ng in realtime) where users are to choose an ssid to attack, and extract the 3 variables we'll need for airodump-ng to get the handshake (ssid, bssid, channel)
![Alt text](3.png?raw=true "ScreenShot 3")
