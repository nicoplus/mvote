from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib import messages

from mysite import models

from datetime import date

# Create your views here.

def index(request):
    all_polls = models.Poll.objects.filter(enabled=True)
    paginator = Paginator(all_polls, 5)
    p = request.GET.get('p')
    try:
        polls = paginator.page(p)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)

    return render(request, 'index.html', locals())

@login_required(login_url='/accounts/login/')
def poll(request, pollid):
    try:
        poll = models.Poll.objects.get(id = pollid)
    except:
        poll = None
    if poll:
        pollitems = models.PollItem.objects.filter(poll = poll).order_by('-vote')

    return render(request, 'poll.html', locals())

@login_required(login_url='/accounts/login/')
def vote(request, pollid, pollitemid):
    if models.VoteCheck.objects.filter(userid = request.user.id, pollid = pollid, vote_date = date.today()):
        messages.add_message(request, messages.WARNING, 'Vote once in a day.')
        return redirect(poll, pollid)
    else:
        vote_rec = models.VoteCheck(userid = request.user.id, pollid = pollid, vote_date = date.today())
        vote_rec.save()
    try:
        pollitem = models.PollItem.objects.get(id=pollitemid)
    except:
        pollitem = None
    if pollitem:
        pollitem.vote += 1
        pollitem.save()

    return redirect(poll, pollid)

@login_required
def govote(request):
    if request.method == 'GET' and request.is_ajax():
        pollitemid = request.GET.get('pollitemid')
        pollid = request.GET.get('pollid')
        bypass = False
        if models.VoteCheck.objects.filter(userid = request.user.id, pollid = pollid, vote_date=date.today()):
            bypass = True
        else:
            vote_rec = models.VoteCheck(userid = request.user.id, pollid = pollid, vote_date = date.today())
            vote_rec.save()
        try:
            pollitem = models.PollItem.objects.get(id=pollitemid)
            if not bypass:
                pollitem.vote += 1
                pollitem.save()
            votes = pollitem.vote
        except:
            votes = 0
    else:
        votes = 0

    return JsonResponse([votes, bypass], safe=False)

