from django.urls import path
from ASISupport_app import views

app_name = 'ASISupport_app'

urlpatterns = [
	path('dashboard/', views.dashboard_view, name = 'dashboard'),
	path('new_case/', views.new_case_view, name = 'new_case'),
	path('case/<id>/', views.case_view, name = 'view_case'),
	path('new_visit/<case>/', views.new_visit_view, name = 'new_visit'),
	path('visit/<id>/', views.visit_view, name = 'view_visit'),
]

