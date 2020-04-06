from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import string, random, piexif, os
from uuid import uuid4
from django.conf import settings
from PIL import Image

# Create your models here.
def path_and_rename(instance, filename):
    #room_code = instance.beerroom.room_code
    pk = instance.user_id
    upload_to = 'images/{id}'.format(id=pk)
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    total_pictures = models.IntegerField()
    active_pi = models.BooleanField()



class Photos(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Plant, on_delete=models.CASCADE)
    photo_room_image = models.ImageField(upload_to=path_and_rename, validators=[FileExtensionValidator(allowed_extensions=['png','jpeg','jpg'])])


    def __str__(self):
        return self.id + self.user

    def save(self, *args, **kwargs):
        super(Photos, self).save(*args, **kwargs)
        print("partyroom",self.user.id)
        #img = Image.open(self.photo_room_image.path)
        img = Image.open(self.photo_room_image.path)
        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])

            if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                exif_bytes = piexif.dump(exif_dict)

                if orientation == 2:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    img = img.rotate(180)
                elif orientation == 4:
                    img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 5:
                    img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 6:
                    img = img.rotate(-90, expand=True)
                elif orientation == 7:
                    img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

                img.save(self.photo_room_image.path, exif=exif_bytes)
        #if img.height > 860 or img.width > 1024:
        #    output_size = (860,1024)
        #    img.thumbnail(output_size)
        #    img.save(self.photo_room_image.path)