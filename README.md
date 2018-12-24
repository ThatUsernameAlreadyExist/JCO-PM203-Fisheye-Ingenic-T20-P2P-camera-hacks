#JCO PM203 Fisheye Ingenic T20 P2P camera hacks
Hacks for p2p-only camera that allow you to use rtsp/web-interface/ftp and other functions.
**NOTE: this hack doesn't modify or upgrade firmware - you can restore the original state of the camera at any time (hack work only with MicroSD-card!).**
This repo is based on hacks for Xiaomi cameras: 
**https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks**

Supported camera model: **JCO HOOM PM203** with Ingenic T20 CPU
![JCO HOOM PM203](/JCO_PM203.jpg)
Also known as:
* [Lensoul 1080P HD Wireless IP Camera](https://www.amazon.com/Lensoul-Detection-Surveillance-Vision-Cloud-Available/dp/B079L94FB7)
* [OWSOO 180-degree Fisheye IP Camera HD 1080P](https://www.amazon.com/OWSOO-180-degree-Fisheye-Wireless-Security/dp/B07G9D9MG3)
* [SANNCE 1080P HD Indoor IP Camera, 180-degree](https://www.amazon.co.uk/SANNCE-180-degree-Wireless-Available-Detection/dp/B07CKS6YS6)
* [Kingkonghome IP Camera Wireless 1080P Wifi Camera](https://www.aliexpress.com/item/Kingkonghome-IP-Camera-Wireless-1080P-Wifi-Camera-Security-Smart-Pet-Camera-Surveillance-Night-Vision-180-degree/32919998389.html)

##How to install
1. Prepare an MicroSD-card with FAT32 filesystem
2. Copy all data from /hacks/microsd folder to MicroSD-card
3. Connect the camera to your WiFI network through Danale app (Android/IOS). See IP-address of the camera in your WiFi-router settings (required to connect via telnet).
4. Place MicroSD-card in camera 
5. Reboot camera
6. After rebooting connect to your camera via telnet (note: telnet works only 5 min after camera start):
    port:     9527
    username: root
    password: jco66688
7. In telnet terminal run command:
    */opt/media/mmcblk0p1/install.sh*
8. After installing camera will be rebooted.
Now you can connect to the camera via browser (https://CAMERA-IP), get RTSP-stream(rtsp://CAMERA-IP:554/unicast), download/upload files via FTP and many other things.
**When hack is enabled, default Danale cloud function will not be available.**

##How to uninstall
To temporary disable hacks: just remove MicroSD-card and reboot camera. To enable hack - insert MicroSD-card and reboot camera.
To permanently remove hacks:
1. Connect to your camera via telnet (note: telnet works only 5 min after camera start)
2. In telnet terminal run command:
    */opt/media/mmcblk0p1/uninstall.sh*
3. After uninstalling camera will be rebooted.

##Misc
* Tested on **firmware: api_ver: 1.0.180323 fw_ver: 3.1.34**
* Default camera login/password: root/jco66688
* Change password for http-access in web interface
* Change login/password for rtsp in web interface or in config-file: /config/rtspserver.conf (rtspserver.conf.dist)
* Change login/password for ftp in config-file: /config/bftpd.password
* For disable ftp/telnet/web-interface: remove files 'system-*' from /config/autostart and reboot camera
* UART connection - see /information/teardown/P_20181212_224700.jpg COM port speed: 115200
* To change WiFi credentials or connect to new network: change(or create) file wpa_supplicant.conf in MicroSD-card and reboot.
wpa_supplicant.conf format:
    ctrl_interface=/var/run/wpa_supplicant
    ctrl_interface_group=0
    ap_scan=1
    network={
            ssid="YOUR WIFI SSID"
            key_mgmt=WPA-PSK
            psk="YOUR PASSWORD"
            priority=2
    }
