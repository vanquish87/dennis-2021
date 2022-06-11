from django.shortcuts import redirect, render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

# Create your views here.
# hence 'projects/projects.html' will work. since folder needs to be specified
def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)


# -------------CRUD views------------------
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': projectObj})

def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        # creating instance of the form with 'POST' data
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # to save it to Project Model
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

# we will create instance of the project using 'pk' then update it
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        # creating instance of the form with 'POST' data
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            # to save it to Project Model
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    context = {'object': project} 
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
        
    return render(request, 'projects/delete_template.html', context)