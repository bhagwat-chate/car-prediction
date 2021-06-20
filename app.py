#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask
from flask import render_template
from flask import request
# import jsonify
import requests
import pickle
import numpy as np
import pandas as pd


# In[4]:


app = Flask(__name__)

model = pickle.load(open('random_forest_regression_model.pkl','rb'))

@app.route('/', methods = ['GET'])

def Home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    
    Fuel_Type_Diesel = 0
    
    if request.methods =='POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Diesel = 1
            Fuel_Type_Petrol = 0
            
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 0
            
        Year = 2021 - Year
        
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
            
        Transmission_Mannual = request.form['Transmission_Mannual']
        if(Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
            
        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                Seller_Type_Individual, Transmission_Mannual]])
    
        output = round(prediction[0], 2)
    
        if output < 0:
            return render_template('index.html', prediction_texts = 'Sorry, you can not Sell this car {}'.fotmat(output))
        else:
            return render_template('index.html', prediction_texts = 'You can sell the car at {}'.format(output))
    
    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug = False)


# In[ ]:




