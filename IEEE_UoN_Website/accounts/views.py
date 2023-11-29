import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from IEEE_UoN_Website import settings
from accounts.models import Profile


# Create your views here.


def log_in(request):
    return render(request, 'signup_login.html')


def token_send(request):
    return render(request, 'token_send.html')


def success(request):
    return render(request, 'success.html')


def register_attempt(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST.get('email')
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        try:
            # Validate username
            if User.objects.filter(username=username).exists():
                messages.success(request, 'Username already exists! Please try a different username.')
                return redirect('accounts:register_attempt')

            # Validate email
            if User.objects.filter(email=email).exists():
                messages.success(request, 'Email already exists! Please try another one.')
                return redirect('accounts:register_attempt')

            # Validate password match
            if pass1 != pass2:
                messages.error(request, "Passwords do not match!")
                return redirect('accounts:register_attempt')

            # Create user object
            user_obj = User.objects.create_user(username, email)
            user_obj.set_password(pass1)
            user_obj.first_name = fname
            user_obj.last_name = lname
            user_obj.is_active = False  # Disable account until email confirmation
            user_obj.save()

            profile_obj = Profile.objects.create(user=user_obj, token=str(uuid.uuid4))
            profile_obj.save()

            return redirect('accounts:token_send')

        except Exception as e:
            print(e)

    return render(request, 'login.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('accounts:login')
        else:
            return redirect('accounts:error')

    except Exception as e:
        print(e)


def error_page(request):
    return render(request, 'error.html')


def send_mail_after_registration(request, user_obj, email, token):  # Send verification email
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    current_site = get_current_site(request)
    subject = 'Confirm your account'
    message = render_to_string('email_confirmation.html', {
        'name': user_obj.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
        'token': generate_token.make_token(user_obj)
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user_obj.email], )
    send_mail(subject, message, email_from, recipient_list, fail_silently=True)
    messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address and activate your account.")
    return redirect('signin')


def send_welcome_email(email, user_obj):  # Send welcome email after successful verification
    subject = "Welcome to the IEEE University of Nairobi Student Branch Website"
    message = f"Hello {user_obj.first_name}!\n\nThank you for registering on our website. Feel free to explore the wonderful world of IEEE!\n\nRegards, \nThe IEEE Team"
    from_email = settings.EMAIL_HOST_USER
    to_list = [user_obj.email]
    send_mail(subject, message, from_email, to_list, fail_silently=False)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_obj = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user_obj = None

    if user_obj is not None and generate_token.check_token(user_obj, token):
        user_obj.is_active = True
        user_obj.save()
        login(request, user_obj)
        messages.success(request, "Your account has been activated!")
        return redirect('accounts:login')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            username = user.username
            return render(request, "index.html", {'username': username})

        else:
            messages.error(request, "Bad Credentials!")
            return redirect("home")
    return render(request, "login.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")
