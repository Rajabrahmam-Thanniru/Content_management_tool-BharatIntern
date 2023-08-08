
from django.db import models
from django.contrib.auth.models import User

STATUS = (
	(0,"Draft"),
	(1,"Publish"),
	(2, "Delete")
)

# creating an django model class
class posts(models.Model):
	
	title = models.CharField(max_length=200, unique=True)
	
	slug = models.SlugField(max_length=200, unique=True)

	author = models.CharField(max_length=200, unique=True)
	
	updated_on = models.DateTimeField(auto_now= True)

	created_on = models.DateTimeField()
	
	content = models.TextField()

	metades = models.CharField(max_length=300, default="new post")

	status = models.IntegerField(choices=STATUS, default=0)

	class Meta:
		ordering = ['-created_on']
		
	def __str__(self):
		return self.title
	

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

