# aircrack-ng GUI

A basic aircrack-ng gui interface using python-gtk3

## What can it do?
Initially, it is to support airmon-ng, where the user can start, stop and check the status of airmon-ng. | **Completed**

Access points scanning window using "iw" with automatic bssid and channel extraction after user chooses an ssid to be attacked. | **Completed**

Airodump-ng with a running timeout, user can choose the access point, specifiy for how long should airodump-ng listen to its trafic, and it will output the data in .cap format | **Completed** * also still looking for a way to autodetect the handshake and terminate airodump-ng

Aircrack-ng window where the user can select a wordlist and the cap file that has the handshake, then the script will try to bruteforce the ap using the wordlist | **Completed**


