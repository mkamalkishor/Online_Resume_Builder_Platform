"""
URL configuration for Online_Resume_Builder_Platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include
from resume_builder.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='home'),
    path('about/',about,name='about'),
    path('feedback/',feedback,name='feedback'),
    path('contact/',contact,name='contact'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('dashboard/',dashboard,name='dashboard'),
    path('create_resume/',create_resume,name='create_resume'),
    path('resume_list',resume_list,name='resume_list'),
    path('my_resume',my_resume,name='my_resume'),

    path('resume/<int:id>/',resume_view, name='resume_view'),
    path('resume/<int:id>/pdf/',resume_pdf, name='resume_pdf'),
    path('resume/<int:id>/edit/',edit_resume, name='edit_resume'),
    path('resume/<int:id>/delete/', delete_resume, name='delete_resume'),
    path('logout/', Logout, name='logout'),
    
 


# admin
    path('admin_login', admin_login, name='admin_login'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('add_templates', add_templates, name='add_templates'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
