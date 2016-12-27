from django.db import models

# Create your models here.
class Employee(models.Model):
#        employee_no = models.IntegerField(primary_key=True)
	fname = models.CharField(max_length=50, blank= False)
	lname = models.CharField(max_length = 50, blank= False)
	zip_code = models.IntegerField(null = True)

	def __str__(self):
		return self.fname + ' ' + self.lname 


class Customer(models.Model):
#    customer_no = models.IntegerField(primary_key=True)
	fname = models.CharField(max_length=50, blank= False)
	lname = models.CharField(max_length = 50, blank= False)
	zip_code = models.IntegerField(null = True)

	def __str__(self):
		return self.fname + ' ' + self.lname


class Part(models.Model):
#    part_no = models.IntegerField(primary_key=True)
	pname = models.CharField(max_length = 20,blank= False)
	price = models.IntegerField(blank= False)
	max_quantity = models.IntegerField(blank= False) #This is the stock quantity for every part

	def __str__(self):
		return self.pname + ' ' + str(self.price) + ' ' + str(self.max_quantity)   


class Order(models.Model):
#    order_no = models.IntegerField(primary_key = True)
	employee_id = models.ForeignKey(Employee)
	customer_id = models.ForeignKey(Customer)
	recv_date = models.DateTimeField(blank = False)
	ship_date = models.DateTimeField(blank = False)

	def __str__(self):
		return str(self.id) + ' ' + self.employee_id.fname + ' ' +  self.customer_id.fname + ' ' + str(self.recv_date) + str(self.ship_date) 


class Quantity(models.Model):
	order_no = models.ForeignKey(Order)
	part_quantity = models.IntegerField(blank= False)
	part_no = models.ForeignKey(Part)

	def __str__(self):
		return str(self.part_quantity) + str(self.part_no)  
