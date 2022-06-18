# from django.http import JsonResponse
from telnetlib import AUTHENTICATION
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project


# using decorators from rest_framework
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},
        
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]

    return Response(routes)


@api_view(['GET'])
# this is for getting jwt AUTHENTICATION 
@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    # serializer is a object on ProjectSerializer to return many=True ie, multiple
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# this is for getting jwt AUTHENTICATION 
@permission_classes([IsAuthenticated])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # serializer is a object on ProjectSerializer to return many=True ie, multiple
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)