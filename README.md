# Baby Names Mini Project - Visualisation IGR204

This is the repository for the "Baby Names" mini project.

**Members of the project group:**  
- Laurent GAYRAUD (MS Big Data)
- Alban PEREIRA (MS Big Data)
- Guillaume PIOL (MS Big Data)
- Célia GIOTTI (MS Big Data)

To do this project, we used Python and coded our visualisations with Altair (https://altair-viz.github.io). Then, to create a more ergonomic and attractive user interface, we used Streamlit (https://streamlit.io). 

**In this repository you will find several files of code, the last version of the project with our refined solution is in this files:**
- visualisation_1_final.py
- visualisation_2_final.py
- visualisation_3_final.py

This 3 files contain all the code for all the visualisations required for the project.

**You also have the first version of the project in this files:**
- visualisation_1.py
- visualisation_2.py
- visualisation_3.py

**You have a folder named "data" with different files which are data files:**
- departements-avec-outre-mer.geojson
- departements-version-simplifiee.geojson
- departements-region.csv
- dpt2020.csv

To view the various visualisations, you will need to create an environment that allows you to run the python scripts from your terminal. Once you have done this, your terminal will issue a command to launch the visualisation interface via Streamlit and open a web page so that you can play with the visualisations.

**Here are the different steps:**  
- Recover the entire Git repository
- Install all the necessary libraries in a specific environment using requirements.txt
- Run in the terminal **"python3 visualisation_1_final.py" or "python3 visualisation_2_final.py" or "python3 visualisation_3_final.py"**
- A command message will be sent to the terminal for viewing with Streamlit, so run in the terminal: **"streamlit run visualisation_1_final.py" or "streamlit run visualisation_2_final.py" or "streamlit run visualisation_3_final.py"** (A web page with the graphs will open: then it's your turn to play!)


**Just to remind you, here are the objectives and guidelines for the mini-projects:** 

In this mini-project, we will be working with a data set of baby names in France. It contains the list of all baby names registered in France, year by year, from 1900 through 2020. There are two data sets: one aggregated to the national level, and another with data by department. Your goal is to create 3 different visualizations around these data, each focussed on answering different kinds of questions about the data:

- **Visualization 1:** How do baby names evolve over time? Are there names that have consistently remained popular or unpopular? Are there some that have were suddenly or briefly popular or unpopular? Are there trends in time?
- **Visualization 2:** Is there a regional effect in the data? Are some names more popular in some regions? Are popular names generally popular across the whole country?
- **Visualization 3:** Are there gender effects in the data? Does popularity of names given to both sexes evolve consistently? (Note: this data set treats sex as binary; this is a simplification that carries into this assignment but does not generally hold.)

This assignment consists of several parts: in the first part, you will sketch design alternatives for different visualizations that can help address each set of questions. In the second part, you will implement that visualization using one of the tools from the class lab assignments. In the third part, you will refine these solutions.



