from django.contrib import admin
from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('log_in/', views.log_in, name='login'),
    path('register/#login', views.signin, name='signin'),
    path('login/#register', views.register_attempt, name='register_attempt'),
    path('token/', views.token_send, name='token_send'),
    path('success/', views.success, name='success'),
    path('verify/<uidb64>/<auth_token>/', views.verify, name='verify'),
    path('error/', views.error_page, name='error')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
