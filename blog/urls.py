from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (PostListView ,
                    PostListViewByPopularity,
                    SearchResultsPostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserCommentListView,
                    UserPostListView,
                    UserLikedPostsView,
                    TagListView,
                    )
urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about,name = "blog-about"),
    path('',PostListView.as_view(),name = "blog-home"),
    path('post/search/', SearchResultsPostListView.as_view(), name="post-search"),
    path('likes/',PostListViewByPopularity.as_view(),name = "blog-home-popular"),
    path('post/<int:pk>/',PostDetailView.as_view(),name = "post-detail"),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name = "post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('post/new/',PostCreateView.as_view(),name = "post-create"),
    path('user_posts/<str:username>/', UserPostListView.as_view(), name="user-posts"),
    path('user_liked_posts/<str:username>/', UserLikedPostsView.as_view(), name="user-liked-posts"),
    path('user_comments/<str:username>/', UserCommentListView.as_view(), name="user-comments"),
    path('tags/<slug:slug>/',TagListView.as_view(), name = "tags"),
    path('post/<int:pk>/like/', views.PostLike, name="post-like"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)