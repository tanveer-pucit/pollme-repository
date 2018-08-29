from django.urls import path
from . import views


app_name="polls"
urlpatterns = [
    path('list/', views.polls_list_view, name='polls_list_view'),
]
