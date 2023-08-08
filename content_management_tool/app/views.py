from django.shortcuts import render, redirect
from .models import posts, UserProfile
from django.views import generic
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from .models import posts, UserProfile
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.shortcuts import get_object_or_404

    



def home(request):
    post_d = posts.objects.filter(status=1).order_by('-created_on')
    user_profile = None
    if request.user.is_authenticated:
         user_profile = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'home.html', {'post_d': post_d, 'user_profile': user_profile})


@login_required(login_url='login')
def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def privacy(request):
    return render(request,'privacy.html')

@login_required(login_url='login')
def terms(request):
    return render(request,'terms.html')


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        status = int(request.POST['status'])
        created_on = datetime.now()
        
        author = request.user

        post = posts(title=title, slug=title, author=author, created_on=created_on, content=content, status=status)
        post.save()

    
        return redirect('home')

    return render(request, 'create_post.html')

def login(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = "Incorrect password or username"
            messages.error(request, error_message)
            return render(request, 'login.html')
     return render(request,'login.html')



def logout_view(request):
    logout(request, next_page='home')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            return redirect('home')  
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


@method_decorator(login_required(login_url='login'), name='dispatch')
class postdetail(DetailView):
    model = posts
    template_name = "post.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(posts, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = None
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
        context['user_profile'] = user_profile
        return context
    

