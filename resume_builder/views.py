from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.loader import get_template
import os
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib.auth.decorators import login_required




def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def feedback(request):
    return render(request, 'feedback.html')

def contact(request):
    return render(request, 'contact.html')

from django.contrib import auth
from django.shortcuts import render, redirect

def login(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is None:
            error = "invalid"
        else:
            auth.login(request, user)
            return redirect('dashboard')  
    return render(request, 'login.html', {'error': error})


def register(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        
        try:
            user=User.objects.create_user(username=username,email=email,password=password)
            Signup.objects.create(user=user,mobile=phone)
            error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'register.html',d)  


@login_required              
def  dashboard(request):
    resumes = Resume.objects.filter(user=request.user)

    context = {
        'resumes': resumes,
        'resume_count': resumes.count(),
        'template_count': Resume.TEMPLATE_CHOICES.__len__(),  # dynamic
    }
    return render(request, 'dashboard.html', context)

    


@login_required
def create_resume(request):
    if request.method == "POST":

        resume = Resume.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            image=request.FILES.get("image"),
            country=request.POST.get("country"),
            state=request.POST.get("state"),
            city=request.POST.get("city"),
            skills=request.POST.get("skills"),
            template=request.POST.get("template") 
        )

        Education.objects.create(
            resume=resume,
            degree=request.POST.get("degree"),
            college=request.POST.get("college"),
            year=request.POST.get("year"),
        )

        Experience.objects.create(
            resume=resume,
            company=request.POST.get("company"),
            role=request.POST.get("role"),
            description=request.POST.get("experience"),
        )

        return redirect("resume_list")   # ✅ ALWAYS return after POST

    # ✅ ALWAYS return for GET request
    return render(request, "create_resume.html")
   

def resume_list(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-id')

    return render(request, 'my_resume.html', {
        'resumes': resumes
    })


@login_required
def resume_pdf(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    education = Education.objects.filter(resume=resume)
    experience = Experience.objects.filter(resume=resume)
    
    image_path = ""
    if resume.image:
        image_path = os.path.join(settings.MEDIA_ROOT, resume.image.name)

    template = get_template('resume_pdf.html')
    html = template.render({
        'resume': resume,
        'education': education,
        'experience': experience,
        'image_path': image_path,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse("Error generating PDF")

    return response



@login_required


        
            
            


def calculate_profile_strength(resume):
    score = 0
    total = 6

    if resume.full_name: score += 1
    if resume.email: score += 1
    if resume.phone: score += 1
    if resume.skills: score += 1
    if resume.image: score += 1
    if resume.country: score += 1

    return int((score / total) * 100)


# Create your views here
def my_resume(request):
    return render(request, 'my_resume.html')

# 🔥 ADD THIS AT THE TOP (below imports)

TEMPLATE_MAP = {
    'classic': 'resume/templates/classic.html',
    'modern': 'resume/templates/modern.html',
    'minimal': 'resume/templates/minimal.html',
}
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume, Education, Experience

# ✅ TEMPLATE CONFIG (GLOBAL)
TEMPLATE_MAP = {
    'classic': 'resume_templates/classic.html',
    'modern': 'resume_templates/modern.html',
    'minimal': 'resume_templates/minimal.html',
}

@login_required
def resume_view(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    education = Education.objects.filter(resume=resume)
    experience = Experience.objects.filter(resume=resume)

    template_name = TEMPLATE_MAP.get(
        resume.template,
        'reume_templates/classic.html'
    )

    return render(request, template_name, {
        'resume': resume,
        'education': education,
        'experience': experience,
    })


@login_required
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    resume.country = request.POST.get("country")
    resume.state = request.POST.get("state")
    resume.city = request.POST.get("city")
    education = Education.objects.filter(resume=resume).first()
    experience = Experience.objects.filter(resume=resume).first()

    if request.method == "POST":

        # Update Resume
        resume.full_name = request.POST.get("full_name")
        resume.email = request.POST.get("email")
        resume.phone = request.POST.get("phone")
        resume.country = request.POST.get("country")
        resume.state = request.POST.get("state")
        resume.city = request.POST.get("city")
        resume.skills = request.POST.get("skills")
        resume.template = request.POST.get("template")

        if request.FILES.get("image"):
            resume.image = request.FILES.get("image")

        resume.save()

        # Update Education
        if education:
            education.degree = request.POST.get("degree")
            education.college = request.POST.get("college")
            education.year = request.POST.get("year")
            education.save()

        # Update Experience
        if experience:
            experience.company = request.POST.get("company")
            experience.role = request.POST.get("role")
            experience.description = request.POST.get("experience")
            experience.save()

        return redirect('resume_list')

    return render(request, 'edit_resume.html', {
        'resume': resume,
        'education': education,
        'experience': experience,
    })


@login_required
def delete_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)

    if request.method == "POST":
        resume.delete()
        return redirect('resume_list')

    return render(request, 'delete.html', {
        'resume': resume
    })

def Logout(request):
    auth.logout(request)
    return redirect('login')


def admin_login(request):

    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user and user.is_staff:
            login(request)
            return redirect('admin_dashboard')
        else:
            error = "Invalid admin credentials"

    return render(request, 'admin_login.html', {'error': error})
    
def admin_dashboard(request):
    return render(request, 'admin/admin_dashbord.html')

def add_templates(request):
    from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib.auth.decorators import user_passes_test
from .models import ResumeTemplate


def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def add_template(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        is_active = request.POST.get("is_active") == "on"
        is_premium = request.POST.get("is_premium") == "on"

        preview_image = request.FILES.get("preview_image")
        html_file = request.FILES.get("html_file")

        ResumeTemplate.objects.create(
            name=name,
            slug=slugify(name),
            description=description,
            is_active=is_active,
            is_premium=is_premium,
            preview_image=preview_image,
            html_file=html_file
        )

        return redirect('admin/admin_dashboard')
    return render(request, 'admin/add_template.html')

