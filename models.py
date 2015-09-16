from django.db import models
from django import forms
import json, urllib2

from scrape.local_secret import API_KEY

from submit.models import Game

# Create your models here.

class SteamIDForm(forms.Form):
    steamid = forms.IntegerField(label = 'SteamID64', widget = forms.NumberInput(attrs={'placeholder':'76561197960434622'}))

    def get_list(self):
        try:
            steamid = self.cleaned_data['steamid']
            request = urllib2.Request('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+unicode(API_KEY)+'&steamid='+unicode(steamid)+'&include_appinfo=1&format=json')
            response = urllib2.urlopen(request)
            parsed = json.loads(response.read())
        except urllib2.HTTPError as e:
            print unicode(e)
            print type(e)
            return e
        my_games = []
        try:
            for x in parsed['response']['games']:
                my_games.append(x['name'].lower().strip())
        except:
            return parsed
        return my_games

#bulk edit form
class GameOwnedForm(forms.ModelForm):
    
    class Meta:
        model = Game
        fields = ['name','owned_pc','owned_360','owned_xb1','owned_ps3','owned_ps4','owned_other']


