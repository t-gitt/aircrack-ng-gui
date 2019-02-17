# aircrack-ng GUI

An [aircrack-ng](https://www.github.com/aircrack-ng/aircrack-ng) gui interface using python-gtk3

## What can it do?
Performing a bruteforce attack on WPA/WPA2 networks using [aircrack-ng](https://www.github.com/aircrack-ng/aircrack-ng) and `iw`.

## Usage
### To Install On Linux
* make sure [aircrack-ng](https://www.github.com/aircrack-ng/aircrack-ng) is installed
* Clone the repo `git clone https://github.com/tqk-gh/aircrack-ng-gui.git`
* `cd aircrack-ng-gui/`
* Install the script by `sudo setup.py install`
* It should have added the script to /usr/bin/ and you can now run it from the terminal by `sudo aircrack-ng-gui.py`

#### Uninstall
* You can uninstall it through pip by `pip uninstall aircrack-ng-gui`


### To Manually Running the script
* make sure [aircrack-ng](https://www.github.com/aircrack-ng/aircrack-ng) is installed
* clone the repo
* install dependencies by `pip install -r requirements.txt`
* run aircrack-ng-gui by `sudo python aircrack-ng-gui.py` | make sure you are running it with python 3

> Airodump-ng output files are saved in `/home/$USER/.aircrack-ng-gui/`

## Screenshots

### Main Window
Main Window where user can choose to go to Scan, airmon-ng, and aircrack-ng windows after selecting the interface (wlp4s0)

![Alt text](screenshots/1.png?raw=true "ScreenShot 1")

### Airmon-ng  Window
A window to check, start or stop airmon-ng, along with starting and stopping systemd NetworkManager.service

![Alt text](screenshots/9.png?raw=true "ScreenShot 9")

### Scanning Window
A wifi access point scanning window. After choosing their interface, the user can scan for wifi ap using iw. Then, after choosing the target ap, they can go to airodump-ng after starting airmon-ng

![Alt text](screenshots/2.png?raw=true "ScreenShot 2")

### Airmon-ng "with ssid chosen" Window
Very similar to Airmon-ng window, except this one pass the ssid variables "SSID, BSSID, CHANNEL" to Airodump-ng window

![Alt text](screenshots/3.png?raw=true "ScreenShot 3")

### Airodump-ng Window | 1
To run airodump-ng (via desired terminal emulator) on the targeted SSID and output the file (with the handshake) to a desired file name. | (could be done better using STDERR and subprocess)

![Alt text](screenshots/5.png?raw=true "ScreenShot 5")



### Airodump-ng Window | 2
After running airodump-ng, the user can use aireplay to send deauthentication packets for desired n times and a desired station to capture the handshake

![Alt text](screenshots/6.png?raw=true "ScreenShot 6")

### Aircrack-ng Window
After saving the handshake into a cap file, aircrack can be accessed from the main window. The user chooses a .cap file that contain the handshake and a wordlist to perform the bruteforce attack on their desired terminal emulator.

![Alt text](screenshots/8.png?raw=true "ScreenShot 8")

## development stages
* Initially, it is to support airmon-ng, where the user can start, stop and check the status of airmon-ng.

* Access points scanning using "iw" with automatic bssid and channel extraction.

* Airodump-ng with ability to choose the access point, and airodump-ng will output the data in .cap format  * still looking for a way to autodetect the handshake and terminate airodump-ng

* An aircrack-ng window where the user can select a wordlist and the cap file that has the handshake. Then, the script will try to bruteforce the handshake using the wordlist

