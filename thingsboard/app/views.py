from django.shortcuts import render
import random
import string
from app.models import *
# from uuid import getnode
import netifaces
import socket
import binascii
import requests

from app.forms import *


def add_connection(source_ip, dest_ip, type_conn, timestamp):
    '''
    add a new connection of type = TCP/UDP/ARP/DNS whatever
    '''
    try:
        t = Thing.objects.get(ip_address=source_ip)
        t.destination_address = dest_ip
        t.type_of_connection = type_conn
        t.visited = timestamp
        t.save()
    except Exception:
        print "No owner wrt server!"
    return 1


def add_urls(source_ip, dest_url, timestamp):
    '''
    add a new URL
    '''
    try:
        t = Thing.objects.get(ip_address=source_ip)
        t.name = dest_url
        t.visited = timestamp
        t.save()
    except Exception:
        print "No owner wrt server!"
    return 1


def get_urls_connections(source_ip):
    f = open('/var/log/snort/alert')
    for l in f:
        if ip in l and "tcp" in l:
            # get destination ip
            # get timestamp
            # dest_ip =
            # type of connection
            # type_conn =

            # add to the connections table of source ip
            add_connection(source_ip, dest_ip, type_conn, timestamp)
        if source_ip in l and "dns" in l:
            # get destination URL
            # get timestamp

            # add to the urls table of source ip
            add_urls(source_ip, dest_url, timestamp)

    f.close()


def fetch_vendor(mac):
    MAC_URL = 'http://macvendors.co/api/' + mac
    r = requests.get(MAC_URL)
    return str(r.json()['result']['company'])


def fetch_ip(mac):
    f = open('/proc/net/arp')
    ip = ""
    for x in f.readlines():
        if mac in x:
            ip = x.split()[0].strip()
            break
    return ip


def index(request):
    return render(request, 'app/index.html')


def block_url(url, source_device_ip):
    '''
    # take url,
    # get its ip from DNS
    # convert ip to hex to suit snort format
    # make rule with host IP as source device's ip
    # give a unique sid for the rule
    '''

    url_to_block = "app.hubbleconnected.com"
    # get ip from dns
    ip = socket.gethostbyname(url_to_block)
    hex_ip = binascii.hexlify(socket.inet_aton(ip))

    f = open("/etc/snort/rules/local.rules", 'a')
    rule = 'drop tcp any any <>' + hex_ip + \
        'any (content: "web url"; msg: "Access Denied"; react:block; sid:' + \
        str(random.randint(1, 10) + 1000000) + ';'
    f.write(rule)


def get_server_mac_address():
    x = netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
    return x


def add_owner(request):
    source_ip = request.get_host().split(":")[0]

    if len(Thing.objects.filter(ip_address=source_ip)) < 1:
        unique_name = "server"
        mac = get_server_mac_address()
        thing = Thing(name=unique_name, mac_address=mac,
                      ip_address=source_ip, admin_or_not=True)
        thing.save()


def things(request):
    '''
    # detect new devices
    # check them in DB
    # if not present, add device in DB
    '''

    # add_owner(request)

    '''
    # get owner from the DB, if current request is from owner, show this page
    # else redirect to home
    '''
    source_ip = request.get_host().split(":")[0]
    print source_ip
    t = {}

    try:
        t = Thing.objects.get(ip_address=source_ip)
        t.admin_or_not = True
        t.save()
    except Exception:
        print "No owner wrt server!"

    try:
        f = open("../../ap.log")
        for line in f.readlines():
            if ("AP-STA-CONNECTED" in line):
                spl = line.split()
                mac = spl[3].strip()
                if len(Thing.objects.filter(mac_address=mac)) < 1:
                    print "New device found!"
                    # add a new device, not already present
                    unique_name = ''.join(random.choice(
                        string.ascii_uppercase + string.digits)
                        for _ in range(6))
                    thing = Thing(name=unique_name, mac_address=mac,
                                  ip_address=fetch_ip(mac), admin_or_not=False,
                                  vendor=fetch_vendor(mac))
                    thing.save()
                else:
                    print "Device already in the DB!"
    except Exception:
        print "No file called ap.log"
    context = Thing.objects.all()

    return render(request, 'app/things.html', {'things': context})


def thing(thingid):
    t = Article.objects.get(pk=thingid)
    f = ThingForm(instance=t)
    return render(request, 'app/thing.html', {'thing': f})
