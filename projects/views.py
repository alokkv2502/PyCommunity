from django.core import paginator
import json
import sys
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from django.http import JsonResponse
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects
from subprocess import Popen, PIPE, STDOUT,TimeoutExpired
from .models import CodeSnippet
from django.views.decorators.csrf import csrf_exempt
def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def python_terminal(request):
    return render(request, 'terminal.html')

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)

    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})


# views.py



@csrf_exempt
def run_code(request):
    data = json.loads(request.body)
    code = data['code']
    python_executable_path = '"C:\Program Files\Python\python.exe"'
    # Create a temporary file to hold the code
    with open('temp_code.py', 'w') as file:
        file.write(code)
    
    # Run the Python script in a separate process
    proc = Popen(['python3', 'temp_code.py'], stdout=PIPE, stderr=STDOUT)
    try:
        # Set a timeout for execution
        output, _ = proc.communicate(timeout=30)
    except TimeoutExpired:
        proc.kill()
        output, _ = proc.communicate()
        output += b'\nError: Execution time exceeded limit.'

    # It's good practice to remove the temp file here
    # os.remove('temp_code.py')
    
    return JsonResponse({'output': output.decode()})


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        newtags_raw = request.POST.get('newtags')
        
        # Check if 'newtags' is provided to prevent AttributeError
        newtags = newtags_raw.replace(',', " ").split() if newtags_raw else []

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            # Create new tags if they do not exist and add them to the project
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag.strip())
                project.tags.add(tag)
            messages.success(request, 'Project created successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)



@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()

            # Get the tags from the form. If 'newtags' is None, default to an empty string.
            newtags_str = request.POST.get('newtags', '')
            newtags_list = [tag.strip() for tag in newtags_str.replace(',', ' ').split()]

            # Clear existing tags and add new ones
            project.tags.clear()
            for tag_name in newtags_list:
                if tag_name:  # Ensure that tag_name is not an empty string
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)



@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)

@login_required
def get_user_code(request):
    # Get the user's latest code snippet
    code_snippet = CodeSnippet.objects.filter(user=request.user).last()
    
    if code_snippet:
        return JsonResponse({'code': code_snippet.code}, status=200)
    else:
        return JsonResponse({'error': 'No code found.'}, status=404)
