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
    return render(request, 'app/things.html', {'things': context})
