from django.shortcuts import render, redirect

from .forms import SignUpForm
from .models import CustomUser

def signup_view(request):
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'], password=form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', context={'form': form})
