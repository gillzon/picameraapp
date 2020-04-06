import os, time
from datetime import datetime
from django.conf import settings
import picamera
from core.models import Photos, Plant
from django.core.management.base import BaseCommand, CommandError
def Command():
    with picamera.PiCamera() as camera:
        borje = 18
        camera.resolution = (2592, 1944)
        camera.start_preview()
        time.sleep(5)
        if not os.path.exists(MEDIA_ROOT + '/' + "images/{restfolder}/".format(restfolder=borje)):
            os.makedirs(MEDIA_ROOT + '/' + "images/{restfolder}/".format(restfolder=borje))
        database_name = 'images' + '/' + str(borje) + '/' + "Pi_Camera" + date_now.strftime("%Y%m%d%f") + '.jpg'
        filename = MEDIA_ROOT + '/' + database_name
        camera.capture(filename)
        camera.stop_preview()
        add_picture = Photos.objects.create(photo_room_image=database_name, user_id=borje)
        add_picture.save()