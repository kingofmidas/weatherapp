from django.shortcuts import render, redirect
import requests
# Create your views here.
from .models import City
from .forms import CityForm

def index(request):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3b7c300dce840315ca02ecc79d3945cf'
    
    err_msg = ''
    message = ''
    message_class = ''

    if(request.method=='POST'):
        form = CityForm(request.POST)
        if form.is_valid():
            name_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=name_city).count()
            if not existing_city_count:
                r = requests.get(url.format(name_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "Такого города не существует"
            else:
                err_msg = 'Город уже существует в базе данных'


        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = "Город успешно добавлен"
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        city_weather = {

            'city':city.name,
            'temp' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form': form,
        'message' : message,
        'message_class': message_class,
    }
    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')