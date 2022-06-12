import profile
from django.shortcuts import redirect, render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

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
    
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile

    form = ProjectForm()
    if request.method == 'POST':
        # creating instance of the form with 'POST' data
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # to save it to Project Model
            project = form.save(commit=False)
            # onetoMany relatioship update , so that owner data can be saved
            project.owner = profile
            project.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

# we will create instance of the project using 'pk' then update it
@login_required(login_url='login')
def updateProject(request, pk):
    # only owner user can update this project
    profile = request.user.profile
    # only getting children 
    project = profile.project_set.get(id=pk)
    # project = Project.objects.get(id=pk)
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

@login_required(login_url='login')
def deleteProject(request, pk):
    # only owner user can delete this project
    profile = request.user.profile
    # only getting children 
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project} 
        
    return render(request, 'projects/delete_template.html', context)