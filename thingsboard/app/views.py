import random
import netifaces
import socket
import binascii
import requests

from app.models import *
from app.forms import *
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView


import plotly.plotly as py
import plotly.offline as opy
import plotly.graph_objs as go
import pandas as pd


def add_connection(source_ip, dest_ip, type_conn, timestamp):
    '''
    add a new connection of type = TCP/UDP/ARP/DNS whatever
    '''
    try:

        c = Connection(source_address=source_ip)
        c.destination_address = dest_ip
        c.type_of_connection = type_conn
        c.visited = timestamp
        c.save()

        t = Thing.objects.get(ip_address=source_ip)
        t.connections.add(c)
        t.save()

        c = t.connections
#        print "connection added to DB of", ip
    except Exception:
        #        print "No owner wrt server!"
        pass


def add_urls(source_ip, dest_url, timestamp):
    '''
    add a new URL
    '''
    try:

        u = URL(name=dest_url)
        u.visited = timestamp
        u.save()

        t = Thing.objects.get(ip_address=source_ip)
        t.urls_visited.add(u)
        t.save()

        # print "URL added to DB of", ip
    except Exception:
        # print "No owner wrt server!"
        pass


def get_urls_connections(source_ip):
    f = open('/var/log/snort/alert')
    for l in f:
        if source_ip in l and "TCP" in l:
            alert_tcp = l.split(" ")
            # get destination ip
            dest_ip_tcp = alert_tcp[11]
            # get timestamp
            timestamp_tcp = alert_tcp[0]
            # type of connection
            type_conn = alert_tcp[4]

            # add to the connections table of source ip
            add_connection(source_ip, dest_ip_tcp, type_conn, timestamp_tcp)
        if source_ip in l and "DNS" in l:
            # get destination URL
            alert_dns = l.split(" ")

            dest_ip_dns = alert_dns[11]

            dest_url = ""
            # convert IP to URL
            try:
                name, alias, addresslist = socket.gethostbyaddr(dest_ip_dns)
                dest_url = name
            except Exception:
                print "No hostname found!"

            # get timestamp
            timestamp_dns = alert_dns[0]

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
    # source_ip = request.get_host().split(":")[0]
    # print source_ip

    # try:
    #     t = Thing.objects.get(ip_address=source_ip)
    #     t.admin_or_not = True
    #     t.save()
    # except Exception:
    #     print "No owner wrt server!"

    '''
    # detect new devices
    # check them in DB
    # if not present, add device in DB
    '''
    try:
        f = open("../../ap.log")
        for line in f:
            if ("AP-STA-CONNECTED" in line):
                spl = line.split()
                mac = spl[3].strip()
                if not Thing.objects.filter(mac_address=mac):
                    print "New device found!"
                    # add a new device, not already present
                    unique_name = "IoT Device"
                    ip = fetch_ip(mac)
                    thing = Thing(name=unique_name, mac_address=mac,
                                  ip_address=ip, vendor=fetch_vendor(mac))
                    thing.save()
                    get_urls_connections(ip)
                else:
                    print "Device already in the DB!"
    except Exception:
        print "Some error"
    ts = Thing.objects.all()
    return render(request, 'app/things.html', {'things': ts})


def thing(request, thingid):
    t = Thing.objects.get(pk=thingid)
    if request.method == 'POST':
        form = ThingForm(request.POST, request.FILES, instance=t)
        if form.is_valid():
            thing = form.save(commit=False)
            thing.save()
            messages.success(
                request, 'Your details were saved. Welcome!')
            return HttpResponseRedirect('/')
        else:
            context = {'form': form, 't': t}
            return render(request, 'app/thing.html', context)
    elif request.method == 'GET':
        form = ThingForm(instance=t)
        context = {'form': form, 't': t}
        return render(request, 'app/thing.html', context)

    return HttpResponseRedirect('/')


def addpermission(request):
    """Open a new Project from admin side."""

    if request.method == 'POST':
        form = PermissionForm(request.POST, request.FILES)
        if form.is_valid():
            tosaveurl = form.save(commit=False)
            tosaveurl.createdon = timezone.now()
            tosaveurl.save()
            return HttpResponseRedirect('/')
        else:
            context = {'form': form}
            return render(request, 'app/addpermission.html', context)
    else:
        form = PermissionForm()
        context = {'form': form}
        return render(request, 'app/addpermission.html', context)


def addowner(request):
    """Open a new Project from admin side."""

    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            tosaveurl = form.save(commit=False)
            tosaveurl.createdon = timezone.now()
            tosaveurl.save()
            return HttpResponseRedirect('/')
        else:
            context = {'form': form}
            return render(request, 'app/addowner.html', context)
    else:
        form = OwnerForm()
        context = {'form': form}
        return render(request, 'app/addowner.html', context)


def addroom(request):
    """Open a new Project from admin side."""

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            tosaveurl = form.save(commit=False)
            tosaveurl.createdon = timezone.now()
            tosaveurl.save()
            return HttpResponseRedirect('/')
        else:
            context = {'form': form}
            return render(request, 'app/addroom.html', context)
    else:
        form = RoomForm()
        context = {'form': form}
        return render(request, 'app/addroom.html', context)


def addtype(request):
    """Open a new Project from admin side."""

    if request.method == 'POST':
        form = TypeForm(request.POST, request.FILES)
        if form.is_valid():
            tosaveurl = form.save(commit=False)
            tosaveurl.createdon = timezone.now()
            tosaveurl.save()
            return HttpResponseRedirect('/')
        else:
            context = {'form': form}
            return render(request, 'app/addtype.html', context)
    else:
        form = TypeForm()
        context = {'form': form}
        return render(request, 'app/addtype.html', context)


class Graph(TemplateView):
    template_name = 'app/stats.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        x = [-2, 0, 4, 6, 7]
        y = [q**2 - q + 3 for q in x]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
                            mode="lines", name='1st Trace')

        data = go.Data([trace1])
        layout = go.Layout(title="Meine Daten", xaxis={
                           'title': 'x1'}, yaxis={'title': 'x2'})
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div

        return context


def draw():

    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")

    trace_high = go.Scatter(
        x=df.Date,
        y=df['AAPL.High'],
        name="AAPL High",
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_low = go.Scatter(
        x=df.Date,
        y=df['AAPL.Low'],
        name="AAPL Low",
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    data = [trace_high, trace_low]

    layout = dict(
        title="Manually Set Date Range",
        xaxis=dict(
            range=['2016-07-01', '2016-12-31'])
    )

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename="Manually Set Range")
