import streamlit as st
import pandas as pd
import requests
import datetime
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

#st.set_page_config(
##    page_title="Web app",
 #   page_icon="🌍",
  #  layout="centered",  # wide
 #   initial_sidebar_state="auto")

#Title of the app
st.title("THIS WEB APP PREDICTS THE AVAILABILITY OF DIVVY BIKES UP TO FIVE DAYS IN ADVANCE")

#st.header("Select the date and time  to explore Divvy's stations traffic")

import streamlit as st
import datetime

# Title of the app
st.title("Select a Date and Time to predict bikes availability per station")

# Get current date and time
now = datetime.datetime.now()
max_date = now + datetime.timedelta(days=5)

# Obtain the user inputs
with st.form('Please provide the inputs'):
    selected_date = st.date_input('Select a date', value=now.date(), min_value=now.date(), max_value=max_date.date())
    selected_time = st.time_input('Select a time', value=now.time())
    submit_button = st.form_submit_button("Submit")

# Check if the selected date and time are valid
selected_datetime = datetime.datetime.combine(selected_date, selected_time)
if submit_button and selected_datetime > now:
    selected_datetime_bis = datetime.datetime.combine(selected_date, selected_time)
    st.success("All is set")
    st.write("Selected Date and Time:", selected_datetime_bis)

    # Create a dictionary with year, month, day, hour, minute, and second as keys
    datetime_dict = dict(
    year_input= int(selected_datetime.year),
    month_input= int(selected_datetime.month),
    day_input= int(selected_datetime.day),
    hour_input= int(selected_datetime.hour),
    min_input= int(selected_datetime.minute),
    sec_input = int(selected_datetime.second)
    )

    #Executing the API
    url='https://deparrpred-z2pwa4emra-ew.a.run.app/predict'
    params=datetime_dict

    response=requests.get(url=url, params=params)
    outcome=response.json()

    stations = pd.DataFrame.from_dict(outcome)


    stations['ratio'] = stations['nb_dep']/stations['nb_arr']
    stations['result'] = stations['ratio'].apply(lambda x: 1 if x > 1 else 0)


    st.header("Here is bikes availability per station on the selected date and time")



    # Step 3: Load the dataframe with latitude, longitude, and dummy_value variables
    # Replace 'df' with the name of your dataframe

    # Step 4: Create a map object
    m = folium.Map(location=[stations['lat'].mean(), stations['lng'].mean()], zoom_start=12)

    # Step 5: Create a MarkerCluster object
    marker_cluster = MarkerCluster(disableClusteringAtZoom=1).add_to(m)

    # Step 6: Add markers to the map
    for index, row in stations.iterrows():
        coord = (row['lat'], row['lng'])
        color = 'red' if row['result'] == 1 else 'green'
        label = f'<div style="font-size: 14px;">{row["station_name"]}</div>'
        folium.Marker(coord, icon=folium.Icon(color=color), popup=label).add_to(marker_cluster)

    # Step 7: Fit the map bounds to show all markers
    m.fit_bounds(marker_cluster.get_bounds())

    folium_static(m)


elif submit_button and selected_datetime <= now:
    st.error("Please select a date and time in the future")
