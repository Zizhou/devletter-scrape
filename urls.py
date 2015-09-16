from django.conf.urls import patterns, url

from scrape import views

urlpatterns = patterns('',
    url(r'^$', views.main_page, name = 'main'),
    url(r'^bulk$', views.bulk, name = 'bulk'),

)
