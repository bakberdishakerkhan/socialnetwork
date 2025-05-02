from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.newslist, name='news_list'), 
    path('<int:pid>/', views.postdetails, name='details'),
    path('add/', views.addPost, name='add-new-post'),
    path('<int:pid>/edit/', views.editPost, name='edit-post' ),
    path('<int:pid>/delete/', views.deletePost, name='delete-post' ),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add-comment'),

]