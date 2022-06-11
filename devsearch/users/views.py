from multiprocessing import context
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# for flashing messages
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm

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
            return redirect('profiles')
        else:
            messages.error(request, 'Error has occurred during registration')


    return render(request, 'users/login_register.html', context)
    
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    # exclude skills which doesn't have any description in child model
    topSkills = profile.skill_set.exclude(description__exact='')
    # give skills which are empty in description
    otherSkills = profile.skill_set.filter(description='')
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)