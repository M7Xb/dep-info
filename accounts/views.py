from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth import get_user_model
from django.utils import timezone

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, '✨ Account created successfully! Please login with your credentials.')
                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful!')  # Make sure this exact text matches
                return redirect('home')
            else:
                messages.error(request, 'Your account is not active.')
        else:
            messages.error(request, 'Invalid email or password.')
            
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    # First clear all existing messages
    storage = messages.get_messages(request)
    storage.used = True
    
    # Clear any login success flags
    if 'show_login_success' in request.session:
        del request.session['show_login_success']
    
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Handle profile image
            if 'profile_image' in request.FILES:
                image_file = request.FILES['profile_image']
                try:
                    user.profile_image_data = image_file.read()
                    user.profile_image_type = image_file.content_type
                except Exception as e:
                    messages.error(request, f'Error uploading image: {str(e)}')
            
            user.save()
            messages.success(request, '✨ Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})
