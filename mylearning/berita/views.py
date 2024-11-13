from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pesan berhasil terkirim. Kamu akan menerima balasan melalui email.')
            return redirect('contact')
    return render(request, 'contact.html')


def guest(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'news.html', {'posts':posts})


def detail(request, slug):
    posts = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.exclude(slug=slug).order_by('?')[:3]
    comments = posts.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = posts
            comment.user = request.user
            comment.save()
            messages.success(request, "Komentar berhasil ditambahkan!")
            return redirect('detail', slug=posts.slug)
    else:
        form = CommentForm()

    return render(request, 'detail.html', {
        'posts': posts,
        'comments': comments,
        'form': form,
        'related_posts': related_posts})


def berita(request):
    posts = Post.objects.filter(category="berita")
    return render(request, 'berita.html', {'posts': posts})
    

def bursa_transfer(request):
    posts = Post.objects.filter(category="bursa_transfer")
    return render(request, 'bursa_transfer.html', {'posts': posts})


def tips(request):
    posts = Post.objects.filter(category="tips")
    return render(request, 'tips.html', {'posts': posts})


def turnamen(request):
    posts = Post.objects.filter(category="turnamen")
    return render(request, 'turnamen.html', {'posts': posts})


def search(request):
    searchQuery = request.GET.get("keyword")
    posts = Post.objects.filter(title__icontains=searchQuery)
    return render(request, 'result.html', {'posts': posts, 'query': searchQuery})


@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    userLevel = request.user
    if userLevel.is_staff:
        return render(request, 'home.html', {'posts':posts})  
    else:
        return render(request, 'news.html', {'posts':posts})  
    

@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile_edit.html', {'form': form})


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
                
                if user.is_staff:
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('home')
                else:
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('guest')
            else:
                messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def view_404(request, exception):
    return render(request, "404.html", status=404)