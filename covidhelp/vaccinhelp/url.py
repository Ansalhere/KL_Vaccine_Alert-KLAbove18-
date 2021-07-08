from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ml', views.index_ml, name='index_ml'),
    path('get_covidinfo_bycountry', views.get_covidinfo_bycountry, name='get_covidinfo_bycountry'),
    path('get_states_new',views.get_states_new, name="get_states"),
    path('get_states_ml',views.get_states_ml, name="get_states_ml"),
    path('get_districts', views.get_districts, name='get_districts'),
    path('get_sessions_by_districts', views.get_sessions_by_districts, name='get_sessions_by_districts'),
]