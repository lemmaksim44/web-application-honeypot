from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('neural/', views.neural_page, name='neural'),
    path('about/', views.about_page, name='about'),
    path('secret/', views.secret_page, name='secret'),
]