from .models import Profile, Skill
# going to use Q lookup to use "OR" in search
from django.db.models import Q
# read django docs for paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginationProfiles(request, profiles, results):
    # using Paginator, request in URL already have page no.
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    # resets results to load page variable number
    try:
        profiles = paginator.page(page)
    # if this is just click visit with no page no. given
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    # if page called is out of range
    except EmptyPage:
        # num_pages tells how many pages ie, set to last page
        page = paginator.num_pages
        profiles = paginator.page(page)

    # if we have lots of pages but don't want to show all the buttons in paginator
    leftIndex = (int(page) - 2)
    # nearing initial pages
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)
    # for nearing last pages
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    search_query = ''
    # extract search_query from frontend
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains=search_query)
    # going to use Q lookup to use "OR" in search '|' will say OR
    # using icontains because we don't need case senstivity
    # using distinct() because skills lookup is giving multiple entries for same instance
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) | 
        Q(skill__in=skills)
    )

    return profiles, search_query