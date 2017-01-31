from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import connection


def index(request):
    return render(request, 'app/index.html')

def detect(request):
    # detect new devices
    # check them in DB
    # if not present, add device in DB
    logfile = open("/home/pi/Documents/BTP/ap.log", "r")
    for line in logfile.readlines():
        if ("AP-STA-CONNECTED" in line):
            print "New device connected"
            spl = line.split(" ")
            print "MAC: " + spl[3]
    return render(request, 'app/detect_devices.html')
    
def owner(request):
    # get owner from the DB, if current request is from owner, show this page
    # else redirect to home 
    return render(request, 'app/owner.html')

def things(request):
    context = [{'id': 1, 'name': 'Motorola FOCUS 66',
                'description': 'Smart Security Camera', 'events': ['']},
               {'id': 2, 'name': 'Raspberry Pi',
                'description': 'Gateway', 'events': ['01/06-11:29:31.458958  [**] [1:10000024:1] Possible TCP DoS [**] [Priority: 0] {TCP} 192.168.26.25:50145 -> 192.168.26.186:80']}]
    # read the log file and update context dictionary
    # add to the events array
    f = open('/var/log/snort/alert')
    for x in f.readlines():
        split = x.split()
        time_stamp = split[0]
        packet_type = split[3]
        packet_method = split[4]
        destination = split[len(split) - 1]

        event = time_stamp + "\t" + packet_type + \
            "\t" + packet_method + " with " + destination
        context[0]['events'].append(x)

    return render(request, 'app/things.html', {'things': context})
