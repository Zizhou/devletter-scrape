from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from scrape.models import SteamIDForm, GameOwnedForm 
from submit.models import Game
from django.contrib.auth.decorators import login_required, permission_required

import json, urllib2
# Create your views here.
def main_page(request):
    form = SteamIDForm
    our_games = []
    if request.method == 'POST':
        form = SteamIDForm(request.POST)
        if form.is_valid():
            saved_id = form.save()
            my_games = saved_id.get_list()
            for x in Game.objects.all():
                if x.name.lower() in my_games:
                    our_games.append(x.name)
                    x.owned_pc = True
                    x.save()
            if type(my_games) == urllib2.HTTPError:
                our_games = [my_games]
            if type(my_games) != type([]):
                our_games = [my_games]
    context = {
       'form' : form, 
       'matches' : our_games,
       'was_post' : request.method == 'POST',
    }
    return render(request, 'scrape/main.html', context)

@login_required
def bulk(request):
    error = []
    if request.method == 'POST':
        #processing
        for x in Game.objects.all():
            form = GameOwnedForm(request.POST,instance = x, prefix = x.name)
            if form.is_valid():
                try:
                    form.save()
                except:
                    try:
                        error.append(x.name.decode('utf-8'))
                    except:
                        error.append(unicode(x.id)+'this one\'s funny...')

    form = []
    for x in Game.objects.all():
        form.append({'name':x.name, 'form':GameOwnedForm(instance=x, prefix=x.name)})

    context = {
        'form':form,
        'error': error,
        'message': len(error)>0
    }
    return render(request, 'scrape/bulk.html', context)
