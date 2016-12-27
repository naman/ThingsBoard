#all forms here
from django.forms import ModelForm
from app.models import Employee, Customer, Order, Quantity, Part

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['fname', 'lname', 'zip_code']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['fname', 'lname' , 'zip_code']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['recv_date', 'ship_date', 'employee_id', 'customer_id']


class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = [ 'pname', 'price', 'max_quantity']


class OrderPartQuantityForm(ModelForm):
	class Meta:
		model = Quantity
		fields = ['order_no', 'part_no', 'part_quantity']
