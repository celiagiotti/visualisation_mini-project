import streamlit as st
import pandas as pd
import altair as alt

# Load the data
names_data = pd.read_csv('./data/dpt2020.csv', sep=";")
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
st.title('Visualisation 3 : Baby names')

# Time period selector
years = names_data['annais'].unique()
start_year, end_year = st.slider('Sélectionner une période', int(years.min()), int(years.max()), (int(years.min()), int(years.max())))

# Filter data by selected period
filtered_data = names_data[(names_data['annais'] >= start_year) & (names_data['annais'] <= end_year)]

# Calculate metrics for Visualization 1
top_20_each_year = filtered_data.groupby(['annais', 'sexe', 'preusuel'])['nombre'].sum().reset_index()
top_20_each_year = top_20_each_year.groupby(['annais', 'sexe']).apply(lambda x: x.nlargest(20, 'nombre')).reset_index(drop=True)

avg_presence = top_20_each_year.groupby(['preusuel', 'sexe']).size().reset_index(name='count')
avg_presence = avg_presence.groupby('sexe')['count'].mean().reset_index()
avg_presence.columns = ['sexe', 'avg_years_in_top_20']

name_counts = filtered_data.groupby('sexe')['preusuel'].nunique().reset_index()
name_counts.columns = ['sexe', 'unique_names']

metrics = pd.merge(avg_presence, name_counts, on='sexe')

# Display metrics with colored text and icons
st.header('Nombre moyen d\'années de présence et nombre de prénoms par genre')
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<p style='font-size:16px;'>Homme - Années moyenne Top 20</p><p style='color:blue; font-size:32px; margin: -15px 0;'>"
                f"<img src='https://img.icons8.com/ios-filled/50/007bff/male.png' style='width:20px;vertical-align:middle;'> "
                f"{metrics[metrics['sexe'] == 'Homme']['avg_years_in_top_20'].values[0]:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px;'>Homme - Nombre de Prénoms</p><p style='color:blue; font-size:32px; margin: -15px 0;'>"
                f"<img src='https://img.icons8.com/ios-filled/50/007bff/male.png' style='width:20px;vertical-align:middle;'> "
                f"{metrics[metrics['sexe'] == 'Homme']['unique_names'].values[0]}</p>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<p style='font-size:16px;'>Femme - Années moyenne Top 20</p><p style='color:pink; font-size:32px; margin: -15px 0;'>"
                f"<img src='https://img.icons8.com/ios-filled/50/ff69b4/female.png' style='width:20px;vertical-align:middle;'> "
                f"{metrics[metrics['sexe'] == 'Femme']['avg_years_in_top_20'].values[0]:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px;'>Femme - Nombre de Prénoms</p><p style='color:pink; font-size:32px; margin: -15px 0;'>"
                f"<img src='https://img.icons8.com/ios-filled/50/ff69b4/female.png' style='width:20px;vertical-align:middle;'> "
                f"{metrics[metrics['sexe'] == 'Femme']['unique_names'].values[0]}</p>", unsafe_allow_html=True)

# Visualization 2: Number of times names appeared in the top 20 during the selected period
st.header('Nombre d\'années de présence dans le top 20 par période sélectionnée')

# Count the number of times each name appears in the top 20 during the selected period
top_names_presence = top_20_each_year.groupby(['preusuel', 'sexe']).size().reset_index(name='count')
top_names_presence = top_names_presence.sort_values('count', ascending=False).groupby('sexe').head(10)

chart2 = alt.Chart(top_names_presence).mark_bar().encode(
    x=alt.X('count:Q', title='Années de présence dans le top 20'),
    y=alt.Y('preusuel:N', sort='-x', title='Prénoms'),
    color=alt.Color('sexe:N', scale=alt.Scale(domain=['Homme', 'Femme'], range=['blue', 'pink'])),
    tooltip=['preusuel', 'count']
).properties(
    width=600,
    height=400
)

st.altair_chart(chart2)
