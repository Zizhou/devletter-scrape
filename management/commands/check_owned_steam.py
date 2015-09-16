##schedule this script with a cron or something
from django.core.management.base import BaseCommand, CommandError

from scrape.models import SteamID
from submit.models import Game

class Command(BaseCommand):

    help = 'updates ownership for all steam ids'
    def handle(self, *args, **options):
        for steamid in SteamID.objects.all():
            try:
                my_games = steamid.get_list()
                for x in Game.objects.all():
                    if x.name.lower() in my_games:
                        x.owned_pc = True
                        x.save()
                print 'handled ' + unicode(steamid)
            except:
                print 'error with ' + unicode(steamid)
