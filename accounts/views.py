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
                "error": "Password must be 8-20 characters"
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
        if user:
            login(request, user)
            return redirect("dashboard")
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
        if occupation and not re.match(r'^[A-Za-z ]+$', occupation):
            messages.error(request, "Occupation should contain only letters")
            return redirect('profile')
        if company and not re.match(r'^[A-Za-z .&]+$', company):
            messages.error(request, "Company name contains invalid characters")
            return redirect('profile')
        if location and not re.match(r'^[A-Za-z ]+$', location):
            messages.error(request, "Location should contain only letters")
            return redirect('profile')
        profile.website = request.POST.get('website')
        profile.about_title = request.POST.get('about_title')
        profile.project_description = request.POST.get('project_description')
        profile.occupation = occupation
        profile.company = company
        profile.location = location
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