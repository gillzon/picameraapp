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
from .forms import AddPlantForm, UploadPhotoForm
from django.db.models import (Avg, 
                            Count, 
                            Min, 
                            Sum)
from django.contrib.auth.mixins import LoginRequiredMixin
import RPi.GPIO as GPIO
import time
import picamera


# Create your views her
class LoggedIn(LoginRequiredMixin,TemplateView):
    template_name = 'login_index.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        user_id = self.request.user.id
        get_plants = Plant.objects.filter(user_id=user_id).order_by('-created_at')
        get_total_plants = (Plant.objects
            .filter(user_id=user_id)
            .aggregate(the_sum=Sum('total_pictures')))    
        ctx['get_plants'] = get_plants
        ctx['get_total_plants'] = get_total_plants
        return ctx

class Create_Plant(LoginRequiredMixin, CreateView):
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

class UploadPhoto(LoginRequiredMixin,CreateView):
    model = Photos
    form_class = UploadPhotoForm
    template_name = 'upload_photo.html'


    def form_valid(self, form):
        files = self.request.FILES.getlist('photo_room_image')
        with picamera.PiCamera() as camera:
             camera.resolution = (1280, 720)
             camera.start_preview()
             camera.exposure_compensation = 2
             camera.exposure_mode = "spotlight"
             camera.meter_mode = "matrix"
             camera.image_effect = "gpen"
             time.sleep(2)
             camera.capture('foo.jpg')
             camera.stop_preview()
        if files:
            user_id = self.request.user.id
            pk = self.kwargs['pk']
            plant_info = Plant.objects.get(id=pk)
            form.instance.user_id = pk
            plant_info.total_pictures = plant_info.total_pictures + 1
            plant_info.save()
            form = form.save(commit=False)
            form.save()
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(18,GPIO.OUT)
            GPIO.output(18,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(18,GPIO.LOW)
            return super().form_valid(form)
        else:
            form = UploadPhotoForm()

    def get_success_url(self):
        return reverse('core:loggedin')


class Delete_Plant_View(DeleteView):
    template_name = 'delete_plant.html'
    model = Plant

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        return ctx
    def get_success_url(self):
        return reverse('core:loggedin')
