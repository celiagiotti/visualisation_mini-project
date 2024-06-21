# Baby Names Mini Project - Visualisation IGR204

This is the repository for the "Baby Names" mini project.

**Members of the project group:**  
- Laurent GAYRAUD (MS Big Data)
- Alban PEREIRA (MS Big Data)
- Guillaume PIOL (MS Big Data)
- Célia GIOTTI (MS Big Data)

To do this project, we used Python and coded our visualisations with Altair (https://altair-viz.github.io). Then, to create a more ergonomic and attractive user interface, we used Streamlit (https://streamlit.io). 

**In this repository you will find several files of code:**
- visualisation_1.py
- visualisation_2.py
- visualisation_3.py

This 3 files contain all the code for all the visualisations required for the project.

**You have other files which are data files:**
- departements-avec-outre-mer.geojson
- departements-version-simplifiee.geojson
- dpt2020.csv

To view the various visualisations, you will need to create an environment that allows you to run the python scripts from your terminal. Once you have done this, your terminal will issue a command to launch the visualisation interface via Streamlit and open a web page so that you can play with the visualisations.

**Here are the different steps:**  
- Recover the entire Git repository
- Install all the necessary libraries in a specific environment using requirements.txt
- Run in the terminal **"python3 visualisation_1.py" or "python3 visualisation_2.py" or "python3 visualisation_3.py"**
- A command message will be sent to the terminal for viewing with Streamlit, so run in the terminal: **"streamlit run visualisation_1.py" or "streamlit run visualisation_2.py" or "streamlit run visualisation_3.py"** (A web page with the graphs will open: then it's your turn to play!)
- 
**Important (especially for visualisation 1):**
- To get the best possible view when you're viewing with Streamlit, when you're on the page in the top right-hand corner you'll see 3 little points, click on them and then click on **"Settings"**. A small page will open and in the **"Appearance"** section click on **"Wide mode"**. This will allow you to see all the graphics correctly.
If you automatically have a white background, remember to select **"Dark"** in the **"Choose app theme, colors and fonts"** section. We've programmed the text to be white, so it will look better with a black background. 
Here's a screenshot to help you:
<img width="236" alt="Capture d’écran 2024-06-21 à 10 53 50" src="https://github.com/celiagiotti/visualisation_mini-project/assets/144688454/05636e5a-e5fa-4411-af24-7cb8968b4b6e">


**Just to remind you, here are the objectives and guidelines for the mini-projects:** 

In this mini-project, we will be working with a data set of baby names in France. It contains the list of all baby names registered in France, year by year, from 1900 through 2020. There are two data sets: one aggregated to the national level, and another with data by department. Your goal is to create 3 different visualizations around these data, each focussed on answering different kinds of questions about the data:

- **Visualization 1:** How do baby names evolve over time? Are there names that have consistently remained popular or unpopular? Are there some that have were suddenly or briefly popular or unpopular? Are there trends in time?
- **Visualization 2:** Is there a regional effect in the data? Are some names more popular in some regions? Are popular names generally popular across the whole country?
- **Visualization 3:** Are there gender effects in the data? Does popularity of names given to both sexes evolve consistently? (Note: this data set treats sex as binary; this is a simplification that carries into this assignment but does not generally hold.)

This assignment consists of several parts: in the first part, you will sketch design alternatives for different visualizations that can help address each set of questions. In the second part, you will implement that visualization using one of the tools from the class lab assignments. In the third part, you will refine these solutions.



