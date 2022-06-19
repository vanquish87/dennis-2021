from multiprocessing import context
import profile
from urllib import request
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# for flashing messages
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles

# Create your views here.
def loginUser(request):
    # check for session in cookie to check if already logged in
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        # request.method is a dictionary of all the data in POST
        username = request.POST['username']
        password = request.POST['password']

        # to check if user exist in database
        try:
            user = User.objects.get(username=username)
        except:
            # for flashing messages
            messages.error(request, 'Username doesnt exist')

        # this check password against username in database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # sets session for user
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def registerUser(request):
    # to render login n register in same page using variable 'page'
    page = 'register'
    # importing custom form with name n email n stuff
    form = CustomUserCreationForm()
    context = {'page': page, 'form': form}
    # creating instance of the form with 'POST' data
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # holding a instance before saving to protect from case sensitive username
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')
            # sets session for user
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'Error has occurred during registration')


    return render(request, 'users/login_register.html', context)
    
def profiles(request):
    # using external function to make code cleaner
    profiles, search_query = searchProfiles(request)
    context = {'profiles': profiles, 'search_query': search_query}

    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    # exclude skills which doesn't have any description in child model
    topSkills = profile.skill_set.exclude(description__exact='')
    # give skills which are empty in description
    otherSkills = profile.skill_set.filter(description='')
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    # OnetoONe relationship for getting profile
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    # prefilled form
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm
    context = {'form': form}
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            # add owner , many to one relationship 
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill was added successfully!')
            return  redirect('account')
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    # get skill from profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    context = {'form': form}
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'skill was updated successfully!')
            return  redirect('account')
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    # get skill from profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete() 
        messages.success(request, 'skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)