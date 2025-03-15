from django.contrib import admin
from django.urls import path, include

from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('technology/', views.technology, name='technology'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
]
