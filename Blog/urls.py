from django.urls import path

from Blog import views

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('posts/<str:category_name>/', views.post_list, name='post-list-category'),
    path('posts/detail/<int:post_id>/', views.post_detail, name='post-detail'),
    path('posts/detail/<int:post_id>/<str:message>/', views.post_detail, name='post-detail-message'),

    path('about/', views.about, name='about'),
]
