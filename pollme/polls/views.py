from django.shortcuts import render
from .models import Poll


def polls_list_view(request):
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls/polls_list.html', context)
