from django.shortcuts import render

#imports for login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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
	return render(request, 'ASISupport_app/dashboard.html')

def case_view(request):
	return render(request, 'ASISupport_app/case.html')

def visit_view(request):
	return render(request, 'ASISupport_app/visit.html')
