from .models import Project, Tag
# going to use Q lookup to use "OR" in search
from django.db.models import Q


def searchProjects(request):
    search_query = ''
    # extract search_query from frontend
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # this is ManytoMany model
    tags = Tag.objects.filter(name__icontains=search_query)
    
    # going to use Q lookup to use "OR" in search '|' will say OR
    # using icontains because we don't need case senstivity
    # using distinct() because skills lookup is giving multiple entries for same instance
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return projects, search_query