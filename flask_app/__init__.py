# app.py
from flask import Flask, render_template, request
from flask_app.prediction import pred
#from flask_app.traffic_api import *

import psycopg2

host = 'Insert host'
user = 'Insert user'
password = 'Insert password'
database = 'Insert database'

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = conn.cursor()
logs = []

def create_app(config=None):
    app = Flask(__name__)
    
    @app.route('/',methods=('GET', 'POST')) # 접속하는 url
    def index():
        if request.method == "POST":
            spot_name = request.form.get('spot_name')
            pm10 = request.form.get('pm10')
            pm25 = request.form.get('pm25')
            O3 = request.form.get('O3')
            NO2 = request.form.get('NO2')
            CO = request.form.get('CO')
            SO2 = request.form.get('SO2')
            hour = request.form.get('hour')
            input = [spot_name, pm10, pm25, O3, NO2, CO, SO2, hour]
            logs.append(input)
            result = pred(input, logs, conn, cur)

            return render_template('index.html', spot_name=spot_name, pm10=pm10, pm25=pm25, O3=O3, NO2=NO2, CO=CO, SO2=SO2, hour=hour, result=result)
        
        elif request.method == "GET":
            spot_name = 'None'
            pm10 = "0"
            pm25 = "0"
            O3 = "0"
            NO2 = "0"
            CO = "0"
            SO2 = "0"
            hour = "0"
            input = [spot_name, pm10, pm25, O3, NO2, CO, SO2, hour]
            result = pred(input, logs, conn, cur)
            return render_template('index.html', spot_name=spot_name, pm10=pm10, pm25=pm25, O3=O3, NO2=NO2, CO=CO, SO2=SO2, hour=hour, result=result)

    return app

app = create_app()