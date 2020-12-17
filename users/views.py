from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import User
from django.views.generic import DetailView,ListView
from django.db.models import Q
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
class PublicProfilesListView(ListView):
    model = User
    template_name = "users/public_profile_list.html"
    context_object_name = "users"
    #ordering = ["-date_posted"]
    paginate_by = 5
class PublicProfilesSearchResultsPostListView(PublicProfilesListView):
    def get_queryset(self):
        query = self.request.GET.get('users_search_request')
        object_list = User.objects.filter(
            Q(username__icontains=query)
        )
        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("usersblogs_search_request")
        return context