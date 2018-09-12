from django.urls import path
from . import views


app_name = "polls"
urlpatterns = [
    # polls/list/
    path('list/', views.polls_list_view, name='polls_list_view'),

    path('add/', views.polls_add_view, name='add'),


    path('edit/<int:poll_id>/', views.polls_edit_view, name='edit_poll'),

    path('edit/<int:poll_id>/choice/add', views.choice_add_view, name='add_choice'),

    path('edit/choice/<int:choice_id>/', views.choice_edit_view, name='edit_choice'),

    path('delete/choice/<int:choice_id>/', views.choice_confirm_delete_view, name='choice_confirm_delete'),

    path('delete/poll/<int:poll_id>/', views.poll_confirm_delete_view, name='poll_confirm_delete'),

    # polls/details/1
    path('details/<int:poll_id>/', views.polls_detail_view, name='polls_detail_view'),

    # polls/details/1/vote
    path('details/<int:poll_id>/polls_vote_save_view/', views.polls_vote_save_view, name='polls_vote_save_view'),
]
