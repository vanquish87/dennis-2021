from calendar import c
from dataclasses import field, fields
from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # django will create all the fiels according to model with __all__
        # fields = '__all__'
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags']