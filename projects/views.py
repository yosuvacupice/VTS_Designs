from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectImage
from django.contrib.auth.models import User
from .models import HireInquiry
from notifications.models import Notification

@login_required
def add_project(request):
    if request.method == "POST":
        is_draft = request.POST.get("is_draft")
        if is_draft == "true":
            visibility = "private"
        else:
            visibility = request.POST.get("visibility")
        project = Project.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            tags=request.POST.get("tags"),
            visibility=visibility,
            license=request.POST.get("license"),
            allow_download=True if request.POST.get("allow_download") else False
        )
        for img in request.FILES.getlist("images"):
            ProjectImage.objects.create(project=project, image=img)
        if is_draft == "true":
            return redirect("add_project")
        else:
            return redirect("project_profile", project.id)
    recent_projects = Project.objects.filter(
        user=request.user
    ).order_by("-created_at")[:3]
    return render(request, "projects/add_project.html", {
        "recent_projects": recent_projects
    })

@login_required
def edit_project(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    if request.method == "POST":
        project.title = request.POST.get("title")
        project.category = request.POST.get("category")
        project.description = request.POST.get("description")
        project.tags = request.POST.get("tags")
        project.visibility = request.POST.get("visibility")
        project.license = request.POST.get("license")
        project.allow_download = True if request.POST.get("allow_download") else False
        project.save()
        for img in request.FILES.getlist("images"):
            ProjectImage.objects.create(project=project, image=img)
        return redirect("add_project")
    return render(request, "projects/edit_project.html", {
        "project": project
    })


@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    project.delete()
    return redirect("add_project")
@login_required
def project_profile(request, id):
    all_public_projects = Project.objects.filter(
        visibility="public"
    ).select_related("user").prefetch_related("images").order_by("-created_at")
    return render(request, "projects/project_profile.html", {
        "projects": all_public_projects
    })

@login_required
def hire_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    projects = Project.objects.filter(
        user=user,
        visibility="public"
    ).order_by("-created_at")
    last_project = projects.first()
    return render(request, "projects/hire_profile.html", {
        "profile_user": user,
        "projects": projects,
        "last_project": last_project
    })

@login_required
def hire_now(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        inquiry = HireInquiry.objects.create(
            sender=request.user,
            receiver=receiver,
            hiring_for=request.POST.get("hiring_for"),
            category=request.POST.get("category"),
            budget=request.POST.get("budget"),
            project_description=request.POST.get("project_description"),
            personal_note=request.POST.get("personal_note"),
            hiring_type=request.POST.get("hiring_type"),
        )
        Notification.objects.create(
            user=receiver,
            sender=request.user,
            text=(
                f"{request.user.username} sent you a hire request\n\n"
                f"Hiring For: {inquiry.hiring_for}\n"
                f"Category: {inquiry.category}\n"
                f"Budget: {inquiry.budget}\n"
                f"Type: {inquiry.hiring_type}\n\n"
                f"Project Description:\n{inquiry.project_description}\n\n"
                f"Personal Note:\n{inquiry.personal_note}"
            ),
            hire_inquiry=inquiry
        )
        return redirect("dashboard")
    return render(request, "projects/hire_now.html", {
        "receiver": receiver
    })

@login_required
def hire_inquiry_detail(request, id):
    inquiry = get_object_or_404(
        HireInquiry,
        id=id,
        receiver=request.user
    )
    return render(request, "projects/hire_inquiry_detail.html", {
        "inquiry": inquiry
    })
