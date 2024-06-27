import streamlit as st
import pandas as pd
import geopandas as gpd
import altair as alt
import folium
from streamlit_folium import folium_static
import branca

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
names_data = names_data.merge(
    departments_regions, left_on='dpt', right_on='num_dep')

# Streamlit app
st.title('Visualisation 2 : Baby names')

# Time period selector
years = names_data['annais'].unique()
start_year, end_year = st.slider('Sélectionner une période', int(
    years.min()), int(years.max()), (int(years.min()), int(years.max())))

# Filter data by selected period
filtered_data = names_data[(names_data['annais'] >= start_year) & (
    names_data['annais'] <= end_year)]

# Visualization 1: Most popular names in France by gender
st.header('Top prénoms en France et par région')
top_names_france = filtered_data.groupby(['preusuel', 'sexe'])[
    'nombre'].sum().reset_index()
top_names_france = top_names_france.sort_values(
    'nombre', ascending=False).groupby('sexe').head(10)

chart1 = alt.Chart(top_names_france).mark_bar().encode(
    x=alt.X('nombre:Q', title='Compte', axis=alt.Axis(format=',d')),
    y=alt.Y('preusuel:N', sort='-x', title='Prénom'),
    color=alt.Color('sexe:N', scale=alt.Scale(
        domain=['Homme', 'Femme'], range=['blue', 'pink'])),
    tooltip=['preusuel', 'nombre']
).properties(
    width=700,
    height=600,
    title='Top 20 national'
)

# Visualization 2: Top names in a selected region
regions = filtered_data['region_name'].unique()
selected_region = st.selectbox('Sélectionner une région', regions)

region_data = filtered_data[filtered_data['region_name'] == selected_region]
top_names_region = region_data.groupby(['preusuel', 'sexe'])[
    'nombre'].sum().reset_index()
top_names_region = top_names_region.sort_values(
    'nombre', ascending=False).groupby('sexe').head(10)

chart2 = alt.Chart(top_names_region).mark_bar().encode(
    x=alt.X('nombre:Q', title='Compte', axis=alt.Axis(format=',d'), scale=alt.Scale(domain=[0, max(
        top_names_france['nombre'].max()/15, top_names_region['nombre'].max())])),
    y=alt.Y('preusuel:N', sort='-x', title='Prénom'),
    color=alt.Color('sexe:N', scale=alt.Scale(
        domain=['Homme', 'Femme'], range=['blue', 'pink'])),
    tooltip=['preusuel', 'nombre']
).properties(
    width=500,
    height=600,
    title=f'Top 20 - {selected_region}'
)

# Apply custom CSS to adjust margins
st.markdown(
    """
    <style>
    .marks {  /* class of main container */
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adjust the spacing between the two charts
chart_combined = alt.hconcat(chart1, chart2).resolve_scale(x='independent')

# Create a layout with Streamlit columns
col1, col2 = st.columns([1, 10])

with col1:
    st.write("")  # Empty column for spacing

with col2:
    st.altair_chart(chart_combined, use_container_width=True)

# Visualization 3: Map with top names by region
st.header("Carte de densité d'un prénom par région")

# Add a name selector for the heatmap
selected_name = st.selectbox(
    'Sélectionner un prénom pour la carte de densité', names_data['preusuel'].unique())

# Calculate density
total_births_by_region = filtered_data.groupby(
    'region_name')['nombre'].sum().reset_index()
name_births_by_region = filtered_data[filtered_data['preusuel'] == selected_name].groupby(
    'region_name')['nombre'].sum().reset_index()
density_data = pd.merge(name_births_by_region, total_births_by_region,
                        on='region_name', suffixes=('_name', '_total'))
density_data['density'] = density_data['nombre_name'] / \
    density_data['nombre_total']

# Merge top names with the GeoDataFrame by creating a region-based GeoDataFrame
# Aggregate the department geometries by region
france_geo['region_name'] = france_geo['code'].map(
    departments_regions.set_index('num_dep')['region_name'])
regions_geo = france_geo.dissolve(
    by='region_name', aggfunc='sum').reset_index()

# Merge density data with the GeoDataFrame
regions_geo = regions_geo.merge(
    density_data[['region_name', 'density']], on='region_name', how='left')
regions_geo['density'] = regions_geo['density'].fillna(
    0)  # Fill NaN values with 0

# Define the colormap with dynamic range based on the density values
min_density = regions_geo['density'].min()
max_density = regions_geo['density'].max()
colormap = branca.colormap.linear.RdYlBu_09.scale(min_density, max_density)

def style_function(feature):
    density = feature['properties'].get('density', 0)
    return {
        'fillColor': colormap(density),
        'color': 'gray',
        'weight': 1,
        'fillOpacity': 0.6,
    }


def highlight_function(feature):
    return {
        'fillColor': 'yellow',
        'color': 'yellow',
        'weight': 1,
        'fillOpacity': 0.6,
    }


def popup_html(row):
    region = row['region_name']
    density = row.get('density', 'N/A')
    return f"<strong>{region}</strong><br>Densité du prénom {selected_name}: {density:.4f}"


# Create a folium map centered on France
m = folium.Map(location=[46.603354, 1.888334], zoom_start=5, tiles=None)
folium.TileLayer('cartodbpositron').add_to(m)

# Add GeoJSON data to the map with style and popups for density
for _, row in regions_geo.iterrows():
    feature = {
        'type': 'Feature',
        'properties': {'region_name': row['region_name'], 'density': row['density']},
        'geometry': row['geometry'].__geo_interface__
    }
    folium.GeoJson(
        data=feature,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.Tooltip(popup_html(row)),
    ).add_to(m)

# Add colormap to the map
colormap.caption = 'Densité du prénom'
colormap.add_to(m)

# Display the map with Streamlit
folium_static(m)
