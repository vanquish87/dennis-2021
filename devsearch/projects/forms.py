from calendar import c
from dataclasses import field, fields
from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # django will create all the fiels according to model with __all__
        # fields = '__all__'
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        # with this we are modifying classes in html for form
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    # with this we are modifying classes in html for form
    # didn't understand much, advanced concept
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # to avoid repetition for every field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'add title'})
        
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'add descriptioon'})