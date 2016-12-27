from django.shortcuts import render
from .models import Employee, Customer, Part, Order, Quantity
from .forms import EmployeeForm, CustomerForm, PartForm, OrderForm, OrderPartQuantityForm 
from django.http import HttpResponseRedirect
from itertools import *
from django.db import connection

# select * from app_customer where lname="Gupta"
# select * from 
# Create your views here.
def index(request):
	customers = Customer.objects.all()
	employees = Employee.objects.all()
	orders = Order.objects.all()
	
	parts_for_order=[]
	for x in orders:
		parts_for_order+=x.quantity_set.all()
	
	parts = Part.objects.all()
	context = {'employees':employees, 'customers':customers, 'orders':orders, 'parts':parts, 'parts_for_order':parts_for_order}
	return render(request, 'app/index.html', context)


def newcustomer(request):
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = CustomerForm()
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')


def customer_edit(request, cid):
	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=Customer.objects.get(pk=cid))
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = CustomerForm(instance=Customer.objects.get(pk=cid))
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')


def customer_delete(request, cid):
	Customer.objects.get(pk=cid).delete()
	return HttpResponseRedirect('/')


def newemployee(request):
	if request.method == 'POST':
		form = EmployeeForm(request.POST)
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = EmployeeForm()
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def employee_edit(request, eid):
	if request.method == 'POST':
		form = EmployeeForm(request.POST, instance=Employee.objects.get(pk=eid))
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = EmployeeForm(instance=Employee.objects.get(pk=eid))
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def employee_delete(request, eid):
	Employee.objects.get(pk=eid).delete()
	return HttpResponseRedirect('/')


def neworder(request):
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = OrderForm()
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def order_edit(request, oid):	
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=Order.objects.get(pk=oid))
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = OrderForm(instance=Order.objects.get(pk=oid))
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def order_delete(request, oid):
	Order.objects.get(pk=oid).delete()
	return HttpResponseRedirect('/')


def newpart(request):
	if request.method == 'POST':
		form = PartForm(request.POST)
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = PartForm()
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def part_edit(request, pid):	
	if request.method == 'POST':
		form = PartForm(request.POST, instance=Part.objects.get(pk=pid))
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = PartForm(instance=Part.objects.get(pk=pid))
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def part_delete(request, pid):
	Part.objects.get(pk=pid).delete()
	return HttpResponseRedirect('/')

def query(request):
	sql = request.read().replace("%22", '\"').replace("%3D", "=").replace("+", " ")[4:]
	cursor = connection.cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	return render(request, 'app/query_results.html', {'results':results,'sql':sql})

def order_per_part(request):
	if request.method == 'POST':
		form = OrderPartQuantityForm(request.POST)
		if form.is_valid():
			usr = form.save(commit=False)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = OrderPartQuantityForm()
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def order_per_part_update(request, opid):	
	if request.method == 'POST':
		form = OrderPartQuantityForm(request.POST, instance=Quantity.objects.get(pk=opid))
		if form.is_valid():
			usr = form.save(commit=False)
			order_no = usr.order_no
			Order.objects.filter(id=order_no).quantity_set.add(usr)
			usr.save()
			return HttpResponseRedirect('/')
	elif request.method == 'GET':
			studentform = OrderPartQuantityForm(instance=Quantity.objects.get(pk=opid))
			context = {'form': studentform}
			return render(request, 'app/thing.html', context)
	return HttpResponseRedirect('/')

def order_per_part_delete(request, opid):
	Quantity.objects.get(pk=opid).delete()
	return HttpResponseRedirect('/')