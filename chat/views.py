from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Message

# ================= MESSAGE LIST =================
@login_required
def compose_message(request):
    if request.method == "POST":
        to_user_id = request.POST.get("to_user")
        text = request.POST.get("text")
        if not to_user_id:
            return render(request, "chat/compose.html", {
                "error": "Please select a user from the list"
            })
        receiver = get_object_or_404(User, id=int(to_user_id))
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            text=text
        )
        return redirect('messages')
    return render(request, 'chat/compose.html')


# ================= SEARCH USERS (AUTOCOMPLETE) =================
@login_required
def search_users(request):
    q = request.GET.get('q', '')
    users = User.objects.filter(
        username__icontains=q
    ).exclude(id=request.user.id)[:5]

    data = [
        {'id': u.id, 'username': u.username}
        for u in users
    ]
    return JsonResponse(data, safe=False)

@login_required
def messages_view(request):
    all_messages = Message.objects.filter(
        receiver=request.user
    ).order_by('-created_at')
    new_messages = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).order_by('-created_at')
    return render(request, 'chat/messages.html', {
        'all_messages': all_messages,
        'new_messages': new_messages,
    })

@login_required
def message_detail(request, id):
    message = get_object_or_404(Message, id=id, receiver=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'chat/message_detail.html', {
        'message': message
    })