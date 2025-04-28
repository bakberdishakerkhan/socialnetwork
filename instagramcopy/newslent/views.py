from django.shortcuts import render, redirect

from .models import News, PostAttachment
from .forms import PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def newslist(request):
    news = News.objects.all().order_by('-publication_date')
    return render(request, 'newslent/post_list.html', {'posts': news})

def postdetails(request, pid):
    news = News.objects.get(pk=pid)
    images = PostAttachment.objects.filter(post_id = pid)
    return render(request, 'newslent/details_page.html', {'post': news, 'images': images})
@login_required
def addPost(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        att = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            for img in att:
                PostAttachment.objects.create(post_id = post.pk, image=img)
        return redirect(to='news:details', pid=post.pk)
    return render(request, 'newslent/newpost.html', {'form':form})
@login_required
def editPost(request, pid):
    post = News.objects.get(pk=pid)
    post_att = PostAttachment.objects.filter(post_id=pid)

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, instance=post)
        
        if form.is_valid():
            post = form.save(commit=False)
            att = request.FILES.getlist('images')
            for img in att:
                PostAttachment.objects.create(post_id = post.pk, image=img)
            chosen = request.POST.getlist('attachments')
            for img_id in chosen:
                PostAttachment.objects.get(pk=int(img_id)).delete()
            post.edited = True
            post.save()
           
        return redirect(to='news:details', pid=post.pk)
    return render(request, 'newslent/editpost.html', {'form':form, "post_att":post_att})
@login_required
def deletePost(request, pid):
    post = News.objects.get(pk=pid)
    post.delete()
    return redirect(to='news:news_list')