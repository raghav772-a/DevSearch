from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.utils import searchProject,paginateProjects
from .models import Project,Tag
from .forms import ProjectForm,ReviewForm



def projects(request):
    projects,search_query=searchProject(request)
    custom_range,projects=paginateProjects(request,projects,6)


  
    context={'projects':projects,'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)


def project(request,pk):
    projectobj=Project.objects.get(id=pk)
    form=ReviewForm()

    if request.method== 'POST':
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=projectobj
        review.owner=request.user.profile
        review.save()

        projectobj.getVoteCount
        
        messages.success(request,'Your review was successfully submitted')
        return redirect('project', pk=projectobj.id)

    return render(request,'projects/single-project.html',{'project':projectobj,'form':form})

@login_required(login_url="login")
def createProject(request):
    profile=request.user.profile
    form=ProjectForm()
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            return redirect('projects')
    context={'form':form}
    return render(request,'projects/project_form.html',context)



@login_required(login_url="login")
def updateProject(request,pk):
    project=Project.objects.get(id=pk)
    form=ProjectForm(instance=project)
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context={'form':form}
    return render(request,'projects/project_form.html',context)


@login_required(login_url="login")
def deleteProject(request,pk):
    project=Project.objects.get(id=pk)
    if request.method=='POST':
        project.delete()
        return redirect('projects')
    context={'object':project}
    return render(request,'projects/delete_template.html',context)








