# Coding_Boyer
This repository is to server as an example of work created on June 4, 2020.

## Building Distance to Query
This program is designed to identify the building from a list of buildings that maintains the minimum distance to each unique item in a list of query locations. It is written in python 3.7. 

## Inputs Parameters
**building.csv**
  * This is a csv file that contains location data for buildings. Currently the program will run if the input csv maintains X and Y headers in capital letter only.  
  
**querys.csv**
  * This is a csv file that contains location data for query locations. Currently the program will run if the input csv maintains X and Y headers in capital letters only.

**epsg Code**
  * This is the assigned CRS using the [epsg](https://www.spatialreference.org/ref/?search=Oregon) CRS system derived for location. 

**Output File Location**
  * Select a output file location. This will be where the reults of the program are written to. 
  
## Outputs
The results will be written to the designated output folder and titled Distance_Results.csv. The output csv contains:
  * Header[Index,Building,Distance,Query]
 
 The Distance_Results.csv contain the name of the **Building** at the identified **Distance** to the **Query** location.

## Running + Installation
Open the QSI_Coding_Test_Boyer.py file in any Python 3 IDE of choice. Insure that you have the needed dependencies installed listed bellow. Change the inputs and output to meet your requirements and program documentation. Exectue. 

### Dependencies
*pandas* 

*geopandas -> GeoDataFrame*

*shapely.geometry -> Point*

### Future Work
I gave a go at wrapping the program in a GUI/UI using QT5. Ran out of time to fully package it with a nice UI. I have attached this python program in addition to the compleated program within this repository for reference labeled UI Wrapping. 
