import email
from email.policy import default
from django.db import models
# for user model check django docs
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    # one to one relationship model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    # to make access easier we are using username in this model itself
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio =  models.TextField(blank=True, null=True)
    # upload_to for location inside image folder ie, images/profiles
    profile_image = models.ImageField(null=True, blank=True, upload_to ='profies/', default='profiles/user-default.png' )
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube= models.CharField(max_length=200, blank=True, null=True)
    social_website= models.CharField(max_length=200, blank=True, null=True)
    
    # create Timestamp automatically
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
         return str(self.username)

    class Meta:
        # results display in which order
        # ordering : highest vote_ratio first, if there is tie than by highest vote_total
        ordering = ['-created']

    # in case user deletes project image we still need something to render template
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url


class Skill(models.Model):
    # many to one relationship 
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    # it would be react, javascript, django etc
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # create Timestamp automatically
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
         return str(self.name)


class Message(models.Model):
    # blank=True, null=True because non registered user can also send message
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    # related_name='messages' is used because both sender n recipient are connected to same model ie, Profile hence needs differnt name to access Message model in Parent child relationship
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')

    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    body =  models.TextField()
    is_read = models.BooleanField(default=False, null=True)

    
    # create Timestamp automatically
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
         return str(self.subject)
    
    class Meta:
        # by unread first and created second priority
        ordering = ['is_read', '-created']