from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import views

from django.views.generic import (CreateView, 
                                    UpdateView, 
                                    DeleteView, 
                                    DetailView, 
                                    TemplateView, 
                                    ListView, 
                                    View, 
                                    FormView)
from time import sleep
from django.contrib.auth.models import User
from .models import Photos, Plant
from .forms import AddPlantForm

# Create your views her
class LoggedIn(TemplateView):
    template_name = 'login_index.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        user_id = self.request.user.id
        get_plants = Plant.objects.filter(user_id=user_id).order_by('-created_at')
        ctx['get_plants'] = get_plants
        return ctx

class Create_Plant(CreateView):
	model = Plant
	form_class = AddPlantForm
	template_name = 'create_plant.html'

	def form_valid(self, form):
		form.instance.user_id = self.request.user.id
		form.instance.total_pictures = 0
		form = form.save()
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('core:loggedin')

class UploadPhoto(CreateView):
    model = Photos
    #form_class = UploadPhotoForm
    template_name = 'index_upload.html'


    def form_valid(self, form):
        files = self.request.FILES.getlist('photo_room_image')
        if files:

            room_code = self.request.GET.get("room_code")
            print("room_code", room_code)

            peder = BeerRoom.objects.get(room_code=room_code)
            peder.total_pictures = peder.total_pictures + 1
            peder.save()
            form.instance.beerroom_id = peder.pk
            form = form.save(commit=False)
            form.save()
            return super().form_valid(form)
        else:
            form = UploadPhotoForm()

    def get_success_url(self):
        room_code = self.request.GET.get("room_code")
        return reverse('core:fekkenation_room', kwargs={'room_code': room_code})
