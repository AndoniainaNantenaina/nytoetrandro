from datetime import date, datetime
from flask import Flask, jsonify, render_template, request
import requests
import os

from citydata.CityData import CityData
from utils.functions import create_connection, getAllFeeds
from weather.forecast import Forecast
from weather.weather import Weather

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

API_KEY = os.environ.get('API_KEY')

def getDataFromApi(city):

    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    response = requests.get(url).json()

    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        return 0

    #   Instanciation de la classe Weather
    W = Weather(
        city_name=city,
        dt=response['dt'],
        main_tmp=response['main']['temp'],
        main_tmp_max=response['main']['temp_max'],
        main_tmp_min=response['main']['temp_min'],
        weather_id=response['weather'][0]['id'],
        weather_main=response['weather'][0]['main'],
        weather_desc=response['weather'][0]['description'],
        weather_icon=response['weather'][0]['icon'],
        timezone=response['timezone']
    )

    #   Renvoyer la réponse
    return W

def getForecastData(city):
    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    response = requests.get(url).json()

    cod = response.get('cod')

    if cod == '200':

        #   La liste
        tz = response['city']['timezone']
        L = response['list']
        list = [Weather]

        for c in L:

            #   Ajouter les données dans la liste
            list.append(Weather(
                city_name=city,
                dt=c['dt'],
                main_tmp=c['main']['temp'],
                main_tmp_max=c['main']['temp_max'],
                main_tmp_min=c['main']['temp_min'],
                weather_id=c['weather'][0]['id'],
                weather_main=c['weather'][0]['main'],
                weather_desc=c['weather'][0]['description'],
                weather_icon=c['weather'][0]['icon'],
                timezone=tz
            ))

        return Forecast(
            count=len(list),
            list=list
        )

    else:
        return 0
        
@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response

# Route vers l'acceuil
@app.route('/')
def index():
    #   Tableau contenant les responses de tout les villes
    resTab = []

    #   Les villes à afficher sur la page d'acceuil
    index_cities = ["Antananarivo", "Paris", "Sydney", "New York"]

    for i in index_cities:
        city = i
        res = getDataFromApi(city=city)
        if res == 0:
            return render_template('error.html', err_city=city, err_msg="Error getting city information" )

        resTab.append(res.__dict__)
    
    return render_template('index.html', cities=index_cities, data=resTab)

# Route vers la page de recherche
@app.route('/search')
def search_page():
    return render_template('search_city.html')

@app.route('/about')
def about():
    return render_template('about.html', about=True)

@app.route('/credits')
def credits():
    return render_template('credits.html', credits=True)

# Route vers la recherche par ville
@app.route('/city')
def search_city():
    city = request.args.get('query')  # city name passed as argument

    #   Prendre les données
    response = getDataFromApi(city=city)
    forecast = getForecastData(city=city)

    if response == 0 and forecast == 0:
        return render_template('error.html', err_city=city, err_msg="Error getting city information" )
    
    # Prendre tout les données
    current_temperature = response.main_tmp
    temp_max = response.main_tmp_max
    temp_min = response.main_tmp_min
    weather_main = response.weather_main
    weather_desc = response.weather_desc
    weather_icon = response.weather_icon

    list_forecast = []
    for o in range(len(forecast.list) -1 ):
        list_forecast.append(forecast.list[o+1].__dict__)

    #   Si les données sont valide
    if current_temperature and temp_min and temp_max and weather_main and weather_desc and weather_icon :
        
        #   Afficher dans le template d'affichage
        return render_template(
            "current_data.html",
            cur_city=city, 
            temp=current_temperature, 
            tempmin=temp_min,
            tempmax=temp_max,
            weath_main=weather_main,
            weath_desc=weather_desc,
            weath_icon=weather_icon,
            l_forecast=list_forecast
        )
    else:
        #Afficher Erreur
        return f'Error getting weather data for {city.title()}'

@app.route('/feeds')
def feeds():

    listID = []

    commentaires = getAllFeeds()

    for c in commentaires:
        listID.append(c)
        
    return render_template('feeds.html', feeds=True, id=listID, flist=commentaires)
    
@app.route('/add_feeds', methods=['GET', 'POST'])
def add_feeds():

    f = create_connection()

    if request.method == 'POST' and len(dict(request.form)) > 0:
        userdata = dict(request.form)
        username = userdata["username"]
        commentaire = userdata["feed"]
        date=datetime.now().strftime("%d/%m/%Y %H h %M")

        new_data ={"username": username, "commentaire": commentaire, "Date": date}
        
        f.post("/Commentaire", new_data)

        newCom = getAllFeeds()
        
        listID = []
        for c in newCom:
            listID.append(c)
        
        return render_template('feeds.html', feeds=True, id=listID, flist=newCom)    
    else:
        return "Désolé, Impossible de rajouter votre commentaire."
