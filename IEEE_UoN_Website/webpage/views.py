from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html', {'navbar': 'about'})


def admin(request):
    return render(request, 'admin.html', {'navbar': 'admin'})


def blogs(request):
    return render(request, 'blogs.html', {'navbar': 'blogs'})


def contact(request):
    return render(request, 'contact.html', {'navbar': 'contact'})


def exec_team(request):
    return render(request, 'exec_team.html', {'navbar': 'exec_team'})


def gallery(request):
    return render(request, 'gallery.html', {'navbar': 'gallery'})


def signup_login(request):
    return render(request, 'signup_login.html')


def home_user(request):
    return render(request, 'home_user.html')


def home_exec(request):
    return render(request, 'home_exec.html')


def log_out(request):
    return render(request, 'log_out.html')
