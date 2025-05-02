
from django.shortcuts import render, get_object_or_404
from user.models import User
from django.contrib.auth.decorators import login_required

@login_required
def select_user(request):
    users = User.objects.exclude(id=request.user.id) 
    return render(request, 'chat/select_user.html', {'users': users})

@login_required
def chat_view(request, other_user_id):
    other_user = User.objects.get(id=other_user_id)
    return render(request, 'chat/chat.html', {'other_user': other_user})
