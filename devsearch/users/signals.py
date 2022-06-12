# for user model check django docs
import profile
from django.contrib.auth.models import User
from .models import Profile
# signals in django to initiate actions saving or deleting
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 


# sender is model which started, created=False is when updated, True when new created
# we use decorator to fire signals
# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    # because of onetoOne relationship
    user = profile.user
    # only to run when update happens
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
        print(f'User updated....{user} ')

# since one to one relationship, reverse of profile deleted will not delete user
# to work around we use post_delete signal to fire this deleteUser 
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print(f'Deleting user....{instance} ')

# anytime User model is created/updated this signal will run
post_save.connect(createProfile, sender=User)
# anytime profile is updated this signal will run
post_save.connect(updateProfile, sender=Profile)

post_delete.connect(deleteUser, sender=Profile)