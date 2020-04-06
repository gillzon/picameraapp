from django import forms
from django.contrib.auth.models import User
from .models import Plant, Photos



class AddPlantForm(forms.ModelForm):
	name = forms.CharField(required=True)
	name.widget.attrs['class'] = 'form-control'
	name.widget.attrs['placeholder'] = 'Chili, Tomato etc.'

	description = forms.CharField(required=True)
	description.widget.attrs['class'] = 'form-control'
	description.widget.attrs['placeholder'] = 'Description of the plant you are waiting to grow'

	active_pi = forms.BooleanField(required=False)
	active_pi.widget.attrs['class'] = 'form-control-checkbox'
	class Meta:
		model = Plant
		fields = ['name','description', 'active_pi']

class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['photo_room_image']