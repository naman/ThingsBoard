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

#ip to url
from ipwhois import IPWhois


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
        if source_ip in l and "TCP" in l:
            alert_tcp = l.split(" ")
            # get destination ip
            dest_ip_tcp = alert[11]
            # get timestamp
            timestamp_tcp = alert[0]
            # type of connection
            type_conn = alert[4]

            # add to the connections table of source ip
            add_connection(source_ip, dest_ip_tcp, type_conn, timestamp_tcp)
        if source_ip in l and "DNS" in l:
            # get destination URL
            alert_dns = l.split(" ")

            dest_ip_dns = alert[11]

            #convert IP to URL
            obj = IPWhois(dest_ip_dns)
            dest_url = obj.lookup_rdap(depth=1)
            
            # get timestamp
            timestamp_dns = alert[0]
            
            # add to the urls table of source ip
            add_urls(source_ip, dest_url, timestamp_dns)

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
    # add_owner(request)
    '''
    # get owner from the DB, if current request is from owner, show this page
    # else redirect to home
    '''
    source_ip = request.get_host().split(":")[0]

    try:
        t = Thing.objects.get(ip_address=source_ip)
        t.admin_or_not = True
        t.save()
    except Exception:
        print "No owner wrt server!"

    '''
    # detect new devices
    # check them in DB
    # if not present, add device in DB
    '''
    try:
        f = open("../../ap-srish.log")
        for line in f:
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

    return render(request, 'app/things.html', {'things': Thing.objects.all()})


def thing(thingid):
    t = Article.objects.get(pk=thingid)
    f = ThingForm(instance=t)
    return render(request, 'app/thing.html', {'thing': f})
