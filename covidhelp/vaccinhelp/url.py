from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_covidinfo_bycountry', views.get_covidinfo_bycountry, name='get_covidinfo_bycountry'),
    path('get_states',views.get_states, name="get_states"),
    path('get_districts', views.get_districts, name='get_districts'),
    path('get_sessions_by_districts', views.get_sessions_by_districts, name='get_sessions_by_districts'),
]