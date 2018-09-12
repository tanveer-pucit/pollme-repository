from django.shortcuts import get_object_or_404, render, redirect
from .models import Poll, Choice, Vote
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import PollForm, EditPollForm, ChoiceForm
import datetime


@login_required
def polls_list_view(request):
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls/polls_list.html', context)


@login_required
def polls_detail_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    print(poll.id)
    user_can_vote = poll.user_can_vote(request.user)
    results = poll.get_res_dect()
    context = {'poll': poll, 'user_can_vote': user_can_vote, 'results': results}
    return render(request, 'polls/poll_detail.html', context)


def polls_vote_save_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.user_can_vote(request.user):
        messages.error(request, 'Are you crazy? you have already voted for this poll!')
        return redirect('polls:polls_detail_view', poll_id=poll_id)

    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=request.user, poll=poll, choice=choice)
        new_vote.save()
    else:
        messages.error(request, 'No choice was selected!')
        return redirect('polls:polls_detail_view', poll_id=poll_id)
    # return render(request, 'polls/poll_results.html', {'poll': poll})
    return redirect('polls:polls_detail_view', poll_id=poll_id)


@login_required
def polls_add_view(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.owner = request.user
            new_poll.save()

            new_choice1 = Choice(
                poll=new_poll,
                choice_text=form.cleaned_data['choice1']
            ).save()
            new_choice2 = Choice(
                poll=new_poll,
                choice_text=form.cleaned_data['choice2']
            ).save()
            messages.success(request, 'Poll and Choices added!', extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:polls_list_view')
    else:
        form = PollForm()
    context = {'form': form}
    return render(request, 'polls/add_poll.html', context)


@login_required
def polls_edit_view(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)

    if request.user != poll.owner:
        return redirect('/')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poll edited successfully!', extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:polls_list_view')
    else:
        form = EditPollForm(instance=poll)

    context = {'form': form, 'poll': poll}
    return render(request, 'polls/edit_poll.html', context)


@login_required
def choice_add_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user != poll.owner:
        return redirect('/')

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request, 'Choice Added successfully!',
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:polls_list_view')
    else:
        form = ChoiceForm()

    return render(request, 'polls/add_choice.html', {'form': form})


@login_required
def choice_edit_view(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)

    if request.user != poll.owner:
        return redirect('/')

    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Choice Edited successfully!',
                             extra_tags='alert alert-success alert-dismissible fade show')

            return redirect('polls:polls_list_view')
    else:
        form = ChoiceForm(instance=choice)

    return render(request, 'polls/add_choice.html', {'form': form, 'edit_mode': True, 'choice': choice})


@login_required
def choice_confirm_delete_view(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)

    if request.user != poll.owner:
        return redirect('/')

    if request.method == 'POST':
        choice.delete()
        messages.success(request, 'Choice has been DELETED successfully!',
                         extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('polls:polls_list_view')

    return render(request, 'polls/delete_choice_confirm.html', {'choice': choice})


@login_required
def poll_confirm_delete_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user != poll.owner:
        return redirect('/')

    if request.method == 'POST':
        poll.delete()
        messages.success(request, 'Poll has been DELETED successfully!',
                         extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('polls:polls_list_view')

    return render(request, 'polls/delete_poll_confirm.html', {'poll': poll})







