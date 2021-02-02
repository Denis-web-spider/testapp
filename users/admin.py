from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import SignUpForm

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = CustomUser
    list_display = ['username', 'email', 'phone_number']

admin.site.register(CustomUser, CustomUserAdmin)
