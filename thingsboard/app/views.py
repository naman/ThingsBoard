from django.shortcuts import render
import random
import string
from app.models import *
from django.http import HttpRequest


import socket
import binascii

def add_connection():
    '''
    add a new connection TCP/UDP/ARP/DNS whatever
    '''
    return 1


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


def owner(request):
    '''
    # get owner from the DB, if current request is from owner, show this page
    # else redirect to home
    '''
    host_ip = request.get_host().split(":")[0]
    
    t = {}

    try:
        t = Thing.objects.get(ip_address=host_ip)
        t.admin_or_not = True
        t.save()
    except Exception as e:
        print "No owner wrt server!"

    return render(request, 'app/owner.html',{'t': t})


def block_url(url, source_device_ip):
    '''
    # take url,
    # get its ip from DNS
    # convert ip to hex to suit snort format
    # make rule with host IP as source device's ip
    # give a unique sid for the rule
    '''

    url_to_block = "app.hubbleconnected.com"
    #get ip from dns
    ip = socket.gethostbyname(url_to_block)
    hex_ip = binascii.hexlify(socket.inet_aton(ip))

    f = open("/etc/snort/rules/local.rules", 'a')
    rule = 'drop tcp any any <> hex_ip any (content: "web url"; msg: "Access Denied"; react:block; sid:1000015;'
    f.write(rule)    


def things(request):
    '''
    # read the log file and update context dictionary
    # add to the events array
    '''

    # f = open('/var/log/snort/alert')
    # for x in f.readlines():
    #     split = x.split()
    #     time_stamp = split[0]
    #     packet_type = split[3]
    #     packet_method = split[4]
    #     destination = split[len(split) - 1]

    #     event = time_stamp + "\t" + packet_type + \
    #         "\t" + packet_method + " with " + destination
    #     context[0]['events'].append(x)

    '''
    # detect new devices
    # check them in DB
    # if not present, add device in DB
    '''
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
                        string.ascii_uppercase + string.digits) for _ in range(6))
                    thing = Thing(name=unique_name, mac_address=mac,
                                  ip_address=fetch_ip(mac), admin_or_not=False)
                    thing.save()
                else:
                    print "Device already in the DB!"
    except Exception as e:
        print "No file called ap.log"
    context = Thing.objects.all()
    return render(request, 'app/things.html', {'things': context})
