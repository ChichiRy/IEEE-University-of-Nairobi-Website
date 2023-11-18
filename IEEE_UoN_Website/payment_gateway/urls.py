from django.urls import path
from payment_gateway import views

urlpatterns = [
    path('pay/', views.pay, name='pay'),
    path('checkout/', views.checkout, name='checkout')
]
