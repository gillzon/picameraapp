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
#import RPi.GPIO as GPIO
import time
from datetime import datetime
import tempfile, zipfile
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import picamera
MEDIA_ROOT = settings.MEDIA_ROOT

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
        date_now = datetime.now()
        files = self.request.FILES.getlist('photo_room_image')
        _pk = self.request.user.id
        get_pk = User.objects.get(id=_pk)

        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)
            filename = MEDIA_ROOT + date_now.strftime("%Y%m%d%f") + '.jpg'
            camera.capture(filename)
            add_picture = Photos.objects.create(photo_room_image=filename, user_id=get_pk.id)
            add_picture.save()
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
            #GPIO.setmode(GPIO.BCM)
            #GPIO.setwarnings(False)
            #GPIO.setup(18,GPIO.OUT)
            #GPIO.output(18,GPIO.HIGH)
            #time.sleep(2)
            #GPIO.output(18,GPIO.LOW)
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



def download_image(request, pk):
        """                                                                         
        Create a ZIP file on disk and transmit it in chunks of 8KB,                 
        without loading the whole file into memory. A similar approach can          
        be used for large dynamic PDF files.                                        
        """
        product_image = Photos.objects.filter(user_id__id=pk).values_list('photo_room_image', flat=True)
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        i = 0
        for index in product_image:
            filename = settings.MEDIA_ROOT + "/" +index # Replace by your files here.  
            archive.write(filename, 'file{name}'.format(name=index)) # 'file%d.png' will be the
        archive.close()
        temp.seek(0)
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=photos.zip'
        return response