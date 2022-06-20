from email import message
from multiprocessing import context
import profile
from urllib import request
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# for flashing messages
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginationProfiles

# Create your views here.
def loginUser(request):
    # check for session in cookie to check if already logged in
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        # request.method is a dictionary of all the data in POST
        username = request.POST['username'].lower()
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
            # if next in the url value so redirect there else to account page
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
    results = 2
    custom_range, profiles = paginationProfiles(request, profiles, results)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}

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


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    # related_name='messages' is used because both sender n recipient are connected to same model ie, Profile hence needs differnt name to access Message model in Parent child relationship
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request,  'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    # only get messages for logged in profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request,  'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    # since non logged in can also send message we need try method to check
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            # if logged in
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request,  'users/message_form.html', context)
