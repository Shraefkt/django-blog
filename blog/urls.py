from django.urls import path
from blog import views
from .views import PostListView , SearchResultsPostListView, PostDetailView, PostCreateView, PostUpdateView,PostListViewByPopularity, PostDeleteView, UserPostListView
urlpatterns = [
    path('index/', views.index, name='index'),
    path('likes/',PostListViewByPopularity.as_view(),name = "blog-home-popular"),
    path('',PostListView.as_view(),name = "blog-home"),
    path('about/', views.about,name = "blog-about"),
    path('post/<int:pk>/',PostDetailView.as_view(),name = "post-detail"),
    path('post/new/',PostCreateView.as_view(),name = "post-create"),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name = "post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('user/<str:username>/', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/like/', views.PostLike, name="post-like"),
    path('post/search/', SearchResultsPostListView.as_view(), name="post-search")

]