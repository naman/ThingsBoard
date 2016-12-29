from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import connection


def index(request):
    return render(request, 'app/index.html')


def things(request):
    context = [{'id': 1, 'name': 'Motorola FOCUS 66',
                'description': 'Smart Security Camera', 'events': ['Off state']},
               {'id': 2, 'name': 'Smart Bulb',
                'description': 'Bulb', 'events': ['Off state']}]
    # read the log file and update context dictionary
    # add to the events array
    f = open('/var/log/snort/alert')
    for x in f.readlines():
        split = x.split()
        time_stamp = split[0]
        packet_type = split[3]
        packet_method = split[4]
        destination = split[len(split) - 1]

        event = time_stamp + "\t" + packet_type +  "\t" + packet_method + " with " + destination 
        context[0]['events'].append(event)

    return render(request, 'app/things.html', {'things': context})
