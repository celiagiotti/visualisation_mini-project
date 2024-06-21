import streamlit as st
import pandas as pd
import geopandas as gpd
import altair as alt
import folium
from streamlit_folium import folium_static

# Load the data
names_data = pd.read_csv('./data/dpt2020.csv', sep=";")
france_geo = gpd.read_file('./data/departements-avec-outre-mer.geojson')
departments_regions = pd.read_csv('./data/departements-region.csv')

# Ensure 'annais' column can be converted to numeric, and handle errors
names_data['annais'] = pd.to_numeric(names_data['annais'], errors='coerce')
names_data = names_data.dropna(subset=['annais'])
names_data['annais'] = names_data['annais'].astype(int)

# Exclude "_PRENOMS_RARES"
names_data = names_data[names_data['preusuel'] != '_PRENOMS_RARES']

# Map sex codes to labels
sex_mapping = {1: 'Homme', 2: 'Femme'}
names_data['sexe'] = names_data['sexe'].map(sex_mapping)

# Merge names_data with departments_regions to add the region information
names_data = names_data.merge(departments_regions, left_on='dpt', right_on='num_dep')

# Streamlit app
st.title('Visualisation 2 : Baby names')

# Time period selector
years = names_data['annais'].unique()
start_year, end_year = st.slider('Sélectionner une période', int(years.min()), int(years.max()), (int(years.min()), int(years.max())))

# Filter data by selected period
filtered_data = names_data[(names_data['annais'] >= start_year) & (names_data['annais'] <= end_year)]

# Visualization 1: Most popular names in France by gender
st.header('Top prénoms en France')
top_names_france = filtered_data.groupby(['preusuel', 'sexe'])['nombre'].sum().reset_index()
top_names_france = top_names_france.sort_values('nombre', ascending=False).groupby('sexe').head(10)

chart1 = alt.Chart(top_names_france).mark_bar().encode(
    x=alt.X('nombre:Q', title='Compte'),
    y=alt.Y('preusuel:N', sort='-x', title='Prénoms'),
    color=alt.Color('sexe:N', scale=alt.Scale(domain=['Homme', 'Femme'], range=['blue', 'pink'])),
    tooltip=['preusuel', 'nombre']
).properties(
    width=600,
    height=400
)

st.altair_chart(chart1)

# Visualization 2: Top names in a selected region
st.header('Top prénoms par région')
regions = filtered_data['region_name'].unique()
selected_region = st.selectbox('Sélectionner une région', regions)

region_data = filtered_data[filtered_data['region_name'] == selected_region]
top_names_region = region_data.groupby(['preusuel', 'sexe'])['nombre'].sum().reset_index()
top_names_region = top_names_region.sort_values('nombre', ascending=False).groupby('sexe').head(10)

chart2 = alt.Chart(top_names_region).mark_bar().encode(
    x=alt.X('nombre:Q', title='Compte'),
    y=alt.Y('preusuel:N', sort='-x', title='Prénoms'),
    color=alt.Color('sexe:N', scale=alt.Scale(domain=['Homme', 'Femme'], range=['blue', 'pink'])),
    tooltip=['preusuel', 'nombre']
).properties(
    width=600,
    height=400
)

st.altair_chart(chart2)

# Visualization 3: Map with top names by region
st.header('Carte du top prénoms par région')

# Get top names for each region
def get_top_names_by_region(data):
    top_names = data.groupby(['region_name', 'sexe', 'preusuel', 'annais'])['nombre'].sum().reset_index()
    top_names = top_names.sort_values('nombre', ascending=False).groupby(['region_name', 'sexe']).first().reset_index()
    top_names_wide = top_names.pivot(index='region_name', columns='sexe', values='preusuel').reset_index()
    return top_names_wide

top_names_map = get_top_names_by_region(filtered_data)

# Merge top names with the GeoDataFrame by creating a region-based GeoDataFrame
# Aggregate the department geometries by region
france_geo['region_name'] = france_geo['code'].map(departments_regions.set_index('num_dep')['region_name'])
regions_geo = france_geo.dissolve(by='region_name', aggfunc='sum').reset_index()

# Merge top names with the regions GeoDataFrame
regions_geo = regions_geo.merge(top_names_map, on='region_name', how='left')

# Create a folium map centered on France
m = folium.Map(location=[46.603354, 1.888334], zoom_start=5)

# Add GeoJSON data to the map with style and popups for top names
def style_function(feature):
    return {
        'fillColor': 'blue',
        'color': 'blue',
        'weight': 2,
        'dashArray': '5, 5',
        'fillOpacity': 0.6,
    }

def highlight_function(feature):
    return {
        'fillColor': 'yellow',
        'color': 'yellow',
        'weight': 2,
        'dashArray': '5, 5',
        'fillOpacity': 0.6,
    }

def popup_html(row):
    region = row['region_name']
    male_name = row.get('Homme', 'N/A')
    female_name = row.get('Femme', 'N/A')
    return f"<strong>{region}</strong><br>Top Nom Homme: {male_name}<br>Top Nom Femme: {female_name}"

# Use the correct column names for top male and female names
for _, row in regions_geo.iterrows():
    folium.GeoJson(
        data=row['geometry'].__geo_interface__,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.Tooltip(popup_html(row)),
    ).add_to(m)

# Display the map with Streamlit
folium_static(m)
