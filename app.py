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


@app.route("/predict", methods=['GET', 'POST'])
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

        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        Total_stops=int(request.form['stops'])

        airline=request.form['airline']
        if(airline=='Jet Airways'):
            Jet_Airways=1
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif(airline=='IndiGo'):
            IndiGo=1
            Jet_Airways = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif(airline=='Air India'):
            Air_India=1
            Jet_Airways = 0
            IndiGo = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif(airline=='Multiple Carriers'):
            Multiple_carriers=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif(airline=='SpiceJet'):
            SpiceJet=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif(airline=='Vistara'):
            Vistara=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif(airline=='GoAir'):
            GoAir=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif(airline=='Multiple carriers Premium economy'):
            Multiple_carriers_Premium_economy=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif (airline=='Jet Airways Business'):
            Jet_Airways_Business=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
        
        elif (airline=='Vistara Premium economy'):
            Vistara_Premium_economy=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Trujet = 0 
        
        elif (airline=='Trujet'):
            Trujet=1
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
        

        Source=request.form['Source']
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0
        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0
        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        Source=request.form['Destination']
        if (Source == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        elif (Source == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        elif (Source == 'New_Delhi'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0
        elif (Source == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0
        elif (Source == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        prediction=model.predict([[Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min, Arrival_hour, Arrival_min, dur_hour, dur_min, Air_India, GoAir, IndiGo, Jet_Airways, Jet_Airways_Business, Multiple_carriers, Multiple_carriers_Premium_economy, SpiceJet, Trujet, Vistara,Vistara_Premium_economy, s_Chennai, s_Delhi, s_Kolkata, s_Mumbai, d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata, d_New_Delhi]])
        result=round(prediction[0], 2)

        return render_template('index.html', prediction_result=" Your flight fare will be around Rs."+result)

    return render_template('index.html')

if __name__=='main':
    app.run(debug=True)

    