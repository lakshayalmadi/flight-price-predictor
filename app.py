from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import numpy as np
import pickle
import pandas as pd
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
model = pickle.load(open('flight_model.pkl', 'rb'))


@app.route('/')
@cross_origin()
def homepage():
    return render_template('index.html')


@app.route("/predict", mehtods=['GET', 'POST'])
@cross_origin()
def predict():
    if request.method=='POST':
        date_dep=request.form['Dep_Time']
        Journey_day=int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month=int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        Dep_hour=int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min=int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        date_arrival=request.form['Arrival_Time']
        Arrival_hour=int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min=int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        Total_stops=int(request.form['stops'])

        airline=request.form['airline']
        Jet_Airways = 0, IndiGo = 0, Air_India = 0, Multiple_carriers = 0, SpiceJet = 0, Vistara = 0, GoAir = 0, Multiple_carriers_Premium_economy = 0, Jet_Airways_Business = 0, Vistara_Premium_economy = 0, Trujet = 0 
        if(airline=='Jet Airways'):
            Jet_Airways=1
        elif(airline=='IndiGo'):
            IndiGo=1
        elif(airline=='Air India'):
            Air_India=1
        elif(airline=='Multiple Carriers'):
            Multiple_carriers=1
        elif(airline=='SpiceJet'):
            SpiceJet=1
        elif(airline=='Vistara'):
            Vistara=1
        elif(airline=='GoAir'):
            GoAir=1
        elif(airline=='Multiple carriers Premium economy'):
            Multiple_carriers_Premium_economy=1
        elif (airline=='Jet Airways Business'):
            Jet_Airways_Business=1
        elif (airline=='Vistara Premium economy'):
            Vistara_Premium_economy=1
        elif (airline=='Trujet'):
            Trujet=1

        Source=request.form['Source']
        s_Delhi=0, s_Kolkata=0, s_Mumbai=0, s_Chennai=0
        if (Source == 'Delhi'):
            s_Delhi=1
        elif (Source == 'Kolkata'):
            s_Kolkata=1
        elif (Source == 'Mumbai'):
            s_Mumbai=1
        elif (Source == 'Chennai'):
            s_Chennai=1

        Source=request.form['Destination']
        d_Cochin = 0, d_Delhi = 0, d_New_Delhi = 0, d_Hyderabad = 0, d_Kolkata = 0