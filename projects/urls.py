from django.urls import path
from . import views
from .views import submission_list
urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>/', views.project, name="project"),
    path('code/', views.code_list, name='code-list'),
    path('create-project/', views.createProject, name="create-project"),
    path('code/<int:pk>/', views.single_code, name='single-code'),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),

    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
    path('submissions/', submission_list, name='submissions'),
    path('terminal/', views.python_terminal, name='python_terminal'),
    path('run_code/', views.run_code, name='run_code'),
    path('create-code/', views.createCode, name='create-code'),
    path('update-code/<int:pk>/', views.updateCode, name='update-code'),
    path('delete-code/<int:pk>/', views.deleteCode, name='delete-code'),
]
