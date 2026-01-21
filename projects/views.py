from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from .models import Project, ProjectImage, HireInquiry
from notifications.models import Notification
import uuid
import re

MAX_IMAGE_SIZE = 10 * 1024 * 1024

@login_required
@never_cache
def add_project(request):
    if request.method == "POST":
        action = request.POST.get("action")
        from_dashboard = request.POST.get("from_dashboard")
        token = uuid.uuid4()

        images = request.FILES.getlist("images")
        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "").strip()
        description = request.POST.get("description", "").strip()
        visibility_input = request.POST.get("visibility", "public")

        recent_projects = Project.objects.filter(
            user=request.user
        ).order_by("-created_at")[:3]

        if not title:
            return render(request, "projects/add_project.html", {
                "recent_projects": recent_projects,
                "error": "Project title is required"
            })

        if not category:
            return render(request, "projects/add_project.html", {
                "recent_projects": recent_projects,
                "error": "Category is required"
            })

        if action == "publish" and not from_dashboard and not description:
            return render(request, "projects/add_project.html", {
                "recent_projects": recent_projects,
                "error": "Description is required"
            })

        if action == "publish" and not images:
            return render(request, "projects/add_project.html", {
                "recent_projects": recent_projects,
                "error": "At least one image is required"
            })

        for img in images:
            if img.size > MAX_IMAGE_SIZE:
                return render(request, "projects/add_project.html", {
                    "recent_projects": recent_projects,
                    "error": "Each image must be under 10MB"
                })

        if action == "draft":
            is_draft = True
            final_visibility = "private"
        else:
            is_draft = False
            final_visibility = visibility_input

        project = Project.objects.create(
            user=request.user,
            title=title,
            category=category,
            description=description or "",
            tags=clean_tags(request.POST.get("tags", "")),
            visibility=final_visibility,
            is_draft=is_draft,
            license=request.POST.get("license", "all"),
            allow_download=True if request.POST.get("allow_download") else False,
            publish_token=token
        )

        for img in images:
            ProjectImage.objects.create(project=project, image=img)

        if not is_draft:
            return redirect("project_profile", project.id)

        return redirect("add_project")

    recent_projects = Project.objects.filter(
        user=request.user
    ).order_by("-created_at")[:3]

    return render(request, "projects/add_project.html", {
        "recent_projects": recent_projects
    })

def clean_tags(raw_tags):
    tag_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
    unique_tags = []
    for t in tag_list:
        if len(t) < 3:
            continue
        if not re.match(r'^[A-Za-z ]+$', t):
            continue
        if t.lower() not in [x.lower() for x in unique_tags]:
            unique_tags.append(t)
    return ", ".join(unique_tags)

@login_required
def edit_project(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)

    if request.method == "POST":
        images = request.FILES.getlist("images")
        action = request.POST.get("action")

        for img in images:
            if img.size > MAX_IMAGE_SIZE:
                return render(request, "projects/edit_project.html", {
                    "project": project,
                    "error": "Image size must be less than 10MB"
                })

        project.title = request.POST.get("title", "").strip()
        project.category = request.POST.get("category", "").strip()
        project.description = request.POST.get("description", "").strip()
        project.tags = clean_tags(request.POST.get("tags", ""))

        if action == "publish":
            project.visibility = "public"
        else:
            project.visibility = "private"

        project.license = request.POST.get("license", project.license)
        project.allow_download = bool(request.POST.get("allow_download"))
        project.save()

        if images:
            project.images.all().delete()

            for img in images:
                ProjectImage.objects.create(project=project, image=img)

        if project.visibility == "public":
            return redirect("project_profile", project.id)

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

ALLOWED_CATEGORIES = ["UI Design", "Mobile App", "Web App"]
@login_required
def hire_now(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        category = request.POST.get("category")
        budget = request.POST.get("budget")
        if category not in ALLOWED_CATEGORIES:
            return render(request, "projects/hire_now.html", {
                "receiver": receiver,
                "error": "Please select a valid category"
            })
        if not budget or not budget.isdigit():
            return render(request, "projects/hire_now.html", {
                "receiver": receiver,
                "error": "Please enter a valid numeric budget"
            })
        inquiry = HireInquiry.objects.create(
            sender=request.user,
            receiver=receiver,
            hiring_for=request.POST.get("hiring_for"),
            category=category,
            budget=budget,
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
