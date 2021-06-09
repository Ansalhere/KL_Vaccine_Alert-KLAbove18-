import datetime
import json
import simplejson as simplejson
from dateutil.tz import tz
from django.shortcuts import render
from django.http import HttpResponse
import requests

from .models import Contact

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
now = datetime.datetime.now()
today_date = now.strftime("%d-%m-%Y")
district_id = 683556
api_telegram_url = "https://api.telegram.org/bot1829919952:AAE2GSjSQ3_LAORy-E57Uj1bvZnsYeaxvhE/sendMessage?chat_id=@__groupid__&text="
group_id = "ernakulam_vaccin_alerts"
def fetch_data_from_cowin(district_id):
    query_params = "?pincode={}&date={}".format("683556",today_date)
    headers = {
        'Host': 'cdn-api.co-vin.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    final_url = base_cowin_url+query_params

    print(final_url)
    response = requests.request("GET",final_url,headers=headers)

    extract_availability_data(response)


def send_message_telegram(message):
    final_telegram_url = api_telegram_url.replace("__groupid__",group_id)
    final_telegram_url = final_telegram_url+message
    print(final_telegram_url)
    response = requests.get(final_telegram_url)
    print(response.text)


def extract_availability_data(response):
    response_json = response.json()
    for center in response_json["centers"]:
        for session in center["sessions"]:
             #if session["available_capacity_dose1"] > 0 or session["available_capacity_dose1"] > 0 and session["min_age_limit"]==45:
                message = "Pincode: {}, Name: {}, Slots: {},Minimum Age: {}".format(
                center["center_id"], center["name"],
                session["available_capacity_dose1"],
                session["min_age_limit"]
                )
                send_message_telegram(message)
# Create your views here.
def index(request):
    context = get_summary()
    return render(request, "cases_info.html", context)

def get_covidinfo_bycountry(request):
    country_name = request.GET.get('country_name')
    print(country_name)
    info_by_country = []
    payload = get_country(country_name)
    return HttpResponse(simplejson.dumps(payload[-2:]), content_type='application/json' )

def get_summary():
    countries_url = "https://api.covid19api.com/summary"
    r = requests.get(countries_url)
    droplets = r.json()
    droplet_list = []
    # for i in range(len(droplets['Country'])):
    #     droplet_list.append(droplets['Country'][i])

    payload = {
        "countries": droplets
    }
    return payload

def get_country(country):

    url = "https://api.covid19api.com/total/country/"+country
    response = requests.request("GET", url)
    return response.json()

def get_states(request):
    api_url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    headers = {
        'Host': 'cdn-api.co-vin.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.request("GET", api_url, headers=headers)
    payload = response.json()
    return render(request,'vaccin_alerts.html',payload )

def get_districts(request):

    state_id = request.GET.get('state_id')
    api_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+state_id
    headers = {
        'Host': 'cdn-api.co-vin.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.request("GET", api_url, headers=headers)
    payload = response.json()
    print(payload)
    return HttpResponse(simplejson.dumps(payload),content_type='application/json')

def get_sessions_by_districts(request):
    district_id = request.GET.get('district_id')
    dateSelected = request.GET.get('date')
    pincode = request.GET.get('pincode')
    print(pincode)
    base = datetime.datetime.today()
    dates = []
    payload = []
    session={'session':[]}
    if(pincode!=None):
        print("inside pincode")
        query_params = "?pincode={}&date={}".format(pincode, today_date)
        api_url = base_cowin_url+query_params;
        headers = {
            'Host': 'cdn-api.co-vin.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }

        response = requests.request("GET", api_url, headers=headers)
        session['session'].append(response.json())
        print(session)

    elif (dateSelected!= ''):
            print('Hi')
            api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=" + district_id + "&date=" + dateSelected
            headers = {
                'Host': 'cdn-api.co-vin.in',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            }

            response = requests.request("GET", api_url, headers=headers)
            session['session'].append(response.json())
    else:
        print("Inside date")
        for x in range(0, 7):
            x = base + datetime.timedelta(days=x)
            y = x.strftime("%d-%m-%Y")
            dates.append(y)

        for date in dates:
            api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=" + district_id + "&date=" + date
            headers = {
                'Host': 'cdn-api.co-vin.in',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            }

            response = requests.request("GET", api_url, headers=headers)
            session['session'].append(response.json())
            print(session)

    return HttpResponse(simplejson.dumps(session), content_type='application/json')

def get_feedback(request):
    if request.method == 'POST':
        email = request.GET.get('email')
        message = request.GET.get('message')
        c = Contact(email=email,message=message)
        response = {"message":"Request/Feedbck sent successfully"}

        return HttpResponse(simplejson.dumps(response), content_type='application/json')
