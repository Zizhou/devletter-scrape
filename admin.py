from django.contrib import admin

from scrape.models import SteamID
# Register your models here.

class SteamIDAdmin(admin.ModelAdmin):
    fields = ['steamid']

admin.site.register(SteamID, SteamIDAdmin)
