from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def guest(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'news.html', {'posts':posts})

def detail(request, slug):
    posts = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.exclude(slug=slug).order_by('?')[:3]

    return render(request, 'detail.html', {
        'posts': posts,
        'related_posts': related_posts})

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts':posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@login_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'add_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})


# View untuk Signup
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun {username} berhasil dibuat! Silakan login.')
            return redirect('login')
        else:
            # Jika form tidak valid, tampilkan pesan error
            messages.error(request, 'Terjadi kesalahan. Silakan periksa form dan coba lagi.')
            print(form.errors)  # Mencetak error form ke console untuk debugging
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# View untuk Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Selamat datang, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# View untuk Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('login')