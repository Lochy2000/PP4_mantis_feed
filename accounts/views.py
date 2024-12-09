from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm


# Create your views here.

#---------- Login request ------------

#-------- Registration -----------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect ('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html',{'form': form})

#-------- User Profile -----------
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required 
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request,'accounts/edit_profile.html', {'form':form})