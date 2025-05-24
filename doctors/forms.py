from django import forms
from .models import Doctor
from core.models import Specialty

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty', 'license_number', 'experience_years', 'education', 'bio', 'consultation_fee']
        widgets = {
            'education': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'specialty': 'Mutaxassislik',
            'license_number': 'Litsenziya raqami',
            'experience_years': 'Tajriba (yil)',
            'education': 'Ta\'lim',
            'bio': 'Biografiya',
            'consultation_fee': 'Konsultatsiya narxi'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Specialty choices
        self.fields['specialty'].queryset = Specialty.objects.all()
        self.fields['specialty'].empty_label = "Mutaxassislikni tanlang"
