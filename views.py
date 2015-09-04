from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from scrape.models import SteamIDForm 
from submit.models import Game

import json, urllib2
# Create your views here.

def main_page(request):
    form = SteamIDForm
    our_games = []
    if request.method == 'POST':
        form = SteamIDForm(request.POST)
        if form.is_valid():
            my_games = form.get_list()
            for x in Game.objects.all():
                if x.name.lower() in my_games:
                    our_games.append(x.name)
                    x.owned_pc = True
                    x.save()
            if type(my_games) == urllib2.HTTPError:
                our_games = [my_games]
    context = {
       'form' : form, 
       'matches' : our_games,
       'was_post' : request.method == 'POST',
    }
    return render(request, 'scrape/main.html', context)
