from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime
import pandas as pd
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
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

	''' roles '''
	groups = list(request.user.groups.values_list('name',flat = True))
 	
	permit_new_case = ('Manager' in groups) or ('Support' in groups)

	return render(request, 'ASISupport_app/dashboard.html', locals())

@login_required(login_url='/accounts/login/')
def new_case_view(request):
	state = 'new'

	''' roles '''
	groups = list(request.user.groups.values_list('name',flat = True))

	''' status list by roles '''
	statuses = []
	if ('Support' in groups ):
		statuses.extend((
						('Open', 'Open'),
						('Resolved', 'Resolved'),
						('On Hold','On Hold'),
						('Cancelled','Cancelled')
						))

	if ('Secretary' in groups):
		statuses.extend((
						('Closed', 'Closed'),
						))

	if ('Manager' in groups):
		statuses.extend(Case.STATUSES)

	statuses = list(set(statuses))


	types = Case.TYPES
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


	if request.method == 'POST' and 'save_btn' in request.POST:
		
		try:

			''' get case data '''

			''' init case number '''
			cases = Case.objects.all()
			case_num_lst = [int(case.case_num[1:]) for case in cases]
			max_case_num = max(case_num_lst)
			req_case_num 			= 'C'+str(max_case_num+1).zfill(6)

			''' get case type '''
			req_case_type 			= request.POST.get('type')
			types_val = (tup[0] for tup in types)
			if req_case_type not in types_val:
				messages.error(request, f'Type field error: <{req_case_type}> is an invalid case type')

			''' get case status '''
			req_status 				= request.POST.get('status')
			statuses_val = (tup[0] for tup in statuses)
			if req_status not in statuses_val:
				messages.error(request, f'Status field error: <{req_status}> is an invalid case status')

			''' get target date '''
			try:
				req_target_date 		= datetime.strptime(request.POST.get('projected_date'),'%Y-%m-%d')
			except Exception as err:
				messages.error(request, f'Projected completion date field error: {err}')

			''' get actual date '''
			try:
				req_actual_date 		= request.POST.get('actual_date')
				if req_actual_date:
					req_actual_date = datetime.strptime(request.POST.get('actual_date'),'%Y-%m-%d')
				else:
					req_actual_date = None
			except Exception as err:
				messages.error(request, f'Actual completion date field error: {err}')

			''' get case manager '''
			try:
				req_case_manager 		= Employee.objects.get(employee_id=request.POST.get('case_manager').split()[2])
			except Exception as err:
				messages.error(request, 'Case manager field error: Invalid case manager')

			''' get machine down state '''
			try:
				req_machine_down		= request.POST.get('machine_down')
				if req_machine_down == 'on':
					req_machine_down = True
				else:
					req_machine_down = False
			except Exception as err:
				messages.error(request, f'Machine down field error: {err}')
			
			''' get customer '''
			try:
				req_customer 			= Customer.objects.get(customer_name=request.POST.get('customer'))
			except Exception as err:
				messages.error(request, 'Customer field error: Invalid customer')

			''' get cutomer contact '''
			req_customer_contact 	= request.POST.get('customer_contact')
			if not req_customer_contact:
				messages.error(request, 'Customer contact field error: Customer contact is required')


			''' get description '''
			req_case_description 	= request.POST.get('case_description')
			if not req_case_description:
				messages.error(request, 'Case description field error: Case description is required')


			req_on_hold_reason = ''
			req_cancellation_reason = ''

			if req_status == 'On Hold':
				''' get on hold reason '''
				req_on_hold_reason = request.POST.get('on_hold_reason')
				if not req_on_hold_reason:
					messages.error(request, 'On Hold Reason field error: On Hold reason is required')


			elif req_status == 'Cancelled':
				''' get Cancellation reason '''
				req_cancellation_reason = request.POST.get('cancellation_reason')
				if not req_cancellation_reason:
					messages.error(request, 'Cancellation Reason field error: Cancellation reason is required')

			else:
				pass
				

			''' get equipment data''' 
			add_equip_sn_lst = request.POST.getlist('serial_number')
			add_equip_sn_lst = list(set(list(filter(lambda x: x != "", add_equip_sn_lst))))
			if not all(sn in equip_sn_lst  for sn in add_equip_sn_lst):
				messages.error(request, 'Equipment field error: Equipment list contains equipment not found in database')


			''' display validation errors '''
			message_list = messages.get_messages(request)
			if message_list:
				return redirect('ASISupport_app:new_case')

			
			''' save case data '''
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

			if (case_data.status == 'Closed' or case_data.status == 'Resolved') and case_data.actual_date == None:
				case_data.close_case()
			
			case_data.save()


			''' save equipment data'''
			for sn in add_equip_sn_lst:
				equip_data = CaseEquipment(case_num=Case.objects.get(case_num=req_case_num),
										equip_sn=Equipment.objects.get(equip_sn=sn),
										)
				equip_data.save()

			messages.success(request, 'Case created successfully')
			return redirect('ASISupport_app:view_case', id=req_case_num)



		except Exception as err:
			''' display errors '''
			if Case.objects.filter(case_num=req_case_num):
				messages.warning(request, f'Equipment field error: {err}')
				return redirect('ASISupport_app:view_case', id=req_case_num)

			messages.error(request, err)
			return redirect('ASISupport_app:new_case')
			

	if request.method == 'POST' and 'cancel_btn' in request.POST:
		return redirect('ASISupport_app:dashboard')

	
	return render(request, 'ASISupport_app/case.html', locals())

@login_required(login_url='/accounts/login/')
def case_view(request, id):
	state = 'view'

	if request.method == 'POST' and 'back_btn' in request.POST:
		return redirect('ASISupport_app:dashboard')

	case = Case.objects.get(case_num=id)
	visits = Visit.objects.filter(case_num=id)

	case_equipment = CaseEquipment.objects.filter(case_num=id)
	case_equipment_sn_lst = [ce.equip_sn for ce in case_equipment]
	filtered_case_equipment = Equipment.objects.filter(equip_sn__in=case_equipment_sn_lst)

	equipment = Equipment.objects.all()
	equip_sn_lst = [equip.equip_sn for equip in equipment]
	equip_pn_lst = [equip.equip_pn for equip in equipment]
	equip_description_lst = [equip.equip_description for equip in equipment]
	equip_property_lst = [{'sn':equip.equip_sn,
						 'pn':equip.equip_pn, 
						 'description':equip.equip_description, 
						 'date':str(datetime.strptime(str(equip.installation_date)[:19],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')), 
						 'warranty':str(equip.warranty)} for equip in equipment]

	types = Case.TYPES
	employees = Employee.objects.all()
	customers = Customer.objects.all()



	''' roles '''
	groups = list(request.user.groups.values_list('name',flat = True))

	''' status list by roles '''
	statuses = []
	if ('Support' in groups ):
		statuses.extend((
						('Open', 'Open'),
						('Resolved', 'Resolved'),
						('On Hold','On Hold'),
						('Cancelled','Cancelled')
						))

	if ('Secretary' in groups):
		statuses.extend((
						('Closed', 'Closed'),
						))

	if ('Manager' in groups):
		statuses.extend(Case.STATUSES)

	statuses = list(set(statuses))


	''' restrict permits '''
	permit_edit = ('Manager' in groups) or ('Support' in groups and case.status not in ['Resolved','Closed','Cancelled']) or ('Secretary' in groups and case.status in ['Resolved'])
	edit = False
	permit_type = False
	permit_status = False
	permit_target_date = False
	permit_actual_date = False
	permit_on_hold_reason = False
	permit_cancellation_reason = False
	permit_case_manager = False
	permit_machine_down = False
	permit_customer = False
	permit_customer_contact = False
	permit_description = False
	permit_equipment_delete = False
	permit_equipment_add = False


	if (request.method == 'POST' and 'edit_btn' in request.POST) or (request.method == 'POST' and 'save_btn' in request.POST):
		edit = True

		''' grant permissions per group '''
		if 'Manager' in groups:
			permit_type = True
			permit_status = True
			permit_target_date = True
			permit_actual_date = True
			permit_on_hold_reason = True
			permit_cancellation_reason = True
			permit_case_manager = True
			permit_machine_down = True
			permit_customer = True
			permit_customer_contact = True
			permit_description = True
			permit_equipment_delete = True
			permit_equipment_add = True

		if 'Support' in groups:
			permit_status = True
			permit_actual_date = True
			permit_on_hold_reason = True
			permit_cancellation_reason = True
			permit_machine_down = True
			permit_description = True
			permit_equipment = True
			permit_equipment_add = True

		if 'Secretary' in groups:
			permit_status = True

	
		if request.method == 'POST' and 'save_btn' in request.POST:

			try:


				''' get updated case data''' 
				updated = False

				''' update type '''
				if permit_type:
					upd_case_type = request.POST.get('type')
					if upd_case_type != case.case_type:
						types_val = (tup[0] for tup in types)
						if upd_case_type not in types_val:
							messages.error(request, f'Type field error: <{upd_case_type}> is an invalid case type')
						else:
							case.case_type = upd_case_type
							updated = True

				''' update status '''
				if permit_status:
					upd_case_status = request.POST.get('status')
					if upd_case_status != case.status:
						statuses_val = (tup[0] for tup in statuses)
						if upd_case_status not in statuses_val:
							messages.error(request, f'Status field error: <{upd_case_status}> is an invalid case status')
						else:
							if case.status == 'On Hold':
								case.on_hold_reason = ''
							if case.status == 'Cancelled':
								case.cancellation_reason = ''
							case.status = upd_case_status
							updated = True

				''' update target date '''
				if permit_target_date:
					try:
						upd_target_date = datetime.strptime(request.POST.get('projected_date'),'%Y-%m-%d')
						if upd_target_date != case.target_date:
							case.target_date = upd_target_date
							updated = True
					except Exception as err:
						messages.error(request, f'Projected completion date field error: {err}')

				''' update actual date '''
				if permit_actual_date:
					try:
						upd_actual_date = request.POST.get('actual_date')
						if upd_actual_date:
							upd_actual_date = datetime.strptime(upd_actual_date,'%Y-%m-%d')
						else:
							upd_actual_date = None

						if upd_actual_date != case.actual_date:
							case.actual_date = upd_actual_date
							updated = True
					except Exception as err:
							messages.error(request, f'Actual completion date field error: {err}')

				''' update on hold reason '''
				if permit_on_hold_reason and case.status == 'On Hold':
					upd_on_hold_reason = request.POST.get('on_hold_reason')
					if upd_on_hold_reason != case.on_hold_reason:
						if not upd_on_hold_reason:
							messages.error(request, 'On Hold Reason field error: On Hold reason is required')
						else:
							case.on_hold_reason = upd_on_hold_reason
							updated = True

				''' update cancellation reason '''
				if permit_cancellation_reason and case.status == 'Cancelled':
					upd_cancellation_reason = request.POST.get('cancellation_reason')
					if upd_cancellation_reason != case.cancellation_reason:
						if not upd_cancellation_reason:
							messages.error(request, 'Cancellation Reason field error: Cancellation reason is required')
						else:
							case.cancellation_reason = upd_cancellation_reason
							updated = True

				''' update case manager '''
				if permit_case_manager:
					try:
						upd_case_manager = Employee.objects.get(employee_id=request.POST.get('case_manager').split()[2])
						if upd_case_manager.employee_id != case.case_manager.employee_id:
							case.case_manager = upd_case_manager
							updated = True
					except Exception as err:
						messages.error(request, 'Case manager field error: Invalid case manager')

				''' update machine down '''
				if permit_machine_down:
					try:
						upd_machine_down = request.POST.get('machine_down')
						if upd_machine_down == 'on':
							upd_machine_down = True
						else:
							upd_machine_down = False

						if upd_machine_down != case.machine_down:
							case.machine_down = upd_machine_down
							updated = True
					except Exception as err:
						messages.error(request, f'Machine down field error: {err}')

				''' update customer (in case and in case visits ) '''
				if permit_customer:
					try:
						upd_customer = Customer.objects.get(customer_name=request.POST.get('customer'))
						if upd_customer.customer_name != case.customer.customer_name:
							case.customer = upd_customer
							for visit in visits:
								visit.customer = upd_customer
							updated = True
					except Exception as err:
						messages.error(request, 'Customer field error: Invalid customer')

				''' update customer contact '''
				if permit_customer_contact:
					upd_customer_contact = request.POST.get('customer_contact')
					if upd_customer_contact != case.customer_contact:
						if not upd_customer_contact:
							messages.error(request, 'Customer contact field error: Customer contact is required')
						else:
							case.customer_contact = upd_customer_contact
							updated = True

				''' update description '''
				if permit_description:
					upd_case_description = request.POST.get('case_description')
					if upd_case_description != case.case_description:
						if not upd_case_description:
							messages.error(request, 'Case description field error: Case description is required')
						else:
							case.case_description = upd_case_description
							updated = True

				''' get updated equipment data''' 
				upd_equip_sn_lst = request.POST.getlist('serial_number')
				upd_equip_sn_lst = list(set(list(filter(lambda x: x != "", upd_equip_sn_lst))))
				if not all(sn in equip_sn_lst  for sn in upd_equip_sn_lst):
					messages.error(request, 'Equipment field error: Equipment list contains equipment not found in database')


				''' check for existsing validation errors '''
				message_list = messages.get_messages(request)
				if message_list:
					return redirect('ASISupport_app:view_case', id=id)
				
				''' save updated case data '''
				if (case.status == 'Closed' or case.status == 'Resolved') and case.actual_date == None:
					case.close_case()

				if updated:
					case.save()
					if permit_customer and visits:
						for visit in visits:
							visit.save()
				

				''' save updated equipment data''' 
				if permit_equipment_delete or permit_equipment_add:

					current_equip_sn_lst = [str(ce) for ce in case_equipment_sn_lst]

					''' delete equipment from case '''
					if permit_equipment_delete:
						for sn in current_equip_sn_lst:
							if sn not in upd_equip_sn_lst:
								CaseEquipment.objects.get(case_num=Case.objects.get(case_num=id), equip_sn=Equipment.objects.get(equip_sn=sn)).delete()

					''' add equipment to case '''
					if permit_equipment_add:
						for sn in upd_equip_sn_lst:
							if sn not in current_equip_sn_lst:
								new_equip = CaseEquipment(case_num=Case.objects.get(case_num=id), equip_sn=Equipment.objects.get(equip_sn=sn))
								new_equip.save()


					''' refresh equipment data collection '''
					case_equipment = CaseEquipment.objects.filter(case_num=id)
					case_equipment_sn_lst = [ce.equip_sn for ce in case_equipment]
					filtered_case_equipment = Equipment.objects.filter(equip_sn__in=case_equipment_sn_lst)



				''' restrict permits '''
				permit_edit = ('Manager' in groups) or ('Support' in groups and case.status not in ['Resolved','Closed','Cancelled']) or ('Secretary' in groups and case.status in ['Resolved'])
				edit = False
				permit_type = False
				permit_status = False
				permit_target_date = False
				permit_actual_date = False
				permit_on_hold_reason = False
				permit_cancellation_reason = False
				permit_case_manager = False
				permit_machine_down = False
				permit_customer = False
				permit_customer_contact = False
				permit_description = False
				permit_equipment_delete = False
				permit_equipment_add = False

				messages.success(request, 'Case updated successfully')


			except Exception as err:
				''' display errors '''
				messages.error(request, err)
				return redirect('ASISupport_app:view_case', id=id)

			

	return render(request, 'ASISupport_app/case.html', locals())

@login_required(login_url='/accounts/login/')
def new_visit_view(request, id):
	state = 'new'

	case = Case.objects.get(case_num=id)

	if request.method == 'POST' and 'save_btn' in request.POST:

		try:

			
			''' get visit data '''

			''' init visit number '''
			visits = Visit.objects.all()
			visit_num_lst = [int(visit.visit_num[1:]) for visit in visits]
			max_visit_num = max(visit_num_lst)
			req_visit_num 			= 'V'+str(max_visit_num+1).zfill(6)

			''' get visit case num '''
			req_case_num			= case

			''' get visit date '''
			try:
				req_visit_date 			= datetime.strptime(request.POST.get('visit_date'),'%Y-%m-%d')
			except Exception as err:
				messages.error(request, f'Visit date field error: {err}')

			''' get engineer '''
			try:
				req_engineer 			= Employee.objects.get(employee_id=request.POST.get('engineer').split()[2])
			except Exception as err:
				messages.error(request, 'Engineer field error: Invalid engineer')

			''' get visit customer '''
			req_customer 			= case.customer

			''' get customer contact '''
			req_customer_contact 	= request.POST.get('customer_contact')
			if not req_customer_contact:
				messages.error(request, 'Customer contact field error: Customer contact is required')

			''' get remote state '''
			try:

				req_remote		= request.POST.get('remote')
				if req_remote == 'on':
					req_remote = True
				else:
					req_remote = False
			except Exception as err:
				messages.error(request, f'Remote field error: {err}')

			''' get visit start time '''
			req_visit_start 		= request.POST.get('visit_start') + ':00'
			if not req_visit_start:
				messages.error(request, 'Visit start field error: Visit start time is required')
			if not re.match("^([0-9]|[01][0-9]|2[0-3]):([0-9]|[0-5][0-9]):00$", req_visit_start):
				messages.error(request, 'Visit start field error: Visit start must be in HH:mm format')	

			''' get visit end time '''
			req_visit_end 			= request.POST.get('visit_end') + ':00'
			if not req_visit_end:
				messages.error(request, 'Visit end field error: Visit end time is required')
			if not re.match("^([0-9]|[01][0-9]|2[0-3]):([0-9]|[0-5][0-9]):00$", req_visit_end):
				messages.error(request, 'Visit end field error: Visit end must be in HH:mm format')	

			''' get travel hours '''
			if not req_remote:
				req_travel_hours 		= request.POST.get('travel_hours')
				if not req_travel_hours:
					messages.error(request, 'Travel hours field error: Visit travel hours are required')
				if not re.match("^[0-9]*\\.?[0-9]*$", req_travel_hours):
					messages.error(request, 'Travel hours field error: Visit travel hours must be a number greater or equal to zero')	
			else:
				req_travel_hours = 0


			''' get number of engineers '''
			req_num_of_engineers 	= request.POST.get('num_of_engineers')
			if not req_num_of_engineers:
				messages.error(request, 'Number of engineers field error: Visit number of engineers is required')
			if not re.match("^[1-9]*$", req_num_of_engineers):
				messages.error(request, 'Number of engineers field error: Visit number of engineers must be a positive whole number')


			''' get visit summary '''
			req_visit_summary 		= request.POST.get('visit_summary')
			if not req_visit_summary:
				messages.error(request, 'Visit summary field error: Visit summary is required')

			''' get parts data '''
			part_pn_lst = request.POST.getlist('part_num')
			part_qty_lst = request.POST.getlist('qty')
			part_charge_lst = request.POST.getlist('charge')
			part_tbl = pd.DataFrame({'part_pn':part_pn_lst, 'part_qty':part_qty_lst, 'part_charge':part_charge_lst})
			part_tbl = part_tbl.drop(part_tbl[part_tbl.part_pn == ''].index)
			d = {'1': True, '0': False}
			part_tbl['part_charge'] = part_tbl['part_charge'].map(d)
			''' check duplicates '''
			dup_tbl = part_tbl[part_tbl['part_pn'].duplicated()]
			if len(dup_tbl) > 0:
				messages.error(request, f"Parts used field error: Detected more than one instance for part/s {','.join(list(set(dup_tbl['part_pn'].tolist())))}")
			''' check pn validity '''
			if not all(Parts.objects.filter(part_pn=pn).exists() for pn in part_tbl['part_pn'].tolist()):
				messages.error(request, 'Parts used field error: Parts used list contains parts not found in database')
			''' check qty validity '''
			if not all(re.match("^[1-9]+$", qty) for qty in part_tbl['part_qty'].tolist()):
				messages.error(request, 'Parts used field error: Parts used list contains invalid quantity inputs, please enter positive whole numbers only')

			''' display validation errors '''
			message_list = messages.get_messages(request)
			if message_list:
				return redirect('ASISupport_app:new_visit', id=id)


			''' save visit data '''
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
			for index, row in part_tbl.iterrows():
				if Parts.objects.filter(part_pn=row['part_pn']).exists():
					part_data = VisitParts(visit_num=Visit.objects.get(visit_num=req_visit_num),
										part_pn=Parts.objects.get(part_pn=row['part_pn']),
										qty=row['part_qty'],
										charge=row['part_charge']
										)
					part_data.save()


			messages.success(request, 'Visit created successfully')
			return redirect('ASISupport_app:view_visit', id=req_visit_num)

		except Exception as err:
			''' display errors '''
			if Visit.objects.filter(visit_num=req_visit_num):
				messages.warning(request, f'Parts used field error: {err}')
				return redirect('ASISupport_app:view_visit', id=req_visit_num)

			messages.error(request, err)
			return redirect('ASISupport_app:new_visit', id=id)


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
	employees = Employee.objects.all()


	if request.method == 'POST' and 'back_btn' in request.POST:
		return redirect('ASISupport_app:view_case', id=visit.case_num)

	visit.sum_visit_hours()
	case = Case.objects.get(case_num=visit.case_num)

	visit_parts_lst = VisitParts.objects.filter(visit_num=id)
	visit_part_pn_lst = [vp.part_pn for vp in visit_parts_lst]
	parts_in_visit = Parts.objects.filter(part_pn__in=visit_part_pn_lst)
	part_description_dict = {VisitParts.objects.get(visit_num=id, part_pn=part.part_pn):part.part_description for part in parts_in_visit}

	parts = Parts.objects.all()
	parts_dict = {part.part_pn:part.part_description for part in parts}

	''' roles '''
	groups = list(request.user.groups.values_list('name',flat = True))

	''' restrict permits '''
	permit_edit = ('Manager' in groups) or ('Support' in groups and case.status not in ['Resolved','Closed','Cancelled'])
	edit = False
	permit_visit_date = False
	permit_engineer = False
	permit_customer_contact = False
	permit_remote = False
	permit_visit_start = False
	permit_visit_end = False
	permit_travel_hours = False
	permit_num_of_engineers = False
	permit_visit_summary = False
	permit_parts_add = False
	permit_parts_delete = False
		



	if (request.method == 'POST' and 'edit_btn' in request.POST) or (request.method == 'POST' and 'save_btn' in request.POST):
		edit = True

		''' grant permissions per group '''
		if 'Manager' in groups:
			permit_visit_date = True
			permit_engineer = True
			permit_customer_contact = True
			permit_remote = True
			permit_visit_start = True
			permit_visit_end = True
			permit_travel_hours = True
			permit_num_of_engineers = True
			permit_visit_summary = True
			permit_parts_add = True
			permit_parts_delete = True


		if 'Support' in groups:
			permit_customer_contact = True
			permit_remote = True
			permit_visit_summary = True
			permit_parts_add = True


		if 'Secretary' in groups:
			pass
	

		if request.method == 'POST' and 'save_btn' in request.POST:

			try:

				''' get updated visit data''' 
				updated = False

				''' get visit date '''
				if permit_visit_date:
					try:
						upd_visit_date = datetime.strptime(request.POST.get('visit_date'),'%Y-%m-%d')
						if upd_visit_date != visit.visit_date:
							visit.visit_date = upd_visit_date
							updated = True
					except Exception as err:
						messages.error(request, f'Visit date field error: {err}')

				''' get engineer '''
				if permit_engineer:
					try:
						upd_engineer = Employee.objects.get(employee_id=request.POST.get('engineer').split()[2])
						if upd_engineer != visit.engineer:
							visit.engineer = upd_engineer
							updated = True
					except Exception as err:
						messages.error(request, 'Engineer field error: Invalid engineer')

				''' get customer contact '''
				if permit_customer_contact:
					upd_customer_contact = request.POST.get('customer_contact')
					if upd_customer_contact != visit.customer_contact:
						if not upd_customer_contact:
							messages.error(request, 'Customer contact field error: Customer contact is required')
						else:
							visit.customer_contact = upd_customer_contact
							updated = True

				''' get remote state '''
				if permit_remote:
					try:
						upd_remote = request.POST.get('remote')
						if upd_remote == 'on':
							upd_remote = True
						else:
							upd_remote = False

						if upd_remote != visit.remote:
							visit.remote = upd_remote
							updated = True
					except Exception as err:
						messages.error(request, f'Remote field error: {err}')

				''' get visit start time '''
				if permit_visit_start:
					upd_visit_start = request.POST.get('visit_start') + ':00'
					if upd_visit_start != visit.visit_start:
						if not upd_visit_start:
							messages.error(request, 'Visit start field error: Visit start time is required')
						elif not re.match("^([0-9]|[01][0-9]|2[0-3]):([0-9]|[0-5][0-9]):00$", upd_visit_start):
							messages.error(request, 'Visit start field error: Visit start must be in HH:mm format')	
						else:
							visit.visit_start = upd_visit_start
							updated = True

				''' get visit end time '''
				if permit_visit_end:
					upd_visit_end = request.POST.get('visit_end') + ':00'
					if upd_visit_end != visit.visit_end:
						if not upd_visit_end:
							messages.error(request, 'Visit end field error: Visit end time is required')
						elif not re.match("^([0-9]|[01][0-9]|2[0-3]):([0-9]|[0-5][0-9]):00$", upd_visit_end):
							messages.error(request, 'Visit end field error: Visit end must be in HH:mm format')	
						else:
							visit.visit_end = upd_visit_end
							updated = True

				''' get travel hours '''
				if not visit.remote:
					if permit_travel_hours:
						upd_travel_hours = request.POST.get('travel_hours')
						if upd_travel_hours != visit.travel_hours:
							if not upd_travel_hours:
								messages.error(request, 'Travel hours field error: Visit travel hours are required')
							elif not re.match("^[0-9]*\\.?[0-9]*$", upd_travel_hours):
								messages.error(request, 'Travel hours field error: Visit travel hours must be a number greater or equal to zero')
							else:
								visit.travel_hours = upd_travel_hours
								updated = True
				else:
					visit.travel_hours = 0

				''' get number of engineers '''
				if permit_num_of_engineers:
					upd_num_of_engineers = request.POST.get('num_of_engineers')
					if upd_num_of_engineers != visit.num_of_engineers:
						if not upd_num_of_engineers:
							messages.error(request, 'Number of engineers field error: Visit number of engineers is required')
						elif not re.match("^[1-9]*$", upd_num_of_engineers):
							messages.error(request, 'Number of engineers field error: Visit number of engineers must be a positive whole number')
						else:
							visit.num_of_engineers = upd_num_of_engineers
							updated = True

				''' get visit summary '''
				if permit_visit_summary:
					upd_visit_summary = request.POST.get('visit_summary')
					if upd_visit_summary != visit.visit_summary:
						if not upd_visit_summary:
							messages.error(request, 'Visit summary field error: Visit summary is required')
						else:
							visit.visit_summary = upd_visit_summary
							updated = True

				''' get updated parts data'''
				part_pn_lst = request.POST.getlist('part_num')
				part_qty_lst = request.POST.getlist('qty')
				part_charge_lst = request.POST.getlist('charge')
				part_tbl = pd.DataFrame({'part_pn':part_pn_lst, 'part_qty':part_qty_lst, 'part_charge':part_charge_lst})
				d = {'1': True, '0': False}
				part_tbl['part_charge'] = part_tbl['part_charge'].map(d)
				''' check duplicates '''
				dup_tbl = part_tbl[part_tbl['part_pn'].duplicated()]
				if len(dup_tbl) > 0:
					messages.error(request, f"Parts used field error: Detected more than one instance for part/s {','.join(list(set(dup_tbl['part_pn'].tolist())))}")
				''' check pn validity '''
				if not all(Parts.objects.filter(part_pn=pn).exists() for pn in part_tbl['part_pn'].tolist()):
					messages.error(request, 'Parts used field error: Parts used list contains parts not found in database')
				''' check qty validity '''
				if not all(re.match("^[1-9]+$", qty) for qty in part_tbl['part_qty'].tolist()):
					messages.error(request, 'Parts used field error: Parts used list contains invalid quantity inputs, please enter positive whole numbers only')


				''' check for existing validation errors '''
				message_list = messages.get_messages(request)
				if message_list:
					return redirect('ASISupport_app:view_visit', id=id)


				''' save updated visit data '''
				if updated:
					visit.save()

				''' save updated parts data ''' 
				if permit_parts_delete or permit_parts_add:

					''' delete parts from visit '''
					if permit_parts_delete:
						for vp in visit_parts_lst:
							if part_tbl.loc[(part_tbl['part_pn'] == vp.part_pn) & (part_tbl['part_qty'] == vp.qty) & (part_tbl['part_charge'] == vp.charge)].empty:
								VisitParts.objects.get(visit_num=Visit.objects.get(visit_num=vp.visit_num), part_pn=Parts.objects.get(part_pn=vp.part_pn)).delete()


					''' add parts to visit '''
					if permit_parts_add:
						for index, row in part_tbl.iterrows():
							if Parts.objects.filter(part_pn=row['part_pn']).exists() and not visit_parts_lst.filter(part_pn=row['part_pn'], qty=row['part_qty'], charge=row['part_charge']).exists():
								part_data = VisitParts(visit_num=Visit.objects.get(visit_num=visit.visit_num),
													part_pn=Parts.objects.get(part_pn=row['part_pn']),
													qty=row['part_qty'],
													charge=row['part_charge']
													)
								part_data.save()



					''' refresh part data collection '''
					visit_parts_lst = VisitParts.objects.filter(visit_num=id)
					visit_part_pn_lst = [vp.part_pn for vp in visit_parts_lst]
					parts_in_visit = Parts.objects.filter(part_pn__in=visit_part_pn_lst)
					part_description_dict = {VisitParts.objects.get(visit_num=id, part_pn=part.part_pn):part.part_description for part in parts_in_visit}


				''' restrict permits '''
				permit_edit = ('Manager' in groups) or ('Support' in groups)
				edit = False
				permit_visit_date = False
				permit_engineer = False
				permit_customer_contact = False
				permit_remote = False
				permit_visit_start = False
				permit_visit_end = False
				permit_travel_hours = False
				permit_num_of_engineers = False
				permit_visit_summary = False
				permit_parts_add = False
				permit_parts_delete = False

				''' refresh visit data collection '''
				visit = Visit.objects.get(visit_num=id)
				visit.sum_visit_hours()


			except Exception as err:
				''' display errors '''
				messages.error(request, err)
				return redirect('ASISupport_app:view_visit', id=id)


	return render(request, 'ASISupport_app/visit.html', locals())

@login_required(login_url='/accounts/login/')
def report_view(request):

	if request.method == 'POST' and 'case_report_clear_btn' in request.POST:
		spotter	= 'case_report'	

	if request.method == 'POST' and 'visit_report_clear_btn' in request.POST:
		spotter	= 'visit_report'	

	if request.method == 'POST' and 'Equipment_report_clear_btn' in request.POST:
		spotter	= 'Equipment_report'	

	if request.method == 'POST' and 'back_btn' in request.POST:
		return redirect('ASISupport_app:dashboard')

	if request.method == 'POST' and 'case_report_search_btn' in request.POST:
		case_report_case 			= request.POST.get('case_report_case')
		case_report_from_date 		= request.POST.get('case_report_from_date')
		case_report_to_date 		= request.POST.get('case_report_to_date')
		case_report_type 			= request.POST.get('case_report_type')
		case_report_status 			= request.POST.get('case_report_status')
		case_report_case_manager 	= request.POST.get('case_report_case_manager')
		case_report_customer 		= request.POST.get('case_report_customer')
		case_report_machine_down 	= request.POST.get('case_report_machine_down')

		cases = Case.objects.all()

		if case_report_case:
			cases = cases.filter(case_num__contains=case_report_case)
		if case_report_from_date:
			cases = cases.filter(create_date__gte=case_report_from_date)
		if case_report_to_date:
			cases = cases.filter(create_date__lte=case_report_to_date)
		if case_report_type:
			cases = cases.filter(case_type=case_report_type)
		if case_report_status:
			cases = cases.filter(status=case_report_status)
		if case_report_case_manager:
			cases = cases.filter(case_manager=Employee.objects.get(employee_id=case_report_case_manager.split()[2]))
		if case_report_customer:
			cases = cases.filter(customer=Customer.objects.get(customer_name=case_report_customer))
		if case_report_machine_down:
			cases = cases.filter(machine_down=True if case_report_machine_down == 'True' else False)

	if request.method == 'POST' and 'visit_report_search_btn' in request.POST:
		visit_report_visit			= request.POST.get('visit_report_visit')
		visit_report_from_date		= request.POST.get('visit_report_from_date')
		visit_report_to_date		= request.POST.get('visit_report_to_date')
		visit_report_engineer		= request.POST.get('visit_report_engineer')
		visit_report_customer		= request.POST.get('visit_report_customer')
		visit_report_remote			= request.POST.get('visit_report_remote')
		visit_report_case			= request.POST.get('visit_report_case')

		visits = Visit.objects.all()

		if visit_report_visit:
			visits = visits.filter(visit_num__contains=visit_report_visit)
		if visit_report_from_date:
			visits = visits.filter(visit_date__gte=visit_report_from_date)
		if visit_report_to_date:
			visits = visits.filter(visit_date__lte=visit_report_to_date)
		if visit_report_engineer:
			visits = visits.filter(engineer=Employee.objects.get(employee_id=visit_report_engineer.split()[2]))
		if visit_report_customer:
			visits = visits.filter(customer=Customer.objects.get(customer_name=visit_report_customer))
		if visit_report_remote:
			visits = visits.filter(remote=True if visit_report_remote == 'True' else False)
		if visit_report_case:
			visits = visits.filter(case_num__in=Case.objects.filter(case_num__contains=visit_report_case))

	if request.method == 'POST' and 'equip_report_search_btn' in request.POST:
		equip_report_sn				= request.POST.get('equip_report_sn')
		equip_report_pn				= request.POST.get('equip_report_pn')
		equip_report_description	= request.POST.get('equip_report_description')
		equip_report_case			= request.POST.get('equip_report_case')
		equip_report_customer		= request.POST.get('equip_report_customer')
		
		case_equip = CaseEquipment.objects.all()

		if equip_report_sn:
			case_equip = case_equip.filter(equip_sn__in=Equipment.objects.filter(equip_sn__contains=equip_report_sn))
		if equip_report_pn:
			case_equip = case_equip.filter(equip_sn__in=Equipment.objects.filter(equip_pn__contains=equip_report_pn))
		if equip_report_description:
			case_equip = case_equip.filter(equip_sn__in=Equipment.objects.filter(equip_description__contains=equip_report_description))
		if equip_report_case:
			case_equip = case_equip.filter(case_num__in=Case.objects.filter(case_num__contains=equip_report_case))
		if equip_report_customer:
			case_equip = case_equip.filter(case_num__in=Case.objects.filter(customer=Customer.objects.get(customer_name=equip_report_customer)))

		case_equip_lst = [{'sn':ce.equip_sn,
						 'pn':Equipment.objects.get(equip_sn=ce.equip_sn).equip_pn, 
						 'description':Equipment.objects.get(equip_sn=ce.equip_sn).equip_description, 
						 'installation_date':Equipment.objects.get(equip_sn=ce.equip_sn).installation_date, 
						 'warranty':Equipment.objects.get(equip_sn=ce.equip_sn).warranty, 
						 'case':ce.case_num, 
						 'customer':Case.objects.get(case_num=ce.case_num).customer.customer_name} for ce in case_equip]
		

	types = Case.TYPES
	statuses = Case.STATUSES
	employees = Employee.objects.all()
	customers = Customer.objects.all()
		
	return render(request, 'ASISupport_app/report.html', locals())
