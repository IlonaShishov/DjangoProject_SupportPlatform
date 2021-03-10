from django.contrib import admin
from ASISupport_app.models import Employee, Customer, Case, Visit, Equipment, Parts, CaseEquipment, VisitParts
# Register your models here.


admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Case)
admin.site.register(Visit)
admin.site.register(Equipment)
admin.site.register(Parts)
admin.site.register(CaseEquipment)
admin.site.register(VisitParts)