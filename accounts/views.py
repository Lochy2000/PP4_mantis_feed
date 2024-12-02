from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm


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

