from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
import re

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if len(email) > 254:
            return render(request, "accounts/login.html", {
                "error": "Email is too long"
            })

        if len(password) < 8 or len(password) > 20:
            return render(request, "accounts/login.html", {
                "error": "Password must be 8–20 characters"
            })

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user and not user.is_staff:
            login(request, user)
            return redirect("dashboard")

        elif user and user.is_staff:
            return render(request, "accounts/login.html", {
                "error": "User access only"
            })

        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid email or password"
            })

    return render(request, "accounts/login.html")


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        occupation = request.POST.get('occupation', '').strip()
        company = request.POST.get('company', '').strip()
        location = request.POST.get('location', '').strip()
        website = request.POST.get('website', '').strip()
        about_title = request.POST.get('about_title', '').strip()
        project_description = request.POST.get('project_description', '').strip()

        if not any([
            occupation,
            company,
            location,
            website,
            about_title,
            project_description
        ]):
            messages.error(request, "Please fill at least one field")
            return redirect('profile')

        if occupation and not re.match(r'^[A-Za-z ]+$', occupation):
            messages.error(request, "Occupation should contain only letters")
            return redirect('profile')

        if company and not re.match(r'^[A-Za-z .&]+$', company):
            messages.error(request, "Company name contains invalid characters")
            return redirect('profile')

        if location and not re.match(r'^[A-Za-z ]+$', location):
            messages.error(request, "Location should contain only letters")
            return redirect('profile')

        profile.occupation = occupation
        profile.company = company
        profile.location = location
        profile.website = website
        profile.about_title = about_title
        profile.project_description = project_description
        profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, 'accounts/profile.html', {
        'profile': profile
    })


@login_required
def search_users(request):
    q = request.GET.get("q", "")
    users = User.objects.filter(username__icontains=q)[:5]
    data = [{"id": u.id, "username": u.username} for u in users]
    return JsonResponse(data, safe=False)

def landing_page(request):
    return render(request, "accounts/landing.html")

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def admin_login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user and user.is_staff:
            login(request, user)
            return redirect("/dashboard/")
        else:
            return render(request, "accounts/admin_login.html", {
                "error": "Admin access only"
            })

    return render(request, "accounts/admin_login.html")
