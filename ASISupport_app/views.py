from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from ASISupport_app.models import Case, Visit, Employee, Customer, CaseEquipment, Equipment, VisitParts, Parts
  


def logout_view(request):
    return auth_views.logout(request)

@login_required(login_url='/accounts/login/')
def dashboard_view(request):
	cases = Case.objects.all()
	return render(request, 'ASISupport_app/dashboard.html', locals())

@login_required(login_url='/accounts/login/')
def new_case_view(request):

	if request.method == 'POST':
		cases = Case.objects.all()
		case_num_lst = [int(case.case_num[1:]) for case in cases]
		max_case_num = max(case_num_lst)


		req_case_num 			= 'C'+str(max_case_num+1).zfill(6)
		req_case_type 			= request.POST.get('type')
		req_status 				= request.POST.get('status')
		# req_create_date 		= 
		req_target_date 		= request.POST.get('projected_date')
		req_actual_date 		= request.POST.get('actual_date')
		req_case_manager 		= request.POST.get('case_manager')
		req_machine_down 		= request.POST.get('machine_down')
		req_customer 			= request.POST.get('customer')
		req_customer_contact 	= request.POST.get('customer_contact')
		req_case_description 	= request.POST.get('case_description')
		# req_cancellation_reason = request.POST.get('status')
		# req_on_hold_reason 		= request.POST.get('status')
		
		case_data = Case(case_num=req_case_num, 
						case_type=req_case_type,
						status=req_status,
						# create_date=req_create_date,
						target_date=req_target_date,
						actual_date=req_actual_date,
						case_manager=req_case_manager,
						machine_down=req_machine_down,
						customer=req_customer,
						customer_contact=req_customer_contact,
						case_description=req_case_description
						# cancellation_reason=req_cancellation_reason,
						# on_hold_reason=req_on_hold_reason
						)		
		case_data.save()
		return redirect('case_view', req_case_num)

	state = 'new'
	types = Case.TYPES
	statuses = Case.STATUSES
	employees = Employee.objects.all()
	customers = Customer.objects.all()

	return render(request, 'ASISupport_app/case.html', locals())


@login_required(login_url='/accounts/login/')
def case_view(request, id):
	state = 'view'
	case = Case.objects.get(case_num=id)
	visits = Visit.objects.filter(case_num=id)

	case_equipment_lst = CaseEquipment.objects.filter(case_num=id)
	equip_lst = [ce.equip_sn for ce in case_equipment_lst]
	equipment = Equipment.objects.filter(equip_sn__in=equip_lst)

	statuses = Case.STATUSES
	return render(request, 'ASISupport_app/case.html', locals())

@login_required(login_url='/accounts/login/')
def new_visit_view(request):
	state = 'new'
	employees = Employee.objects.all()
	return render(request, 'ASISupport_app/visit.html', locals())

@login_required(login_url='/accounts/login/')
def visit_view(request, id):
	state = 'view'
	visit = Visit.objects.get(visit_num=id)
	visit.sum_visit_hours()
	case = Case.objects.get(case_num=visit.case_num)

	visit_parts_lst = VisitParts.objects.filter(visit_num=id)
	part_pn_lst = [vp.part_pn for vp in visit_parts_lst]
	parts = Parts.objects.filter(part_pn__in=part_pn_lst)
	part_description_dict = {VisitParts.objects.get(visit_num=id, part_pn=part.part_pn):part.part_description for part in parts}

	return render(request, 'ASISupport_app/visit.html', locals())
