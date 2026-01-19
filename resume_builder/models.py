from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Signup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=True)

def _str_(self):
        return self.user.username


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # STEP 1 – Personal
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    TEMPLATE_CHOICES = (
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('minimal', 'Minimal'),
    )
    template = models.CharField(
        max_length=20,
        choices=TEMPLATE_CHOICES,
        default='classic'
    )

    # STEP 4 – Skills (FIXED)
    skills = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.full_name


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    college = models.CharField(max_length=150)
    year = models.CharField(max_length=10)


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    description = models.TextField()



class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    html_file = models.FileField(
        upload_to='resume_templates/',
        blank=True,
        null=True
    )

    preview_image = models.ImageField(
        upload_to='template_previews/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
