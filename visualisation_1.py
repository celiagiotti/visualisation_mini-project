import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.enable('json')

# Load data
names = pd.read_csv("dpt2020.csv", sep=";")
names.drop(names[names.preusuel == '_PRENOMS_RARES'].index, inplace=True)
names.drop(names[names.dpt == 'XX'].index, inplace=True)

# Create a range of years from 1900 to 2020 (the minimum and maximum years in the dataset)
names['annais'] = names['annais'].astype(int)
year_range = np.arange(1900, 2021, 1)

# Select the range using a slider (for the visualisation in Streamlit)
st.markdown("<b><small>Select a range of years</small></b>",
            unsafe_allow_html=True)
start_year, end_year = st.select_slider(
    "Year Range Slider", options=year_range, value=(1900, 2020), label_visibility="collapsed")

filtered_names = names[(names['annais'] >= start_year)
                       & (names['annais'] <= end_year)]

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

    # Filter least 20 male and least 20 female names
    least_20_males = aggregated_names[aggregated_names['sexe'] == 1].nsmallest(
        20, 'nombre')
    least_20_females = aggregated_names[aggregated_names['sexe'] == 2].nsmallest(
        20, 'nombre')

    # Invert the order for male names and set y-axis on the right
    top_20_males['nombre'] = -top_20_males['nombre']
    least_20_males['nombre'] = -least_20_males['nombre']

    # Combine the datasets for males and females
    top_combined_names = pd.concat([top_20_males, top_20_females])
    least_combined_names = pd.concat([least_20_males, least_20_females])

    # Create the top names chart for males
    top_males_chart = alt.Chart(top_20_males).mark_bar().encode(
        x=alt.X('nombre:Q', title='', axis=alt.Axis(labels=True, format='~s')),
        y=alt.Y('preusuel:N', title='', sort=None, axis=alt.Axis(
            orient='left', labels=False, ticks=False)),
        color=alt.value('blue'),
        tooltip=['preusuel', 'nombre', 'gender']
    ).properties(
        width=300,
        height=400
    )

    top_males_text = top_males_chart.mark_text(
        align='right',
        baseline='middle',
        dx=-3
    ).encode(
        text='preusuel:N'
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
        color=alt.value('violet'),
        tooltip=['preusuel', 'nombre', 'gender']
    ).properties(
        width=300,
        height=400
    )

    top_females_text = top_females_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3
    ).encode(
        text='preusuel:N'
    )

    top_females_numbers = top_females_chart.mark_text(
        align='right',
        baseline='middle',
        dx=-3,
        color='violet'
    ).encode(
        text='nombre:Q'
    )

    top_combined_chart = alt.hconcat(
        (top_males_chart + top_males_text + top_males_numbers),
        (top_females_chart + top_females_text + top_females_numbers)
    ).resolve_scale(
        x='independent'
    ).properties(
        title='Top 20 Male and Female Names'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Create the least names chart for males
    least_males_chart = alt.Chart(least_20_males).mark_bar().encode(
        x=alt.X('nombre:Q', title='', axis=alt.Axis(labels=True, format='~s')),
        y=alt.Y('preusuel:N', title='', sort=None, axis=alt.Axis(
            orient='left', labels=False, ticks=False)),
        color=alt.value('blue'),
        tooltip=['preusuel', 'nombre', 'gender']
    ).properties(
        width=300,
        height=400
    )

    least_males_text = least_males_chart.mark_text(
        align='right',
        baseline='middle',
        dx=-3
    ).encode(
        text='preusuel:N'
    )

    least_males_numbers = least_males_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3,
        color='blue'
    ).encode(
        text='nombre:Q'
    )

    # Create the least names chart for females
    least_females_chart = alt.Chart(least_20_females).mark_bar().encode(
        x=alt.X('nombre:Q', title='', axis=alt.Axis(labels=True, format='~s')),
        y=alt.Y('preusuel:N', title='', sort=None, axis=alt.Axis(
            orient='right', labels=False, ticks=False)),
        color=alt.value('violet'),
        tooltip=['preusuel', 'nombre', 'gender']
    ).properties(
        width=300,
        height=400
    )

    least_females_text = least_females_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3
    ).encode(
        text='preusuel:N'
    )

    least_females_numbers = least_females_chart.mark_text(
        align='right',
        baseline='middle',
        dx=-3,
        color='violet'
    ).encode(
        text='nombre:Q'
    )

    least_combined_chart = alt.hconcat(
        (least_males_chart + least_males_text + least_males_numbers),
        (least_females_chart + least_females_text + least_females_numbers)
    ).resolve_scale(
        x='independent'
    ).properties(
        title='Least 20 Male and Female Names'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Create columns for layout
    col1, col2 = st.columns([2, 3])

    # Select a name for the popularity chart in the right column
    with col2:
        st.markdown("<b><small>Select a name</small></b>",
                    unsafe_allow_html=True)
        name_selected = st.selectbox(
            "Name Select Box", aggregated_names['preusuel'].unique(), label_visibility="collapsed")

    # Filter data for the selected name and the selected years
    name_data = names[(names['preusuel'] == name_selected) & (
        names['annais'] >= start_year) & (names['annais'] <= end_year)]

    # Calculate the rank for each year
    yearly_counts = filtered_names.groupby(['annais', 'preusuel']).agg({
        'nombre': 'sum'}).reset_index()
    yearly_counts['rank'] = yearly_counts.groupby(
        'annais')['nombre'].rank(method='first', ascending=False)

    # Get the rank for the selected name
    name_rank_data = yearly_counts[yearly_counts['preusuel'] == name_selected]

    # Create the popularity over time chart
    popularity_chart = alt.Chart(name_rank_data).mark_line(point=alt.OverlayMarkDef(color='orange'), color='orange').encode(
        x=alt.X('annais:O', title='Year', axis=alt.Axis(format='d')),
        y=alt.Y('rank:Q', title='Rank', scale=alt.Scale(
            domain=(0, name_rank_data['rank'].max() + 1))),
        tooltip=['annais', 'rank']
    ).properties(
        title=f'Popularity of {name_selected} over time',
        width=600,
        height=400
    )

    popularity_text = popularity_chart.mark_text(
        align='left',
        baseline='middle',
        dx=5, dy=-5,
        color='white'
    ).encode(
        text='rank:Q'
    )

    popularity_combined_chart = (popularity_chart + popularity_text).properties(
        title=f'Popularity of {name_selected} over time'
    )

    # Display the charts side by side in Streamlit
    with col1:
        st.altair_chart(top_combined_chart.configure_title(
            fontSize=24, anchor='start'), use_container_width=True)
        st.altair_chart(least_combined_chart.configure_title(
            fontSize=24, anchor='start'), use_container_width=True)
    with col2:
        st.altair_chart(popularity_combined_chart.configure_title(
            fontSize=24, anchor='start'), use_container_width=True)

else:
    st.write("No data available for the selected year range.")
