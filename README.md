# ENSF-592-Project
This project involved:

1. Data Preparation

  - Cleaning
  
  - Merging
  
2. Data Aggregation

  - Analysing a specific group of data
  
3. Visualization

The goal of the project is to find the features that can affect the number of accident in Calgary City.
All data provided is based on https://data.calgary.ca/browse.

Focused features:

1. Road Features
  
  1.1. Road Speed
  
    - https://data.calgary.ca/Health-and-Safety/Speed-Limits-Map/rbfp-3tic
    
  1.2. Average Traffic Volume
  
    - 2018 (Traffic_Volumes_for_2018.csv)
    
  1.3. Road Signals
  
    - Traffic Signals (Traffic_Signals.csv)
    
    - Traffic Signs (Traffic_Signs.csv)
    
    - Traffic cameras (Traffic_Camera_Locations.csv)
    
2. Weather Features

  - Temperature
  
  - Visibility
  
For each grid in Calgary map, following features are calculated for year 2018:

● Average speed limit

● Average Traffic volume

● Average number of traffic cameras

● Number of Traffic Signals

● Number of Traffic Signs

● Daily Weather Condition

  - Temperature
  
  - Visibility
  
● Target: Average number of Traffic accidents

● Analyse the data and interpret the relation between the number of accidents and the above feature in 2018.

Different techniques used for visualizing data using python are histogram, scatter plot, line graph, heatmap.
