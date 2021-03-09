from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import datetime


class Employee(models.Model):
	employee_id = models.CharField(max_length=100, primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=100)
	email = models.EmailField(max_length=254, unique = True)
	password = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Customer(models.Model):
	customer_name = models.CharField(max_length=100, primary_key=True)

	def __str__(self):
		return self.customer_name


class Case(models.Model):
	TYPES = (
		('Support', 'Support'),
		('Training', 'Training'),
		('Maintenance', 'Maintenance'),
		('installation','Installation')
	)
	STATUSES = (
		('Open', 'Open'),
		('Resolved', 'Resolved'),
		('Closed', 'Closed'),
		('On Hold','On Hold'),
		('Cancelled','Cancelled')
	)
	case_num = models.CharField(max_length=100, primary_key=True)
	case_type = models.CharField(max_length=100, choices=TYPES)
	status = models.CharField(max_length=100, choices=STATUSES)
	create_date = models.DateTimeField(default=timezone.now)
	target_date = models.DateField()
	actual_date = models.DateField(blank=True, null=True)
	case_manager = models.ForeignKey(Employee, on_delete=models.CASCADE)
	machine_down =  models.BooleanField(default=False)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	customer_contact = models.CharField(max_length=100)
	case_description = models.TextField()
	cancellation_reason = models.TextField(blank=True, null=True)
	
	def close_case(self):
		self.actual_date = timezone.now
		self.save()

	def __str__(self):
		return self.case_num


class Visit(models.Model):
	visit_num = models.CharField(max_length=100, primary_key=True)
	case_num = models.ForeignKey(Case, on_delete=models.CASCADE)
	visit_date = models.DateTimeField(default = timezone.now)
	engineer = models.ForeignKey(Employee, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)#!!!must be same customer as in case
	customer_contact = models.CharField(max_length=100)#!!!must be same customer as in case
	remote =  models.BooleanField(default=False)
	visit_start = models.TimeField() 
	visit_end = models.TimeField() 
	# visit_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
	travel_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
	num_of_engineers = models.IntegerField(blank=True, null=True)
	visit_summary = models.TextField()

	def sum_visit_hours(self):
		self.visit_hours = (datetime.strptime(str(self.visit_end), '%H:%M:%S') - datetime.strptime(str(self.visit_start), '%H:%M:%S')).seconds / 3600

	def __str__(self):
		return self.visit_num


class Equipment(models.Model):
	equip_sn = models.CharField(max_length=100, primary_key=True)
	equip_pn = models.CharField(max_length=100)
	equip_description = models.TextField()
	installation_date = models.DateTimeField()
	warranty = models.DecimalField(max_digits=20, decimal_places=2) #in months

	def __str__(self):
		return self.equip_sn


class Parts(models.Model):
	part_pn = models.CharField(max_length=100, primary_key=True)
	part_description = models.TextField()

	def __str__(self):
		return self.part_pn


class CaseEquipment(models.Model):
	case_num = models.ForeignKey(Case, on_delete=models.CASCADE)
	equip_sn = models.ForeignKey(Equipment, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.case_num} {self.equip_sn}'


class VisitParts(models.Model):
	visit_num = models.ForeignKey(Visit, on_delete=models.CASCADE)
	part_pn = models.ForeignKey(Parts, on_delete=models.CASCADE)
	qty = models.IntegerField(blank=True, null=True)
	charge = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.visit_num} {self.part_pn}'

