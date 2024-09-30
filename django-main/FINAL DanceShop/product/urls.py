from django.urls import path
from .views import AllProductView, TopView, SortAll, ListUsr, Params, Product, TopView, ListUsr
app_name = "product"

# ссылки для персональных данных и объявлений под страницу

urlpatterns = [
    path('sort_by/', SortAll.as_view()),
    path('allproducts/', AllProductView.as_view()),
    path('getalladsofusr/', ListUsr.as_view()),
    path('params/', Params.as_view()),
    path('products/', Product.as_view()),
    path('top/', TopView.as_view()),
    path('usrlist/', ListUsr.as_view()),
]
