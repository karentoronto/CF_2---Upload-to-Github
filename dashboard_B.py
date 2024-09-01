############################################### Citibike DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
from streamlit_keplergl import keplergl_static
from PIL import Image
from numerize import numerize


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'NYC Citi Bike Sharing Strategy Dashboard', layout='wide')
st.title("NYC Citi Bike Sharing Strategy Dashboard")

## Define Side Bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])
########################## Import data ###########################################################################################

df = pd.read_csv('df_final_updated_season.csv', index_col = 0)
# top20 = pd.read_csv('top20_updated.csv', index_col = 0)


############################################ DEFINE THE PAGES #####################################################################

### INTRO PAGE

if page == 'Intro page':
    st.markdown("The dashboard will help make NYC Citi Bike make informed decisions that will circumvent availability issues.")
    st.markdown("The high demand for bike sharing in NYC has led to a distribution problem. This dashboard is a descriptive analysis of existing data and presents actionable insighs to the business strategy team to avoid a distribution problem and ensure the company's position as a leader in eco-friendly transportation solutions in the city.")

    st.markdown('#### Overall Approach:')
    st.markdown('1. Define Objective')
    st.markdown('2. Source Data')
    st.markdown('3. Interactive Visualizations')
    st.markdown('4. Geospatial Plot')
    st.markdown('5. Dashboard Creation')
    st.markdown('6. Findings and Recommendations')
    
    st.markdown('#### Dashboard Sections:')
    st.markdown('- Weather component and bike usage')
    st.markdown('- Most popular stations')
    st.markdown('- Interactive map with aggregated bike trips')
    st.markdown('- Recommendations')
    st.markdown('The dropdown menu on the left under "Aspect Selector" will take you to the different aspects of the analysis our team looked at.')
    
    myImage = Image.open('citi_bike.jpg') 
    st.image(myImage)
    st.markdown('Source: https://www.nyc.gov/office-of-the-mayor/news/576-18/mayor-de-blasio-dramatic-expansion-citi-bike#/0')
   



# # # # ######################################### DEFINE THE CHARTS #####################################################################

elif page == 'Weather component and bike usage':
### Create the dual axis line chart page ###

  fig_2= make_subplots(specs=[[{"secondary_y": True}]])


  fig_2.add_trace(
      go.Scatter(
          x=df['date'],
          y=df['bike_rides_daily'],
          name='Daily bike rides',
          line=dict(color='blue')
      ),
      secondary_y=False
  )

  # Adding the second trace
  fig_2.add_trace(
      go.Scatter(
          x=df['date'],
          y=df['avgTemp'],
          name='Daily temperature',
          line=dict(color='red')
      ),
      secondary_y=True
  )

  # Setting titles for the axes
  fig_2.update_layout(
      title_text="Daily Bike Rides and Temperature",
      xaxis_title="Date",
      yaxis_title="Bike Rides",
      yaxis2_title="Temperature"
  )

  st.plotly_chart(fig_2, use_container_width=True)


  st.markdown("There is a correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily.")
  st.markdown("As temperatures drop, so does bike usage. As temperatures increase, bike usage also trends upward. This insight indicates that the shortage problem may be prevalent in the warmer months, approximately between May and July.")


# Most Popular Bike Stations Page

elif page == 'Most popular stations':

    # Create the seasons filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label = 'Select the season', options = df['season'].unique(),
    default = df['season'].unique())

    df1 = df.query('season == @season_filter')
   
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value = numerize.numerize(total_rides))



  ## Bar chart

    df1['trips']=1
    df_groupby_bar = df1.groupby('start_station_name', as_index=False).agg({'trips': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'trips')


    fig_1 = px.bar(data_frame = top20, 
              x = 'start_station_name', 
              y ='trips', 
              color= 'trips', 
              color_continuous_scale ='ice_r')

    fig_1.update_layout({
      'title': {'text': 'Top 20 Bike-Sharing Facilities Operated by Citi Bike', 'font': {'weight': 'bold'}},
      'xaxis': {'title': {'text': 'Start Station Name', 'font': {'weight': 'bold'}}, 'tickfont': {'size': 10}},
      'yaxis': {'title': {'text': 'Number of Trips', 'font': {'weight': 'bold'}}}
  })


    st.plotly_chart(fig_1, use_container_width=True)
    st.markdown('The top 3 most popular stations are: W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St. These are stations that we can cross reference with the geospatial plot to see if these stations also account for the most popular routes.') 



# ### Create the Map ###
elif page == 'Interactive map with aggregated bike trips': 

    path_to_html = "NYC Bike Sharing Trips Aggregated_Updated.html" 

    # Read file and keep in 
    # variable
    with open(path_to_html, 'r') as f: 
        html_data = f.read()

    # Show in webpage
    st.header('Aggregated Bike Trips in NYC - 2022')
    st.components.v1.html(html_data,height = 1000)
    st.markdown('#### Using the filter on the left hand side of the map, we can check whether the most popular start stations also appear in the most popular trips.')
    st.markdown("The most popular start stations are W 21 st & 6 Ave, West St/Chambers St, Broadway/W 58 St. While having the aggregated bike trips filter enabled, the most popular starting stations are not always associated with the most common routes taken.")
    st.markdown('Some of the most common routes are between 12 Ave/W 40 St and West St/Chambers St, Pier 40-Hudson River Park and West St & Chamber St, which are located along the water.')

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("citi_bike_part2.jpg")  #source: https://www.bloomberg.com/news/articles/2023-07-17/bikeshare-participation-is-growing-fast-in-nyc-boston
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown("- There is a clear correlation between temperature and number of bike trips. Ensure that bikes are fully stocked in all the popular stations during the warmer months between May and July  in order to meet the higher demand, but provide a lower supply in winter and late autumn.")
    st.markdown("- Ensure the starting stations on popular routes such as those by the river side are well stocked. The routes are as follows: (1) between 12 Avenue & West 40th St and West St & Chamber St; (2) Pier 40-Hudson River Park and West St & Chamber St; (3) North Moore St & Greenwich St and Versey & Church; (4) McGuiness Blvd & Eagle St and Vernon Blvd & 50 Ave.")
    