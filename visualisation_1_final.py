# Visualization 1

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.enable('json')

# Load data
names = pd.read_csv("data/dpt2020.csv", sep=";")
names.drop(names[names.preusuel == '_PRENOMS_RARES'].index, inplace=True)
names.drop(names[names.dpt == 'XX'].index, inplace=True)

# Streamlit app
st.title('Visualisation 1 : Baby names')

# Create a range of years from 1900 to 2020
names['annais'] = names['annais'].astype(int)
year_range = np.arange(1900, 2021, 1)

# Select the range using a slider
st.markdown("<b><small>Sélectionner une période</small></b>",
            unsafe_allow_html=True)
start_year, end_year = st.select_slider(
    "Year Range Slider", options=year_range, value=(1900, 2020), label_visibility="collapsed"
)

filtered_names = names[(names['annais'] >= start_year)
                       & (names['annais'] <= end_year)]

# Initialize session state for selected names
if 'selected_names' not in st.session_state:
    st.session_state.selected_names = []

# Function to add a name


def add_name():
    if name_to_add and name_to_add not in st.session_state.selected_names:
        st.session_state.selected_names.append(name_to_add)

# Function to remove a name


def remove_name():
    if name_to_remove in st.session_state.selected_names:
        st.session_state.selected_names.remove(name_to_remove)


# Ensure filtered data is not empty
if not filtered_names.empty:
    # Sum the counts per name for all regions and selected years
    aggregated_names = filtered_names.groupby(
        ['preusuel', 'sexe']).agg({'nombre': 'sum'}).reset_index()

    # Map gender to labels
    aggregated_names['gender'] = aggregated_names['sexe'].map(
        {1: 'Male', 2: 'Female'})

    # Filter top 20 male and top 20 female names
    top_20_males = aggregated_names[aggregated_names['sexe'] == 1].nlargest(
        20, 'nombre')
    top_20_females = aggregated_names[aggregated_names['sexe'] == 2].nlargest(
        20, 'nombre')

    # Invert the order for male names and set y-axis on the right
    top_20_males['nombre'] = -top_20_males['nombre']

    # Combine the datasets for males and females
    top_combined_names = pd.concat([top_20_males, top_20_females])

    # Create the top names chart for males
    top_males_chart = alt.Chart(top_20_males).mark_bar().encode(
        x=alt.X('nombre:Q', title='', axis=alt.Axis(labels=True, format='~s')),
        y=alt.Y('preusuel:N', title='', sort=None, axis=alt.Axis(
            orient='left', labels=False, ticks=False)),
        color=alt.value('blue'),
        tooltip=[alt.Tooltip('preusuel:N', title='prenom'), alt.Tooltip(
            'nombre:Q', title='nombre'), alt.Tooltip('gender:N', title='sexe')]
    ).properties(
        width=400,
        height=400
    )

    top_males_text = top_males_chart.mark_text(
        align='right',
        baseline='middle',
        dx=-3
    ).encode(
        text='preusuel:N',
        color=alt.value('white')
    )

    top_males_numbers = top_males_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3,
        color='blue'
    ).encode(
        text='nombre:Q'
    )

    # Create the top names chart for females
    top_females_chart = alt.Chart(top_20_females).mark_bar().encode(
        x=alt.X('nombre:Q', title='', axis=alt.Axis(labels=True, format='~s')),
        y=alt.Y('preusuel:N', title='', sort=None, axis=alt.Axis(
            orient='right', labels=False, ticks=False)),
        color=alt.value('pink'),
        tooltip=[alt.Tooltip('preusuel:N', title='prenom'), alt.Tooltip(
            'nombre:Q', title='nombre'), alt.Tooltip('gender:N', title='sexe')]
    ).properties(
        width=400,
        height=400
    )

    top_females_text = top_females_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3
    ).encode(
        text='preusuel:N',
        color=alt.value('white')
    )

    top_females_numbers = top_females_chart.mark_text(
        align='right',
        baseline='middle',
        dx=-3,
        color='pink'
    ).encode(
        text='nombre:Q'
    )

    top_combined_chart = alt.hconcat(
        (top_males_chart + top_males_text + top_males_numbers),
        (top_females_chart + top_females_text + top_females_numbers)
    ).resolve_scale(
        x='independent'
    ).properties(
        title='Top 20 des prénoms masculins et féminins les plus populaires'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Display the top combined chart
    st.altair_chart(top_combined_chart.configure_title(
        fontSize=24, anchor='start'), use_container_width=True)

    # Create columns for adding and removing names
    st.markdown("<b><small>Ajouter ou retirer des prénoms pour la courbe de popularité</small></b>",
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        name_to_add = st.selectbox(
            "Ajouter un prénom", aggregated_names['preusuel'].unique(), key='add_name_select', label_visibility="collapsed")
        if st.button("Ajouter", key='add_button'):
            add_name()

    with col2:
        name_to_remove = st.selectbox(
            "Retirer un prénom", st.session_state.selected_names, key='remove_name_select', label_visibility="collapsed")
        if st.button("Retirer", key='remove_button'):
            remove_name()

    # Filter data for the selected names and the selected years
    if st.session_state.selected_names:
        selected_names_data = names[(names['preusuel'].isin(st.session_state.selected_names)) &
                                    (names['annais'] >= start_year) &
                                    (names['annais'] <= end_year)]

        # Calculate the rank for each year
        yearly_counts = filtered_names.groupby(['annais', 'preusuel']).agg({
            'nombre': 'sum'}).reset_index()
        yearly_counts['rank'] = yearly_counts.groupby(
            'annais')['nombre'].rank(method='first', ascending=False)

        # Get the rank for the selected names
        name_rank_data = yearly_counts[yearly_counts['preusuel'].isin(
            st.session_state.selected_names)]

        # Create a selection that allows zooming
        zoom = alt.selection_interval(bind='scales')

        # Create the popularity over time chart
        popularity_chart = alt.Chart(name_rank_data).mark_line(point=alt.OverlayMarkDef(color='orange'), color='orange').encode(
            x=alt.X('annais:O', title='Année', axis=alt.Axis(format='d')),
            y=alt.Y('rank:Q', title='Rang', scale=alt.Scale(
                domain=(0, name_rank_data['rank'].max() + 1))),
            color=alt.Color('preusuel:N', title='Prénom'),
            tooltip=[alt.Tooltip('annais:O', title='annee'),
                     alt.Tooltip('rank:Q', title='rang')]
        ).properties(
            title="Popularité des prénoms au cours des années",
            width=1000,
            height=600
        ).add_selection(zoom)

        popularity_text = popularity_chart.mark_text(
            align='left',
            baseline='middle',
            dx=5, dy=-5,
            color='white'
        ).encode(
            text='rank:Q'
        )

        popularity_combined_chart = (popularity_chart + popularity_text).properties(
            title="Popularité des prénoms au cours des années"
        )

        # Display the popularity chart
        st.altair_chart(popularity_combined_chart.configure_title(
            fontSize=24, anchor='start'), use_container_width=False)
else:
    st.write("No data available for the selected year range.")
