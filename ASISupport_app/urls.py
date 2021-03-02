from django.urls import path
from ASISupport_app import views

app_name = 'ASISupport_app'

urlpatterns = [
	path('dashboard/', views.dashboard_view, name = 'dashboard'),
	path('case/', views.new_case_view, name = 'new_case'),
	path('case/<id>/', views.case_view, name = 'view_case'),
	path('visit/', views.visit_view, name = 'visit'),
	path('login/', views.login_view, name = 'login'),
]

