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
names_data = names_data.merge(
    departments_regions, left_on='dpt', right_on='num_dep')

# Streamlit app
st.title('Visualisation 3 : Baby names')

# Time period selector
years = names_data['annais'].unique()
start_year, end_year = st.slider('Sélectionner une période', int(
    years.min()), int(years.max()), (int(years.min()), int(years.max())))

# Filter data by selected period
filtered_data = names_data[(names_data['annais'] >= start_year) & (
    names_data['annais'] <= end_year)]

# Calculate metrics for Visualization 1
top_20_each_year = filtered_data.groupby(['annais', 'sexe', 'preusuel'])[
    'nombre'].sum().reset_index()
top_20_each_year = top_20_each_year.groupby(['annais', 'sexe']).apply(
    lambda x: x.nlargest(20, 'nombre')).reset_index(drop=True)

avg_presence = top_20_each_year.groupby(
    ['preusuel', 'sexe']).size().reset_index(name='count')
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
st.header('Nombre d\'années de présence dans le top 20 dans la période sélectionnée')

# Count the number of times each name appears in the top 20 during the selected period
top_names_presence = top_20_each_year.groupby(
    ['preusuel', 'sexe']).size().reset_index(name='count')
top_names_presence = top_names_presence.sort_values(
    'count', ascending=False).groupby('sexe').head(10)

# Average presence bar data
avg_presence_bars = avg_presence.copy()
avg_presence_bars['preusuel'] = avg_presence_bars['sexe'].apply(
    lambda x: 'MOYENNE ' + x)
avg_presence_bars['count'] = avg_presence_bars['avg_years_in_top_20']

# Combine top names presence with avg presence bars
combined_presence = pd.concat(
    [top_names_presence, avg_presence_bars[['preusuel', 'sexe', 'count']]])

chart2 = alt.Chart(combined_presence).mark_bar().encode(
    x=alt.X('count:Q', title='Années de présence dans le top 20'),
    y=alt.Y('preusuel:N', sort='-x', title='Prénoms'),
    color=alt.Color('sexe:N', scale=alt.Scale(
        domain=['Homme', 'Femme'], range=['blue', 'pink'])),
    tooltip=['preusuel', 'count']
).properties(
    width=800,
    height=600
)

st.altair_chart(chart2)


# Visualization 3: Scatter plot
st.header('Nuage de points des prénoms dans le top 20 dans la période sélectionnée')

# Filter scatter data to only include top 20 names from Visualization 2
top_names = top_names_presence['preusuel'].unique()
filtered_top_names_data = filtered_data[filtered_data['preusuel'].isin(
    top_names)]

# Calculate metrics for scatter plot
avg_year = filtered_top_names_data.groupby(['preusuel', 'sexe'])[
    'annais'].mean().reset_index()
total_births = filtered_top_names_data.groupby(['preusuel', 'sexe'])[
    'nombre'].sum().reset_index()
top_20_avg_presence = top_20_each_year.groupby(['preusuel', 'sexe'])[
    'annais'].size().reset_index(name='avg_years_in_top_20')

scatter_data = pd.merge(avg_year, total_births, on=['preusuel', 'sexe'])
scatter_data = scatter_data.merge(
    top_20_avg_presence, on=['preusuel', 'sexe'], how='left')

chart3 = alt.Chart(scatter_data).mark_circle().encode(
    x=alt.X('annais:Q', title='Année moyenne à laquelle un prénom est donné',
            scale=alt.Scale(domain=[start_year, end_year]), axis=alt.Axis(format='d')),
    y=alt.Y('avg_years_in_top_20:Q',
            title='Nombre d\'années moyen dans le top 20'),
    size=alt.Size('nombre:Q', title='Nombre total de naissances',
                  scale=alt.Scale(range=[100, 2000])),
    color=alt.Color('sexe:N', scale=alt.Scale(
        domain=['Homme', 'Femme'], range=['blue', 'pink'])),
    tooltip=[
        alt.Tooltip('preusuel:N', title='Prénom'),
        alt.Tooltip('annais:Q', title='Année moyenne'),
        alt.Tooltip('avg_years_in_top_20:Q', title='Cumul années top 20'),
        alt.Tooltip('nombre:Q', title='Nombre de naissances')
    ]
).properties(
    width=800,
    height=600
).interactive()

# Customize legend to ensure visibility on dark background
chart3 = chart3.configure_legend(
    labelColor='white',
    titleColor='white',
    titleFontSize=12,
    labelFontSize=10,
    symbolFillColor='white',
    symbolStrokeColor='black',
    symbolStrokeWidth=1,
    symbolSize=200
)

st.altair_chart(chart3)
