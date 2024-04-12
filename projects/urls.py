from django.urls import path
from . import views
from .views import submission_list
urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>/', views.project, name="project"),

    path('create-project/', views.createProject, name="create-project"),

    path('update-project/<str:pk>/', views.updateProject, name="update-project"),

    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
    path('submissions/', submission_list, name='submissions'),
    path('terminal/', views.python_terminal, name='python_terminal'),
    path('run_code/', views.run_code, name='run_code'),
]
