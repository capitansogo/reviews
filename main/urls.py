from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rewiews/', views.place, name='place'),
    path('about/', views.about, name='about'),
]
