from django.shortcuts import render , redirect ,get_object_or_404,HttpResponseRedirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import User
from django.views.generic import DetailView,ListView
from django.db.models import Q
from django.urls import reverse
from blog.models import Post,Comment
# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Your account has been created, you are now able to login")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request,"users/register.html", {"form":form})
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your Profile has been updated")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
               "u_form": u_form,
               "p_form": p_form
               }
    return render(request, "users/profile.html",context)

class PublicProfileDetailView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        follower_connected = get_object_or_404(User, id = self.kwargs['pk'])
        followed = False
        if follower_connected.profile.followers.filter(id=self.request.user.id).exists():
            followed = True
        data['number_of_followers'] = follower_connected.profile.followers.count()
        data['followed'] = followed
        data['number_of_posts'] = Post.objects.filter(author=follower_connected).count()
        data['number_of_comments'] = Comment.objects.filter(author=follower_connected).count()
        return data

def UserFollow(request, pk):
    usertofollow = get_object_or_404(User, id=request.POST.get('user_id'))
    if usertofollow.profile.followers.filter(id=request.user.id).exists():
        usertofollow.profile.followers.remove(request.user)
    else:
        usertofollow.profile.followers.add(request.user)
    return HttpResponseRedirect(reverse('publicprofiles', args=[str(pk)]))

class PublicProfilesListView(ListView):
    model = User
    template_name = "users/public_profile_list.html"
    context_object_name = "users"
    ordering = ["-date_joined"]
    paginate_by = 5
class FollowersPublicProfilesListView(PublicProfilesListView):
    ordering = ["-profile__followers"]
class PublicProfilesSearchResultsPostListView(PublicProfilesListView):
    def get_queryset(self):
        query = self.request.GET.get('users_search_request')
        object_list = User.objects.filter(
            Q(username__icontains=query)
        )
        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("users_search_request")
        return context