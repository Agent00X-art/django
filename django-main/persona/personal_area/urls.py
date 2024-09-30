from django.urls import path
from .views import PersonalDataView, PhoneCode_ValidationSendView, PhoneCode_ValidateView, LoginView, LogoutView, EmailSendCode, EmailCodeValidate, DialogCreateView, MessageViews, GetChatsViews, GetOnePersonalView, CreateLoyaltyCardView, CreateGiftCardView
app_name = "users"

# ссылки для персональных данных и объявлений под страницу

urlpatterns = [
    path('personality/', PersonalDataView.as_view()),
    path('personality/<int:pk>', PersonalDataView.as_view()), # ссылка для delete, post и put запросов
    path('codesend/<int:pk>', PhoneCode_ValidationSendView.as_view()), # ссылка для delete, post и put запросов
    path('codevalidate/<int:pk>', PhoneCode_ValidateView.as_view()), # ссылка для delete, post и put запросов
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('emailcodesend/', EmailSendCode.as_view()),
    path('emailcodevalidate/', EmailCodeValidate.as_view()),
    path('chatcreate/', DialogCreateView.as_view()),
    path('chat/<str:pk>', MessageViews.as_view()),
    path('allchat/', GetChatsViews.as_view()),
    path('getpersonal/', GetOnePersonalView.as_view()),
    path('loyaltycard/', CreateLoyaltyCardView.as_view()),
    path('giftcard/', CreateGiftCardView.as_view()),
]
