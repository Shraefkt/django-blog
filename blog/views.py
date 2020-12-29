from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView , DetailView, CreateView, UpdateView ,DeleteView
from .models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import NewCommentForm
from django.db.models import Q,Count
from taggit.models import Tag
from django.template.defaultfilters import slugify
# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_posts = Post.objects.all().count()
    num_comments = Comment.objects.all().count()

    # The 'all()' is implied by default.
    num_users = User.objects.count()
    main_featured_post = Post.objects.get(pk=1)
    common_tags = Post.tags.most_common()[:4]
    context = {
        'num_posts': num_posts,
        'num_comments': num_comments,
        'num_users': num_users,
        'main_featured_post' : main_featured_post,
        'common_tags' : common_tags,
    }

    return render(request, 'blog/index.html', context=context)

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["common_tags"] = Post.tags.most_common()[:4]
        return context
    def get_queryset(self):
        return Post.objects.filter(is_published=True)
class PostListViewByPopularity(PostListView):
    ordering = ["-likes"]

class SearchResultsPostListView(PostListView):
    def get_queryset(self):
        query = self.request.GET.get('blogs_search_request')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) , is_published=True
        )
        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("blogs_search_request")
        return context

class TagListView(ListView):
    model = Post
    template_name = "blog/post_sort.html"
    context_object_name = "posts"
    paginate_by = 5
    sort_by = "-date_posted"

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        return Post.objects.filter(tags=tag, is_published=True).order_by("-date_posted")
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        data["common_tags"] = Post.tags.most_common()[:4]
        data["title"] = f"Tagged: {tag}"
        return data

class UserPostListView(ListView):
    model = Post
    template_name = "blog/post_sort.html"
    context_object_name = "posts"
    paginate_by = 5
    sort_by = "-date_posted"
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        if user == self.request.user:
            return Post.objects.filter(author=user).order_by("-date_posted")
        else:
            return Post.objects.filter(author=user,is_published = True).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        data["title"] = f"Posts by {user}"
        data["common_tags"] = Post.tags.most_common()[:4]
        data["user_is_author"] = True if self.request.user == user else False
        return data

class UserCommentListView(ListView):
    model = Comment
    template_name = "blog/user_comments.html"
    context_object_name = "comments"
    paginate_by = 5
    sort_by = "-date_posted"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Comment.objects.filter(author=user).order_by("-date_posted")

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        data["reading_time"] = likes_connected.reading_time()
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        comments_connected = Comment.objects.filter(
            blogpost_connected=self.get_object()).order_by('-date_posted')
        data["post_tags"] = Post.tags.all()
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  blogpost_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ["cover_image","title","tagline", "content","notes","tags","is_published"]
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ["cover_image","title","tagline", "content","notes","tags","is_published"]
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = "/"
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def about(request):
    context = {}
    return render(request, "blog/about.html",context)

class UserLikedPostsView(ListView):
    model = Post
    template_name = "blog/post_sort.html"
    context_object_name = "posts"
    paginate_by = 5
    sort_by = "-date_posted"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(likes = user, is_published=True).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        data["title"] = f"{user}'s liked posts"
        data["common_tags"] = Post.tags.most_common()[:4]
        return data