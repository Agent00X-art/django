from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import PersonalData
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = PersonalData
        fields = ('Phone',)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = PersonalData
        fields = ('Phone',)
