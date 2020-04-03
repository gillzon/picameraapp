from django import forms
from django.contrib.auth.models import User
from .models import Plant



class AddPlantForm(forms.ModelForm):
	name = forms.CharField(required=True)
	name.widget.attrs['class'] = 'form-control'
	name.widget.attrs['placeholder'] = 'Chili, Tomato etc.'

	description = forms.CharField(required=True)
	description.widget.attrs['class'] = 'form-control'
	description.widget.attrs['placeholder'] = 'Description of the plant you are waiting to grow'
	class Meta:
		model = Plant
		fields = ['name','description']
