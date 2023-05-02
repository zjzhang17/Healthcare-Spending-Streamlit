import streamlit as st
import pandas as pd
import altair as alt
import streamlit as st
import plotly.express as px
import geopandas as gpd
import json


# Call set_page_config() at the beginning of your script
st.set_page_config(page_title="US Healthcare Spending")

# Load the data from a CSV file
df = pd.read_csv('USA_STATE_HEALTH_SPENDING.csv')
df = df[df['metric']=='Spending per capita']

def create_page1():
    st.title("Introduction")
    st.subheader("Overview of the US Healthcare System")
    text = "The US healthcare system is one of the most expensive in the world due to a variety of factors. One of the main reasons is the high cost of medical care and prescription drugs, which is driven by a lack of price regulation and negotiation, as well as the complexity of the healthcare system. Additionally, hospital fees have been increasing over time for a number of reasons. Some of the main factors contributing to rising hospital costs include technological advancements, administrative costs, and insurance coverage."
    st.write(text)
    image = "healthcare_expensive.jpeg"
    st.image(image, caption='Source: [https://molentax.com/why-is-healthcare-so-expensive/]')

# Define the function that creates the first page
def create_page2():
    st.title("US Healthcare Spending")
    st.subheader("2003-2019 US Healthcare Spending per Capita")

    # Create a selector for choosing the chart type
    chart_type = st.selectbox("Select Chart Type", ['Bar Chart', 'Line Chart'])

    if chart_type == 'Bar Chart':
        # Create the widgets for selecting the year and state
        subgroup_selector = st.selectbox("Type of Care & Payer", df['subgroup'].unique().tolist())
        state_selector = st.selectbox("Select a State", df['state'].unique().tolist())

        # Filter the data by the selected year and state
        filtered_data = df[(df['subgroup'] == subgroup_selector) & (df['state'] == state_selector)]

        # Create a bar chart using Altair
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x='year',
            y=alt.Y('val:Q', axis=alt.Axis(title='Per capita in USD'))
        )

        # Display the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)

    else:
        # Filter the data by the selected state
        filtered_data = df.groupby(['year', 'subgroup'])['val'].mean().reset_index()
        st.title("The Median Expenditure of Healthcare Services Over Time")
        # Create a line chart using Altair
        chart = alt.Chart(filtered_data).mark_line().encode(
            x='year',
            y=alt.Y('val:Q', axis=alt.Axis(title='per Capita in USD')),
            color='subgroup'
        )

        # Display the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)
        
with open("/Users/jasonzhang/Documents/USA_Health_Spending/map.json") as f:
    geomap = json.load(f)

    
def create_page3():
    st.title('Per Capita Spending by U.S. States: A Map Comparison from 2003 to 2019')
    df = pd.read_csv('USA_STATE_HEALTH_SPENDING.csv')
    df2 = df[df['metric']=='Spending per capita']
    
    # Create a slider widget in the sidebar for selecting years
    year = st.sidebar.slider("Select year", 2003, 2019, 2019)
    
    # Filter the data for the selected year
    df_filtered = df2[df2['year'] == year]
    
    fig = px.choropleth_mapbox(df_filtered,
                            geojson=geomap,
                            featureidkey='properties.NAME',
                            locations='state',
                            color='val',
                            color_continuous_scale="YlOrRd",
                            mapbox_style="carto-positron",
                            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5)
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    
    st.plotly_chart(fig)
    st.write('This map displays the per capita spending by U.S. states from 2003 to 2019. Alaska and Hawaii have the highest per capita spending among all U.S. states')









    






 








