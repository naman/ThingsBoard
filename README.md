# ThingsBoard
A dashboard for tracking IoT activity + IDS. Please read the paper for further information: http://ieeexplore.ieee.org/document/7945418/

# Overview

## Operating System / System Requirements
1. Raspberry Pi (RPi)
2. Raspbian OS on the RPi.
3. RJ45 ethernet Cable
4. A set of IoT devices

### Gateway

To use the RPi as a gateway, connect using two NICs (network infterfaces).
1. Ethernet to get connectivity to the internet.
2. Wi-Fi to make an ad-hoc hotspot LAN which IoT devices will connect to.

We have used hostapd to configure RPi as an access point and setup dnsmasq (to be used as a DHCP service) to assign IP addresses to the IoT devices connected via the ad-hoc hotspot LAN.

### Firewall/Intrusion Detection System + Dashboard

We have used Snort IDS to identify various types of connections, attacks and log them in files. We used Django to make a frontend web UI, which acts as an interface to for tweaking Snort configuration and parse the logs (mentioned earlier) in order to display the status of the IoT device, and the connections that it makes in realtime etc. Please read the interface logic in Django views (https://github.com/naman/ThingsBoard/blob/master/thingsboard/app/views.py).

# Installation

1. Install Raspbian OS (https://www.raspberrypi.org/downloads/raspbian/).
2. Setup a Wifi LAN ad-hoc hotspot network (https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/).
3. Make sure some of the IoT devices are connected successfully (get an IP address) and are able to connect to the internet through the RPi (acting as a gateway).
3. Setup Snort IDS on Raspberry Pi with the proper configuration and rules to monitor/log IoT traffic. (https://www.snort.org/downloads)
4. For the dashboard on RPi,  
    4.1 Clone the repo.
    4.2 Install python and pip using https://pip.pypa.io/en/latest/installing.html.
    4.3 Install all the package requirements using `pip install -r requirements.txt`.
    4.4 The project uses SQLite3 as the database. Create a database and initial migrations using `python manage.py syncdb && python manage.py migrate`.
    4.5 Collect all the static files by running `python manage.py collectstatic`.
    4.6 Run the server using `python manage.py runserver`. Open http://localhost:8080 to view the dashboard.

