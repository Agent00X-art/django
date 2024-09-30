from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import PersonalData, Message, CreateGiftCard, CreateLoyaltyCard
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = PersonalData
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('Surname', 'Name', 'Patronymic', 'Phone', 'PhoneValidate', 'PhoneCode', 'email', 'EmailValidate', 'EmailCode', 'Location', 'Avatar', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Surname', 'Name', 'Patronymic', 'Phone', 'PhoneValidate', 'PhoneCode', 'email', 'EmailValidate', 'EmailCode', 'Location', 'Avatar', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(PersonalData, CustomUserAdmin)
admin.site.register(Message)
admin.site.register(CreateLoyaltyCard)
admin.site.register(CreateGiftCard)