from django.contrib import admin

# Register your models here.
from .models import Message, Profile, Skill

# to show up in admin panel
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)