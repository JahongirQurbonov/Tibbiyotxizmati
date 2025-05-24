from django import forms
from .models import Patient

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['gender', 'blood_type', 'emergency_contact', 'emergency_phone', 
                 'medical_history', 'allergies', 'current_medications']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'current_medications': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'gender': 'Jinsi',
            'blood_type': 'Qon guruhi',
            'emergency_contact': 'Favqulodda aloqa',
            'emergency_phone': 'Favqulodda telefon',
            'medical_history': 'Tibbiy tarix',
            'allergies': 'Allergiyalar',
            'current_medications': 'Joriy dorilar'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
