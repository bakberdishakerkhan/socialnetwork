from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Follow
from .forms import RegistrationForm, UserLoginForm
from django.core.mail import EmailMessage
from .token import TokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

acc_active_token = TokenGenerator()

def registration(request):
    if request.method != 'POST':
        form = RegistrationForm()
    else:
        print('POST запрос получен')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('Форма валидна')
            email_address = form.cleaned_data.get('email')

            try:
                exist_user = User.objects.get(email=email_address)
                if not exist_user.is_active:
                    exist_user.delete()
                else:
                    return render(request, '#', {'error': 'данный пользователь уже существует'})
            except User.DoesNotExist:
                pass

            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} сохранён')

            # Отправка письма
            to_email = email_address
            mail_subject = 'Ссылка на активацию аккаунта'
            message = render_to_string('auth/acc_active_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'domain': get_current_site(request),
                'token': acc_active_token.make_token(user)
            })
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, 'auth/registr_email_message.html', {'email': email_address})
        else:
            print('Форма не валидна', form.errors)

    return render(request, 'auth/registration.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None
    if user is not None and acc_active_token.check_token(user, token):
        time_elapsed = timezone.now()-user.date_joined
        if time_elapsed.total_seconds()<900:
            user.is_active = True
            user.save()
            return render(request, 'auth/result_activation.html', {'is_active': True})
        else:
             return render(request, 'auth/result_activation.html', {'is_active': False})
        
def user_login(request):
    if request.method != 'POST':
        form = UserLoginForm()
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('news:news_list')
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('news:news_list')


@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    
    # Подсчет подписок и подписчиков
    following_count = Follow.objects.filter(follower=profile_user).count()  # Количество подписок
    followers_count = Follow.objects.filter(following=profile_user).count()  # Количество подписчиков

    return render(request, 'user/profile.html', {
        'profile_user': profile_user,
        'is_following': is_following,
        'following_count': following_count,
        'followers_count': followers_count
    })

@require_POST
@login_required
def toggle_follow(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    if Follow.objects.filter(follower=request.user, following=profile_user).exists():
        # Отписка
        Follow.objects.filter(follower=request.user, following=profile_user).delete()
    else:
        # Подписка
        Follow.objects.get_or_create(follower=request.user, following=profile_user)

    return redirect('user:profile', user_id=profile_user.id)



