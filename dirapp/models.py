from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, AbstractBaseUser
import Image

# Create your models here.


class UserProfileManager(models.Manager):
    def search(self, q):
        if q:
            return UserProfile.objects.filter(Q(user__email__icontains=q) | Q(user__first_name__icontains=q) |
                                          Q(user__last_name__icontains=q))
        else:
            return UserProfile.objects.all()


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    Address = models.CharField(max_length=50)
    Photo = models.FileField(upload_to='photos', default='photos/default.jpg')
    Phone = models.CharField(max_length=20, null=True)
    objects = UserProfileManager()

    def save(self, *args, **kwargs):
        # save user profile
        super(UserProfile, self).save(*args, **kwargs)
        # resize user photo
        if self.Photo:
            size = 50, 50
            im = Image.open(self.Photo.path)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(self.Photo.path, 'JPEG')
