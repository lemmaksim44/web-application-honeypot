from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('neural/', views.neural_page, name='neural'),
    path('about/', views.about_page, name='about'),

    # Главная страница. Тема: Debug
    # HTML
    path('internal/', views.secret_page, name='secret'),
    path('debug/', views.secret_page, name='secret'),
    path('trace/', views.secret_page, name='secret'),
    # JS
    path('debug-console/', views.secret_page, name='secret'),
    path('test-panel/', views.secret_page, name='secret'),
    path('logs/', views.secret_page, name='secret'),

    # Страница ИИ. Тема: Admin
    # HTML
    path('administrator/', views.secret_page, name='secret'),
    path('control-panel/', views.secret_page, name='secret'),
    path('admin-dashboard/', views.secret_page, name='secret'),
    # JS
    path('administrator-panel/', views.secret_page, name='secret'),
    path('admin-panel/', views.secret_page, name='secret'),
    path('management/', views.secret_page, name='secret'),

    # Страница обратной связи. Тема: Config
    # HTML
    path('app-config/', views.secret_page, name='secret'),
    path('site-settings/', views.secret_page, name='secret'),
    path('settings/', views.secret_page, name='secret'),
    # JS
    path('config/', views.secret_page, name='secret'),
    path('env/', views.secret_page, name='secret'),
    path('system-config/', views.secret_page, name='secret'),

    # Страница о нас. Тема: # Backup
    # HTML
    path('archive/', views.secret_page, name='secret'),
    path('database-dump/', views.secret_page, name='secret'),
    path('backup-old/', views.secret_page, name='secret'),
    # JS
    path('backup/', views.secret_page, name='secret'),
    path('db-backup/', views.secret_page, name='secret'),
    path('data-dump/', views.secret_page, name='secret'),

]