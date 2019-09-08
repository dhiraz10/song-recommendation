from django.db import models
from django.contrib.auth.models import User
from time import time

# Create your models here.
def get_upload_path(instance,filename):
	return "songimgs/%s_%s" %(str(time()).replace('.','_'),filename)

class Song(models.Model):
	name= models.CharField(max_length=100)
	file= models.FileField(upload_to='media/songs/')
	tag= models.CharField(max_length=100, blank=True)
	# description= models.CharField(max_length=500, blank=True)
	image = models.ImageField(upload_to= get_upload_path,blank=True)
	# randoms = RandomManager()
	def __str__(self):
		return self.name

class UserInterest(models.Model):
	user= models.ForeignKey(User,on_delete=models.CASCADE)
	tag= models.CharField(max_length=100)
	song= models.ForeignKey(Song,default=1,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class Review(models.Model):
	user= models.ForeignKey(User,on_delete=models.CASCADE)
	song= models.ForeignKey(Song,on_delete=models.CASCADE)
	rating= models.IntegerField()
	review= models.CharField(max_length=400, blank=True)
	def __str__(self):
		return self.user.username
