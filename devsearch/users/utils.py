from .models import Profile, Skill
# going to use Q lookup to use "OR" in search
from django.db.models import Q


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