from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from ASISupport_app.models import Case, Visit, Employee, Customer, CaseEquipment, Equipment, VisitParts, Parts
  


def logout_view(request):
    return auth_views.logout(request)

@login_required(login_url='/accounts/login/')
def dashboard_view(request):
	search_case_value = request.POST.get('search_case')

	if request.method == 'POST' and 'search_case_btn' in request.POST:
		if search_case_value:
			cases = Case.objects.filter(case_num__contains=search_case_value, status='Open')
			return render(request, 'ASISupport_app/dashboard.html', locals())

	cases = Case.objects.filter(status='Open')
	return render(request, 'ASISupport_app/dashboard.html', locals())

@login_required(login_url='/accounts/login/')
def new_case_view(request):
	state = 'new'

	if request.method == 'POST' and 'save_btn' in request.POST:
		
		''' save case data '''
		cases = Case.objects.all()
		case_num_lst = [int(case.case_num[1:]) for case in cases]
		max_case_num = max(case_num_lst)

		req_case_num 			= 'C'+str(max_case_num+1).zfill(6)
		req_case_type 			= request.POST.get('type')
		req_status 				= request.POST.get('status')
		req_target_date 		= datetime.strptime(request.POST.get('projected_date'),'%Y-%m-%d')

		req_actual_date 		= request.POST.get('actual_date')
		if req_actual_date:
			req_actual_date = datetime.strptime(request.POST.get('actual_date'),'%Y-%m-%d')
		else:
			req_actual_date = None
		
		req_case_manager 		= Employee.objects.filter(first_name=request.POST.get('case_manager').split()[0], last_name=request.POST.get('case_manager').split()[1])[0]
		
		req_machine_down		= request.POST.get('machine_down')
		if req_machine_down == 'on':
			req_machine_down = True
		else:
			req_machine_down = False
		
		req_customer 			= Customer.objects.get(customer_name=request.POST.get('customer'))
		req_customer_contact 	= request.POST.get('customer_contact')
		req_case_description 	= request.POST.get('case_description')
		req_on_hold_reason = ''
		req_cancellation_reason = ''
		if req_status == 'On Hold':
			req_on_hold_reason = request.POST.get('on_hold_reason')
		elif req_status == 'Cancelled':
			req_cancellation_reason = request.POST.get('cancellation_reason')
		else:
			pass
			

		case_data = Case(case_num=req_case_num, 
						case_type=req_case_type,
						status=req_status,
						target_date=req_target_date,
						actual_date=req_actual_date,
						case_manager=req_case_manager,
						machine_down=req_machine_down,
						customer=req_customer,
						customer_contact=req_customer_contact,
						case_description=req_case_description,
						cancellation_reason=req_cancellation_reason,
						on_hold_reason=req_on_hold_reason
						)		
		case_data.save()

		''' save equipment data''' 
		equip_sn_lst = request.POST.getlist('serial_number')
		equip_sn_lst = filter(lambda x: x != "", equip_sn_lst)

		for sn in equip_sn_lst:
			equip_data = CaseEquipment(case_num=Case.objects.get(case_num=req_case_num),
									equip_sn=Equipment.objects.get(equip_sn=sn),
									)
			equip_data.save()

		return redirect('ASISupport_app:view_case', id=req_case_num)

	if request.method == 'POST' and 'cancel_btn' in request.POST:
		return redirect('ASISupport_app:dashboard')

	types = Case.TYPES
	statuses = Case.STATUSES
	employees = Employee.objects.all()
	customers = Customer.objects.all()
	equipment = Equipment.objects.all()
	equip_sn_lst = [equip.equip_sn for equip in equipment]
	equip_pn_lst = [equip.equip_pn for equip in equipment]
	equip_description_lst = [equip.equip_description for equip in equipment]
	equip_property_lst = [{'sn':equip.equip_sn,
						 'pn':equip.equip_pn, 
						 'description':equip.equip_description, 
						 'date':str(datetime.strptime(str(equip.installation_date)[:19],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')), 
						 'warranty':str(equip.warranty)} for equip in equipment]

	return render(request, 'ASISupport_app/case.html', locals())

@login_required(login_url='/accounts/login/')
def case_view(request, id):
	state = 'view'

	if request.method == 'POST' and 'back_btn' in request.POST:
		return redirect('ASISupport_app:dashboard')

	case = Case.objects.get(case_num=id)
	visits = Visit.objects.filter(case_num=id)

	case_equipment_lst = CaseEquipment.objects.filter(case_num=id)
	equip_lst = [ce.equip_sn for ce in case_equipment_lst]
	equipment = Equipment.objects.filter(equip_sn__in=equip_lst)

	statuses = Case.STATUSES
	return render(request, 'ASISupport_app/case.html', locals())

@login_required(login_url='/accounts/login/')
def new_visit_view(request, id):
	state = 'new'

	case = Case.objects.get(case_num=id)

	if request.method == 'POST' and 'save_btn' in request.POST:

		''' save visit data '''
		visits = Visit.objects.all()
		visit_num_lst = [int(visit.visit_num[1:]) for visit in visits]
		max_visit_num = max(visit_num_lst)

		req_visit_num 			= 'V'+str(max_visit_num+1).zfill(6)
		req_case_num			= case
		req_visit_date 			= datetime.strptime(request.POST.get('visit_date'),'%Y-%m-%d')
		req_engineer 			= Employee.objects.filter(first_name=request.POST.get('engineer').split()[0], last_name=request.POST.get('engineer').split()[1])[0]
		req_customer 			= case.customer
		req_customer_contact 	= request.POST.get('customer_contact')
		req_remote		= request.POST.get('remote')
		if req_remote == 'on':
			req_remote = True
		else:
			req_remote = False
		req_visit_start 		= request.POST.get('visit_start') + ':00'
		req_visit_end 			= request.POST.get('visit_end') + ':00'
		req_travel_hours 		= request.POST.get('travel_hours')
		req_num_of_engineers 	= request.POST.get('num_of_engineers')
		req_visit_summary 		= request.POST.get('visit_summary')

		visit_data = Visit(visit_num=req_visit_num, 
						case_num=req_case_num,
						visit_date=req_visit_date,
						engineer=req_engineer,
						customer=req_customer,
						customer_contact=req_customer_contact,
						remote=req_remote,
						visit_start=req_visit_start,
						visit_end=req_visit_end,
						travel_hours=req_travel_hours,
						num_of_engineers=req_num_of_engineers,
						visit_summary=req_visit_summary
						)		
		visit_data.sum_visit_hours()
		visit_data.save()

		''' save part data '''
		part_pn_lst = request.POST.getlist('part_num')
		part_description_lst = request.POST.getlist('part_description')		
		part_qty_lst = request.POST.getlist('qty')
		part_charge_lst = request.POST.getlist('charge')
		part_tbl = pd.DataFrame({'part_pn':part_pn_lst, 'part_description':part_description_lst, 'part_qty':part_qty_lst, 'part_charge':part_charge_lst})
		d = {'1': True, '0': False}
		part_tbl['part_charge'] = part_tbl['part_charge'].map(d)
		# if part_tbl.all(axis='columns').all():
		for index, row in part_tbl.iterrows():
			part_data = VisitParts(visit_num=Visit.objects.get(visit_num=req_visit_num),
								part_pn=Parts.objects.get(part_pn=row['part_pn']),
								qty=row['part_qty'],
								charge=row['part_charge']
								)
			part_data.save()

		return redirect('ASISupport_app:view_visit', id=req_visit_num)

	if request.method == 'POST' and 'cancel_btn' in request.POST:
		return redirect('ASISupport_app:view_case', id=id)

	parts = Parts.objects.all()
	parts_dict = {part.part_pn:part.part_description for part in parts}
	employees = Employee.objects.all()
	return render(request, 'ASISupport_app/visit.html', locals())

@login_required(login_url='/accounts/login/')
def visit_view(request, id):
	state = 'view'

	visit = Visit.objects.get(visit_num=id)

	if request.method == 'POST' and 'back_btn' in request.POST:
		return redirect('ASISupport_app:view_case', id=visit.case_num)

	visit.sum_visit_hours()
	case = Case.objects.get(case_num=visit.case_num)

	visit_parts_lst = VisitParts.objects.filter(visit_num=id)
	part_pn_lst = [vp.part_pn for vp in visit_parts_lst]
	parts = Parts.objects.filter(part_pn__in=part_pn_lst)
	part_description_dict = {VisitParts.objects.get(visit_num=id, part_pn=part.part_pn):part.part_description for part in parts}

	return render(request, 'ASISupport_app/visit.html', locals())

@login_required(login_url='/accounts/login/')
def report_view(request):

	if request.method == 'POST' and 'back_btn' in request.POST:
		return redirect('ASISupport_app:dashboard')

	if request.method == 'POST' and 'case_report_search_btn' in request.POST:
		search_case 			= request.POST.get('search_case_case')
		search_from_date 		= request.POST.get('search_case_from_date')
		search_to_date 			= request.POST.get('search_case_to_date')
		search_type 			= request.POST.get('search_case_type')
		search_status 			= request.POST.get('search_case_status')
		search_case_manager 	= request.POST.get('search_case_case_manager')
		search_customer 		= request.POST.get('search_case_customer')
		search_machine_down 	= request.POST.get('search_case_machine_down')

		cases = Case.objects.all()

		if search_case:
			cases = cases.filter(case_num=search_case)
		if search_from_date:
			cases = cases.filter(create_date__gte=search_from_date)
		if search_to_date:
			cases = cases.filter(create_date__lte=search_to_date)
		if search_type:
			cases = cases.filter(case_type=search_type)
		if search_status:
			cases = cases.filter(status=search_status)
		if search_case_manager:
			cases = cases.filter(case_manager=Employee.objects.filter(first_name=search_case_manager.split()[0], last_name=search_case_manager.split()[1])[0])
		if search_customer:
			cases = cases.filter(customer=Customer.objects.get(customer_name=search_customer))
		if search_machine_down:
			cases = cases.filter(machine_down=True if search_machine_down == 'True' else False)

	if request.method == 'POST' and 'case_report_export_to_excel_btn' in request.POST:
		# cases = cases.fetch(3)
		pass
		

	types = Case.TYPES
	statuses = Case.STATUSES
	employees = Employee.objects.all()
	customers = Customer.objects.all()
		
	return render(request, 'ASISupport_app/report.html', locals())