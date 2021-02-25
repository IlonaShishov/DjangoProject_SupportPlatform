from django.db import models
from django.utils import timezone
# from django.core.urlresolvers import reverse
from django.urls import reverse
# Create your models here.

# class Case(models.Model):
# 	TYPES = (
# 		('Support', 'Support'),
# 		('Training', 'Training'),
# 		('Maintenance', 'Maintenance'),
# 		('installation','Installation')
# 	)
# 	STATUSES = (
# 		('Open', 'Open'),
# 		('Resolved', 'Resolved'),
# 		('Closed', 'Closed'),
# 		('On Hold','On Hold'),
# 		('Cancelled','Cancelled')
# 	)
# 	case_num = models.CharField(max_length=100, primary_key=True)
# 	case_type = models.CharField(max_length=100, choices=TYPES)
# 	status = models.CharField(max_length=100, choices=STATUSES)
# 	target_date = models.DateTimeField()
# 	completion_date = models.DateTimeField()
# 	create_date = models.DateTimeField(default = timezone.now())
# 	case_manager = models.ForeignKey(Users, on_delete=models.CASCADE)
# 	machine_down =  models.BooleanField(default=False)
# 	customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
# 	customer_contact = models.CharField(max_length=100)
# 	description = models.TextField()

# 	def closeCase(self):
# 		self.completion_date = timezone.now()
# 		self.save()


# class Visit(models.Model):
# 	visit_num = models.CharField(max_length=100, primary_key=True)
# 	case_num = models.ForeignKey(Case, on_delete=models.CASCADE)
# 	visit_date = models.DateTimeField(default = timezone.now())
# 	engineer = models.ForeignKey(Users, on_delete=models.CASCADE)
# 	customer = models.ForeignKey(Customers, on_delete=models.CASCADE)#!!!must be same customer as in case
# 	customer_contact = models.CharField(max_length=100)#!!!must be same customer as in case
# 	remote =  models.BooleanField(default=False)
# 	visit_start = models.TimeField() 
# 	visit_end = models.TimeField() 
# 	visit_hours = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
# 	travel_hours = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
# 	num_of_engineers = models.IntegerField()
# 	visit_summary = models.TextField()

# 	def totVisitHours(self):
# 		self.visit_hours = (self.visit_end - self.visit_start).seconds / 60
