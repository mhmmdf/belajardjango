from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class Post(models.Model):
    # Pilihan kategori
    BERITA = 'berita'
    TURNAMEN = 'turnamen'
    BURSA_TRANSFER = 'bursa_transfer'
    TIPS = 'tips'
    
    CATEGORY_CHOICES = [
        (BERITA, 'Berita'),
        (TURNAMEN, 'Turnamen'),
        (TIPS, 'Tips'),
        (BURSA_TRANSFER, 'Bursa Transfer'),
    ]
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=BERITA,  # Default kategori adalah Berita
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title)
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    
class Contact(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pesan masuk dari: {self.fullname}"