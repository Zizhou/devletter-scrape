from django.db import models
from django import forms
import json, urllib2

from scrape.local_secret import API_KEY

# Create your models here.

class SteamIDForm(forms.Form):
    steamid = forms.IntegerField(label = 'Steam ID', widget = forms.NumberInput(attrs={'placeholder':'76561197960434622'}))

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
        for x in parsed['response']['games']:
            my_games.append(x['name'].lower().strip())

        return my_games
