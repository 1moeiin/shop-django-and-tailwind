from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# Manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DR', 'در انتظار'
        PUBLISHED = 'PB', 'منتشر شده'
        REJECTED = 'RJ', 'رد شده'
    
    
    # relationship
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='دسته بندی')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    inventory = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    weight = models.PositiveIntegerField(default=0, verbose_name="وزن")
    price = models.PositiveIntegerField(default=0, verbose_name="قیمت")
    off = models.PositiveIntegerField(default=0, verbose_name="تخفیف")
    new_price = models.PositiveIntegerField(default=0, verbose_name="قیمت پس از تخفیف")

    # date 
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")
    
    # status
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    # managers
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('shop:product_details', args=[self.id, self.slug])


class Ticket(models.Model):
    
    message = models.TextField()
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
    
    def __str__(self):
        return f"{self.name}: {self.product}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="post_images/")
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
    
    def __str__(self):
        return self.title
    
    
class ProductFeature(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام ویژگی')
    value = models.CharField(max_length=255, verbose_name='مقدار ویژگی')
    product = models.ForeignKey(Post, related_name='features', on_delete=models.CASCADE, verbose_name='محصول')

    def __str__(self):
        return self.name + ":" + self.value