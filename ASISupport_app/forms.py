from django import forms 
from ASISupport_app.models import Case

class NewCaseAdminForm(forms.ModelForm):	

    class Meta: 
        model = Case 
        fields = "__all__"


class NewCaseSupportForm(forms.ModelForm):	

    class Meta: 
        model = Case 
        fields = ['actual_date', 'machine_down', 'case_description', 'cancellation_reason', 'on_hold_reason']