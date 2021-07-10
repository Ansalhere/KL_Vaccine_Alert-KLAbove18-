import datetime
import json
import simplejson as simplejson
from django.shortcuts import render
from django.http import HttpResponse
import requests

# from .models import Contact


now = datetime.datetime.now()
today_date = now.strftime("%d-%m-%Y")
district_id = 683556
api_telegram_url = "https://api.telegram.org/bot1829919952:AAE2GSjSQ3_LAORy-E57Uj1bvZnsYeaxvhE/sendMessage?chat_id=@__groupid__&text="
group_id = "ernakulam_vaccin_alert"

telegram_mapping = {
    '307':'ernakulam_vaccin_alert',
    '301':'alappuzha_vaccin_alert',
    '306':'idukki_vaccin_alert',
    '297':'Kannur_vaccin_alert',
    '295':'Kasaragod_vaccin_alert',
    '298':'Kollam_vaccin_alert',
    '304':'Kottayam_vaccin_alert',
    '305':'Kozhikode_vaccin_alert',
    '302':'malappuramvaccine_alert',
    '308':'palakkadvaccine_alert',
    '300':'Pathanamthittavaccine_alert',
    '296':'Thiruvananthapuramvaccine_alert',
    '303':'Thrissurvaccine_alert',
    '299':'Wayanadvaccine_alert',
}

def dist_fetch_data_from_cowin(district_id):
    district_base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    query_params = "?district_id={}&date={}".format(district_id,today_date)
    headers = {
        'Host': 'cdn-api.co-vin.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    final_url = district_base_cowin_url+query_params
    print(final_url)
    response = requests.request("GET",final_url,headers=headers)
    print(response)
    extract_availability_data(response,district_id)
def fetch_data_from_cowin(pincode):
    pin_base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    query_params = "?pincode={}&date={}".format(pincode,today_date)
    headers = {
        'Host': 'cdn-api.co-vin.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    final_url = pin_base_cowin_url+query_params
    response = requests.request("GET",final_url,headers=headers)
    extract_availability_data(response,pincode)
def send_message_telegram(message,id):

    final_telegram_url = api_telegram_url.replace("__groupid__",telegram_mapping[str(id)])
    final_telegram_url = final_telegram_url+message
    print(final_telegram_url)
    response = requests.get(final_telegram_url)
    print(response.text)
def extract_availability_data(response,id):
    response_json = response.json()
    print(response_json)
    for center in response_json["centers"]:
        for session in center["sessions"]:
              try:
                  if session["max_age_limit"]:
                       max_age = session["max_age_limit"]
              except KeyError:
                       max_age = ""
              if session["available_capacity_dose1"] > 0 or session["available_capacity_dose2"] > 0 :
                message = "പ്രായം: {} - {} \n" \
                          "സ്ഥലം: {}, \n" \
                          "ഒന്നാമത്തെ വാക്‌സിൻ സ്ലോട്ട്: {},\n"\
                          "രണ്ടാമത്തെ വാക്‌സിൻ സ്ലോട്ട്: {},\n" \
                          "വാക്‌സിൻ : {},\n"\
                          "പിൻകോഡ്: {}, \n"\
                              .format(
                session["min_age_limit"],
                max_age,
                center["name"],
                session["available_capacity_dose1"],
                session["available_capacity_dose2"],
                session["vaccine"],
                center["center_id"],
                )
                send_message_telegram(message,id)
# Create your views here.
def index(request):
    context = get_summary()
    return render(request, "cases_info.html", context)

def index_ml(request):
    context = get_summary()
    return render(request, "cases_info_ml.html", context)

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

def get_states_new(request):
    api_url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.get(api_url, headers=headers)
    try:
        payload = response.json()
    except:
        print(" NO Payload")
        payload = {"response.json()":""}
    return render(request,'vaccin_alerts.html',payload )

def get_states(request):
    api_url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.request("GET", api_url, headers=headers)
    try:
        payload = response.json()
    except:
        print(" NO Payload")
    return render(request,'vaccin_alerts.html',payload )

def get_states_ml(request):
    api_url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    headers = {
        "accept": "text / html,'application/json', application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    response = requests.request("GET", api_url, headers=headers)
    try:
        payload = response.json()
    except:
        print(" NO Payload")
        payload = {"response.json()": ""}
    return render(request, 'vaccin_alerts_ml.html', payload)

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
        base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
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

# def get_feedback(request):
#     if request.method == 'POST':
#         email = request.GET.get('email')
#         message = request.GET.get('message')
#         c = Contact(email=email,message=message)
#         response = {"message":"Request/Feedbck sent successfully"}
#
#         return HttpResponse(simplejson.dumps(response), content_type='application/json')
