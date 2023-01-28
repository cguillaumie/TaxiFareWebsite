import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import datetime


pick_up_adress = st.text_input("select pick-up adress", value = "45 Rockefeller Plaza, New York, NY 10111, United States")

                               
dropoff_adress = st.text_input("select dropoff adress" , value = "11 Wall St, New York, NY 10005, United States")
                               
                               
date_entry = st.date_input("Select a date")
                               
                           
time_entry = st.time_input("Select a time")
                                                       
passenger_count = st.select_slider("Select number of passenger", options=[1,2, 3, 4,5])
                                   
GOOGLE_API_KEY = "AIzaSyCsUnUor-GuaCrn7xivVkOVwTSf0XtagTU"
                                   
#https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key=YOUR_API_KEY  
GEOCODE_URL_pickup = "https://maps.googleapis.com/maps/api/directions/json?origin="pick_up_adress"&destination="dropoff_adress"&key="+GOOGLE_API_KEY
                                   
geo_response = requests.request("GET", GEOCODE_URL_pickup)
                                
result = json.loads(geo_response.text)
                                
pickup_latitude = result["results"][0]["geometry"]["location"]["lat"]
                                
pickup_longitude = result["results"][0]["geometry"]["location"]["lng"]
                                
GEOCODE_URL_dropoff =  "AIzaSyCsUnUor-GuaCrn7xivVkOVwTSf0XtagTU"
                                
geo_response1 = requests.request("GET", GEOCODE_URL_dropoff)
                                 
result1 = json.loads(geo_response1.text)
                                 
dropoff_latitude = result1["results"][0]["geometry"]["location"]["lat"]
                                 
dropoff_longitude = result1["results"][0]["geometry"]["location"]["lng"]
                                 
url = "https://taxifare.lewagon.ai/predict"
                                 
if url == "https://taxifare.lewagon.ai/predict":
                                   
    st.markdown("Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...")
                    
params =  {"pickup_datetime": f'{date_entry} {time_entry}',
                      
            "pickup_longitude": pickup_longitude,
                      
            "pickup_latitude": pickup_latitude,
                      
            "dropoff_longitude": dropoff_longitude,
                      
            "dropoff_latitude": dropoff_latitude,
                      
            "passenger_count": passenger_count}
                      
request = requests.get(url,params=params)
           
response = request.json()["fare"]
                          
st.write(f'You will pay {response} $')
                          
dict_pos = {
    "longitude": [pickup_longitude,dropoff_longitude],  
    "latitude": [pickup_latitude,dropoff_latitude],
}
                          
map_data = pd.DataFrame(dict_pos,index=[0,1])
                          
st.map(map_data)
                          
