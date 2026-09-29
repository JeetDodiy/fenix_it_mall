"""
Employees App – Forms
"""
from django import forms
from .models import Employee, Attendance, Leave


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone', 'address',
                  'designation', 'department', 'salary', 'join_date', 'status', 'profile_picture']
        widgets = {
            'employee_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. EMP-001  (leave blank to auto-generate)',
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit number', 'maxlength': '10', 'minlength': '10', 'pattern': '[0-9]{10}', 'title': 'Enter 10-digit phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'designation': forms.TextInput(attrs={'class': 'form-input'}),
            'department': forms.TextInput(attrs={'class': 'form-input'}),
            'salary': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'join_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make employee_id optional in the form (model auto-generates if blank)
        self.fields['employee_id'].required = False
        self.fields['employee_id'].help_text = 'Leave blank to auto-generate.'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'check_in', 'check_out', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'check_in': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
