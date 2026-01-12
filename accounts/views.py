from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile

# ---------- LOGIN ----------
def login_view(request):
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
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid email or password"
            })
    return render(request, "accounts/login.html")

# ---------- PROFILE ----------
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.website = request.POST.get('website')
        profile.about_title = request.POST.get('about_title')
        profile.project_description = request.POST.get('project_description')
        profile.occupation = request.POST.get('occupation')
        profile.company = request.POST.get('company')
        profile.location = request.POST.get('location')
        profile.save()
        return redirect('dashboard')
    return render(request, 'accounts/profile.html', {
        'profile': profile
    })

from django.http import JsonResponse
from django.contrib.auth.models import User
@login_required
def search_users(request):
    q = request.GET.get("q", "")
    users = User.objects.filter(
        username__icontains=q
    )[:5]
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "username": u.username
        })
    return JsonResponse(data, safe=False)
