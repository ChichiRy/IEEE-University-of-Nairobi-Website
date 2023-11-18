from django.urls import path

from webpage import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('manage/', views.admin, name='admin'),
    path('blogs/', views.blogs, name="blogs"),
    path('contact/', views.contact, name='contact'),
    path('team/', views.exec_team, name="exec_team"),
    path('gallery/', views.gallery, name='gallery'),
    path('login/', views.signup_login, name="signup_login"),
    path('home_user/', views.home_user, name="home_user"),
    path('home_exec/', views.home_exec, name='home_exec'),
    path('out/', views.log_out, name="log_out")
]
