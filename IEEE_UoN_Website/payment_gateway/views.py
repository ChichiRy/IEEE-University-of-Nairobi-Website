from django.shortcuts import render

# Create your views here.


def pay(request):
    return render(request, 'pay.html')


def checkout(request):
    return render(request, 'checkout.html')
