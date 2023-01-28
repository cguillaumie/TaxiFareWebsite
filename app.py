import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import datetime

from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import ColumnDataSource
from bokeh.palettes import Set3
from bokeh.palettes import Category20
from bokeh.palettes import RdBu3
from bokeh.resources import CDN
from bokeh.embed import file_html
import streamlit.components.v1 as components




st.title("Taxifare Website")

pick_up_adress = st.text_input("select pick-up adress", value = "45 Rockefeller Plaza, New York, NY 10111, United States")

                               
dropoff_adress = st.text_input("select dropoff adress" , value = "11 Wall St, New York, NY 10005, United States")
                               
                               
date_entry = st.date_input("Select a date")
                               
                           
time_entry = st.time_input("Select a time")
                                                       
passenger_count = st.select_slider("Select number of passenger", options=[1,2, 3, 4,5])
                                   
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
                                   
# GEOCODE_URL_dir = f'https://maps.googleapis.com/maps/api/directions/json?origin={pick_up_adress}&destination={dropoff_adress}&key={GOOGLE_API_KEY}'


GEOCODE_URL_pickup = f'https://maps.googleapis.com/maps/api/geocode/json?address={pick_up_adress}&key={GOOGLE_API_KEY}'


GEOCODE_URL_dropoff= f'https://maps.googleapis.com/maps/api/geocode/json?address={dropoff_adress}&key={GOOGLE_API_KEY}'

                                   
geo_response1 = requests.request("GET", GEOCODE_URL_pickup)
                                
result1 = json.loads(geo_response1.text)
  
geo_response2 = requests.request("GET", GEOCODE_URL_dropoff)

result2 = json.loads(geo_response2.text)

pickup_latitude = result1['results'][0]['geometry']['location']['lat']

pickup_longitude = result1['results'][0]['geometry']['location']['lng']

dropoff_latitude = result2['results'][0]['geometry']['location']['lat']

dropoff_longitude = result2['results'][0]['geometry']['location']['lng']

                                                               
url = "https://taxifare.lewagon.ai/predict"
                                                   
params =  {"pickup_datetime": f'{date_entry} {time_entry}',
                      
            "pickup_longitude": pickup_longitude,
                      
            "pickup_latitude": pickup_latitude,
                      
            "dropoff_longitude": dropoff_longitude,
                      
            "dropoff_latitude": dropoff_latitude,
                      
            "passenger_count": passenger_count}
                      
request = requests.get(url,params=params)
           
response = round(request.json()["fare"],2)
                          
st.write(f'You will pay {response} $')
                          

#map_data = pd.DataFrame(dict_pos,index=[0,1])
                          
#st.map(map_data)
                          
  
bokeh_width, bokeh_height = 800,600



def plotMap(zoom=10, map_type='roadmap'):
    dict_pos = {
    "longitude": [pickup_longitude,dropoff_longitude],  
    "latitude": [pickup_latitude,dropoff_latitude],
    }
    centered_long = (pickup_longitude + dropoff_longitude) /2
    centered_lat = (pickup_latitude + dropoff_latitude) / 2                     
    
    gmap_options = GMapOptions(lat=centered_lat, lng=centered_long, map_type=map_type, zoom=zoom)  
    p = gmap(GOOGLE_API_KEY, gmap_options, title='Taxifare Map', width=bokeh_width, height=bokeh_height)
    
    #latArr = []
    #longArr = []
    #colorArr = []
    #labelArr = []
    #colidx = 0
    #colpalette = Category20.get(20)
    #print('palette length:', len(Set3))
    
      
    p.circle(x='longitude', y='latitude', size=10, alpha=0.9, color='blue', source= dict_pos)
   
    html = file_html(p, CDN, "pickup_dropoff")
    return html
  
components.html(plotMap(13, 'roadmap'), height = bokeh_height, width = bokeh_width)

