from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    # polls/list/
    path('login/', views.accounts_login_view, name='login'),
    path('logout/', views.accounts_logout_view, name='logout'),
    path('register/', views.accounts_register_view, name='register'),
]
