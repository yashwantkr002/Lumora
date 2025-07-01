from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.utils.timezone import now
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage
import re
from django.db.models import Q
from itertools import chain
from django.db import transaction
import pyotp
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Invalid email format.")
            return redirect('register')

        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(regex, password):
            messages.error(
                request,
                "Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create user
        user = CustomUser.objects.create_user(username=username, email=email)
        user.set_password(password)

        # Generate OTP and send email
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, digits=6, interval=600)
        otp = totp.now()
        subject = 'OTP Verification'
        email_template_name = 'otpemailsend.html'
        context = {
            'otp': otp,
            'email': email,
            'site_name': 'MySite',
            'user': user,
        
        }
        message = render_to_string(email_template_name, context)
        try:
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            email_message.content_subtype = 'html'
            email_message.send(fail_silently=False )
            user.otp_secret = secret
            user.save()
            request.session['email'] = email
            messages.success(request, "Registration successful. Please check your email for verification.")
            return redirect('otp')
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")
            return redirect('register')

    return render(request, "register.html")

def getotp(request):
    email = request.session.get('email')
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        messages.error(request, "User not found. Please register again.")
        return redirect('register')
    if request.method == 'POST':
        totp = pyotp.TOTP(user.otp_secret, digits=6, interval=600)
        otp = request.POST.get('otp')
        if totp.verify(otp):
            messages.success(request, "OTP verified successfully!")
            login(request, user)
            request.session.pop('email', None)  # Clear session
            return redirect('/')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('otp')

    return render(request, 'otp.html', {'email': email})

def resend_otp(request):
    email = request.session.get('email')
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('otp')
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, digits=6, interval=600)
    otp = totp.now()
    # Send the OTP to the user's email
    subject = 'OTP Verification'
    email_template_name = 'otpemailsend.html'
    context = {
            'otp': otp,
            'email': email,
            'site_name': 'MySite',
            'user': user,
        }
    message = render_to_string(email_template_name, context)
    try:
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)
        # Save the OTP secret for the user
        user.otp_secret = secret
        user.save()
        messages.success(request, "OTP has been resent successfully. Please check your email.")
        return redirect('otp')  # Redirect to the OTP verification page

    except Exception as e:
        messages.error(request, f"Error occurred while resending OTP: {str(e)}")
        return redirect('otp')  # Redirect to the OTP verification page


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request,'login.html')

def resetpass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            # Check if the reset was requested within the last 5 minutes
            if user.password_reset_requested_at and now() - user.password_reset_requested_at < timedelta(minutes=10):
                messages.error(request, "A reset link was recently sent. Please wait before requesting a new one.")
                return redirect("reset")
            
            # Update the timestamp for the reset request
            user.password_reset_requested_at = now()
            user.save()

            # Generate email content
            subject = "Password Reset Requested"
            email_template_name = "password_reset_email.html"
            context = {
                "email": user.email,
                "domain": request.get_host(),
                "site_name": "MySite",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "https" if request.is_secure() else "http",
            }
            email_content = render_to_string(email_template_name, context)
            
            try:
                email_message=EmailMessage(
                    subject=subject,
                    body=email_content,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email],
                )
                email_message.content_subtype = "html"
                email_message.send(fail_silently=False)

                request.session['email'] = email
                messages.success(request, "Password reset email has been sent.")
                return redirect("passwordemail")
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
        else:
            messages.error(request, "Email not found.")
    return render(request, 'resetpass.html')

def passwordResetEmail(request):
    email = request.session.get('email')
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        messages.error(request, "User not found. Please register again.")
        return redirect('register')
    request.session.pop('email', None)
    return render(request,'passwordResetEmail.html',{'email':email})

def password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    # Check if the user and token are valid
    if user is not None and default_token_generator.check_token(user, token):
        # Check if the link has expired (5 minutes)
        if user.password_reset_requested_at and now() - user.password_reset_requested_at > timedelta(minutes=10):
            messages.error(request, "The reset link has expired. Please request a new one.")
            return redirect('reset')

        if request.method == 'POST':
            # Get new passwords from the form
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            # Validate password strength
            regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            if not re.match(regex, new_password1):
                messages.error(
                    request,
                    "Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
                )
                return redirect('password_reset_confirm', uidb64=uidb64, token=token)

            # Check if passwords match
            if new_password1 != new_password2:
                messages.error(request, "Passwords do not match.")
                return redirect('password_reset_confirm', uidb64=uidb64, token=token)

            # Save the new password
            user.set_password(new_password1)
            user.save()

            messages.success(request, "Your password has been reset successfully. You can now log in.")
            return redirect('login')

        # Render the password reset page
        return render(request, 'resetpage.html', {'user': user})

    else:
        messages.error(request, "The reset link is invalid.")
        return redirect('reset')

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def follow_unfollow_user(request, username):
    if request.method == "POST":
        with transaction.atomic():
            user_to_follow = get_object_or_404(CustomUser, username=username)

            if request.user == user_to_follow:
               return JsonResponse({"error": "You cannot follow yourself."}, status=400)

            # Check if the user is already following
            follow_instance, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
            )

            if not created:
                # Unfollow the user
                follow_instance.delete()
                is_following = False
            else:
                # Follow the user
                is_following = True

            # Return the updated follower count and status
            follower_count = Follow.objects.filter(followed=user_to_follow).count()
            return JsonResponse({
                "is_following": is_following,
                "follower_count": follower_count
            })

    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required(login_url='/login/')
def profile(request,username):
    user_profile = get_object_or_404(CustomUser, username=username)
    posts= Post.objects.filter(author=user_profile).order_by('-created_at')
    follower = Follow.objects.filter(followed=user_profile)
    following = Follow.objects.filter(follower=user_profile)
    numberpost=posts.count()
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user_profile).exists()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = request.GET.get('page')
        paginator = Paginator(posts, 20)  # 20 posts per page
        try:
            page = paginator.page(page_number)
        except Exception:
            return JsonResponse({'posts': []})  # No more posts

        posts_data = [
            {
                'id': post.id,
                'image_url': post.image.url if post.image else None,
                'video_url': post.video.url if post.video else None,
                'likes_count':post.like_count(),
            }
            for post in page.object_list
        ]
        return JsonResponse({'posts': posts_data})
    paginator = Paginator(posts, 20)
    first_page_posts = paginator.page(1)   
    return render(request,'profile.html',{'user_profile':user_profile,'posts':first_page_posts,'follower':follower,'following':following,'user':request.user,'is_following':is_following,'numberpost':numberpost})

@login_required(login_url='/login/')
def post_detail(request, post_id):
    # Fetch the post by ID or return 404 if not found
    post = get_object_or_404(Post, id=post_id)

    # Fetch related comments ordered by creation date
    comments = post.comment_set.all().order_by('-created_at')

    # Pagination for comments
    paginator = Paginator(comments, 10)  # Show 10 comments per page
    page_number = request.GET.get('page', 1)
    comments_page = paginator.get_page(page_number)

    # Check for AJAX request for loading more comments
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comments_data = [
            {
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for comment in comments_page
        ]
        return JsonResponse({'comments': comments_data, 'has_next': comments_page.has_next()})
    
    # created=Like.objects.filter(user=request.user, post=post_id)
    # Render the post detail page
    return render(request, 'post_detail.html', {
        'post': post,
        'comments_page': comments_page,
        'like':post.like_count(),
        'is_liked':post.is_liked_by(user=request.user) 
    })

@login_required(login_url='/login/')
def editprofile(request):
    user =CustomUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')
        user.first_name = first_name
        user.last_name = last_name
        user.bio = bio
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        return redirect('profile', username=user.username)

    return render(request,'editprofile.html',{user:user})

@login_required(login_url='/login/')
def create_post(request):
    
    if request.method == 'POST':
        caption = request.POST.get('caption')
        media_file = request.FILES.get('media_file')

        if media_file:
            # Determine the media type based on file extension
            media_type = 'video' if media_file.content_type.startswith('video') else 'image'

            # Save the post
            post = Post.objects.create(
                author=request.user,
                media_type=media_type,
                image=media_file if media_type == 'image' else None,
                video=media_file if media_type == 'video' else None,
                caption=caption,
            )
            post.save()
            return redirect('index')  # Redirect after successful post creation

    return render(request, 'create_post.html')

@login_required(login_url='/login/')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    with transaction.atomic():
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
        # Unlike the post
            like.delete()
            liked = False
        else:
            liked = True
    return JsonResponse({
        "liked": liked,
        "likes_count":post.like_count()
    })


@login_required(login_url='/login/')
def search_users(request):
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)  # Get the current page number
    users = CustomUser.objects.filter(
        Q(username__icontains=query) | Q(bio__icontains=query)
    ).exclude(id=request.user.id) if query else CustomUser.objects.all().exclude(id=request.user.id)

    followed = Follow.objects.filter(follower=request.user)
    followed_users = [user.followed.username for user in followed]

    paginator = Paginator(users, 20)  # 20 users per page

    try:
        users_page = paginator.page(page_number)
        users_data = [
            {
                "username": user.username,
                "profile_picture": user.profile_picture.url if user.profile_picture else "/static/default-profile.png",
                "bio": user.bio or "No bio available",
            }
            for user in users_page
        ]
        has_next = users_page.has_next()
    except EmptyPage:
        users_data = []  # No more users
        has_next = False

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "users": users_data,
            "followed_users": followed_users,
            "has_next": has_next,  # To indicate if there are more pages
        })

    return render(request, 'search.html', {
        'users': users_page,
        'followed_users': followed_users,
    })


@login_required(login_url='/login/')
def reels_view(request):
    reels = Post.objects.filter(media_type='video').order_by('-created_at')
    page_number = request.GET.get('page',1)
    paginator = Paginator(reels, 2)  # 5 reels per page
    page_obj = paginator.page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
        with transaction.atomic():
            reels_data = [
                {
                'id': reel.id,
                "author": reel.author.username,
                "author_image": reel.author.profile_picture.url if reel.author.profile_picture else "/static/default-profile.png",  
                'image_url': reel.image.url if reel.image else None,
                'video_url': reel.video.url if reel.video else None,
                'likes_count': reel.like_count(),
                'is_liked': reel.is_liked_by(user=request.user),
                "caption": reel.caption,
                "created_at": reel.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "view_count": reel.view_count,

            }
            for reel in page_obj
        ]
        return JsonResponse({
            "reels":reels_data,
            "has_next": page_obj.has_next()
            })
    reels=[i for i in page_obj]
    for reel in reels:
        reel.is_liked = reel.is_liked_by(user=request.user)
        reel.like_count = reel.like_count()

    return render(request, 'reels.html', {'reels': reels})


@login_required(login_url='/login/')
def index(request):
    page_number = request.GET.get('page', 1)
    print(page_number)
    requestuser = request.user
    user = CustomUser.objects.filter(username=requestuser).first()

    user_following_list = []
    feed = []
    if requestuser.is_authenticated:
        user_following = Follow.objects.filter(follower=requestuser)
        for following in user_following:
            user_following_list.append(following.followed.username)

        for usernames in user_following_list:
            feed_lists = Post.objects.filter(author__username=usernames).order_by('-created_at')
            feed.append(feed_lists)

        feed_list = list(chain(*feed))
    else:
        feed_list = Post.objects.all().order_by('-created_at')

    # Add extra attributes to each post
    for post in feed_list:
        post.is_liked = post.is_liked_by(user=request.user)
        post.like_count = post.like_count()

    # Paginate the feed list
    paginator = Paginator(feed_list, 10)
    page_obj = paginator.get_page(page_number)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        posts_data = [
            {
                "id": post.id,
                "author": post.author.username,
                "author_image": post.author.profile_picture.url if post.author.profile_picture else "/static/default-profile.png",
                "caption": post.caption,
                "image_url": post.image.url if post.image else "",
                "video_url": post.video.url if post.video else "",
                "is_liked": post.is_liked,
                "like_count": post.like_count,
                'created_at': post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for post in page_obj
        ]
        return JsonResponse({
            "posts": posts_data,
            "has_next": page_obj.has_next(),
        })

    return render(request, "index.html", {"user": user, "posts": page_obj})



