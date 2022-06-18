from django.urls import path
from . import views

# to generate JSON webtoken & refreshtoken using jwt.io ie, simpleJWT
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),

    # to generate JSON webtoken & refreshtoken using jwt.io ie, simpleJWT
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
