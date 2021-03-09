from django.shortcuts import render

#imports for login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from ASISupport_app.models import Case, Visit, Employee, Customer, CaseEquipment, Equipment
# from django.views.generic import (TemplateView)
# from ASISupport_app.models import Case, Visit

# Create your views here.
def login_view(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username, password = password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('dashboard'))
			else:
				return HttpResponse('Account not active')
		else:
			print('Username: {}'.format(username))
			return HttpResponse('Invalid credentials')
	else:
		return render(request, 'ASISupport_app/login.html', {})

def dashboard_view(request):
	cases = Case.objects.all()
	return render(request, 'ASISupport_app/dashboard.html', locals())

def new_case_view(request):
	state = 'new'
	types = Case.TYPES
	statuses = Case.STATUSES
	employees = Employee.objects.all()
	customers = Customer.objects.all()
	return render(request, 'ASISupport_app/case.html', locals())

def case_view(request, id):
	state = 'view'
	case = Case.objects.get(case_num=id)
	visits = Visit.objects.filter(case_num=id)

	case_equipment_lst = CaseEquipment.objects.filter(case_num=id)
	equip_lst = [ce.equip_sn for ce in case_equipment_lst]
	equipment = Equipment.objects.filter(equip_sn__in=equip_lst)
	
	statuses = Case.STATUSES
	return render(request, 'ASISupport_app/case.html', locals())

def new_visit_view(request):
	state = 'new'
	return render(request, 'ASISupport_app/visit.html', locals())

def visit_view(request, id):
	state = 'view'
	visit = Visit.objects.get(visit_num=id)
	return render(request, 'ASISupport_app/visit.html', locals())