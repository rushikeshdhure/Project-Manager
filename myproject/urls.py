"""project_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from myapp.views import UserRegisterView,UserListView,ClientListView,ClientDetailView,ProjectCreateView,ClientUpdateView,ClientDeleteView
from myapp.views import UserLoginView,UserLogoutView,get_all_data,ClientRegisterView,ProjectListView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('myapp.urls')),
    # path('', home),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', UserRegisterView.as_view(), name='create-user'),
    path('userlist/', UserListView.as_view(), name='user-list'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('client/', ClientRegisterView.as_view(), name='create-client'),
    path('clientslist/', ClientListView.as_view(), name='client-list'),
    path('cdetails/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='update-client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete-client'),

    path('projects/', ProjectCreateView.as_view(), name='create-project'),
    path('projectslist/', ProjectListView.as_view(), name='project-list'),

    path('data/', get_all_data, name='get_all_data'),

    
  
]



