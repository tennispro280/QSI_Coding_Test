# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 09:11:00 2020

@author: Cole
"""
import pandas as pd 
import os 
from geopandas import GeoDataFrame as gdf
from shapely.geometry import Point


#inout variables

building_csv = r"C:\QSI_Coding_Test\Data\buildings.csv"         #input buildings file path
queries_csv = r"C:\QSI_Coding_Test\Data\queries.csv"            #input queries file path
epsg = 2913                                                     #input epsg ~~ https://www.spatialreference.org/ref/?search=Oregon
outpath = r'C:\QSI_Coding_Test\Data'                            #Data folder/output file location for analyis

def csv_query_dist(building_csv,queries_csv,epsg,outpath):                                                    
    """ This module will take in a building csv and queries csv that have X and Y values as headers
        {Accepts Caps only}. It will convert these into spatial data points applying a CRS that 
        is assigned by the input epsg code. For each location in the queries data it will return 
        the associated building that is the minimum distance from the query location in the form
        of an output csv."""    
#Generate building gdf
    
    File_Name = building_csv                                                            #calls on the queris csv set this to a input variable 
    bdf = pd.read_csv(                                                                  #create data frame for buildings from csv assuming header at position 0 
        File_Name, delimiter=",", header=0 )
         
    geometry = [Point(xy) for xy in zip(bdf.X, bdf.Y)]                                  #assign the geomety to pull from the X and Y columns (As set only works on CAP field names, change to accept both)
    crs = {'init':"{0}{1}".format(('epsg:'),epsg)}                                                               #assign the spatial reference using epsg codes ##https://spatialreference.org/ref/epsg/wgs-84-utm-zone-10n/
    b_gdf = gdf(                                                                        #create geodataframe of building locations
            bdf, crs=crs, geometry=geometry)
    
    b_gdf = b_gdf.rename(columns={'geometry': 'buildings'}).set_geometry('buildings')   #rename the geometry colum to queries
    TC = len(bdf.axes[0])                                                                #z is assigned the total number of n buildings (used later)
    print(crs)
#Generate Queries gdf
    
    File_Name = queries_csv                                                         #calls on the queris csv set this to a input variable 
    df = pd.read_csv(
        File_Name, delimiter=",", header=0 )                                        #create data frame for queries from csv assuming header at position 0
              
    geometry = [Point(xy) for xy in zip(df.X, df.Y)]                                #assign the geomety to pull from the X and Y columns (As set only works on CAP field names, change to accept both)
    crs = {'init':"{0}{1}".format(('epsg:'),epsg)}                                                           #assign the spatial reference using epsg codes #https://spatialreference.org/ref/epsg/wgs-84-utm-zone-10n/
    q_gdf = gdf(                                                                    #create geodataframe of query locations
            df, crs=crs, geometry=geometry)
    
    q_gdf = q_gdf.rename(columns={'geometry': 'queries'}).set_geometry('queries')   #Rename the geometry column to queries

#Build list to used for future compilation
    Q = []                                                                          #List of query names
    B = []                                                                          #List of building names
    D = []                                                                          #List of distance to elements

#Generate distance from Query to building
    
    for index,row in q_gdf.iterrows():                                              #iterate through query gdf using index position: allows for a point feature of queris to be created iterativley and appllied in nested loop 
        Q.append(row.Name)                                                          #appened Query name to list each iteration                                                               
        point = row.queries                                                         # create the query point feature to apply to nested loop
        for index,row in b_gdf.iterrows():                                          #iterate through buildings gdf using index position 
            dist = point.distance(row.buildings)                                    # calculate the distance from the point(query-point) feature to the point feature n-building

            B.append(row.Name)                                                      #append the associated building at given index position 
            D.append(dist)                                                          #Calculate the distance from n-query to each n-building; append to list 
                      
    BD = pd.DataFrame(list(zip(B,D)),columns =['Building','Distance'])              #create df that zips the building and distance together: gives distance for (0:n) Buildings for each item in the query. total = #query items * #building items
    
#Build list of minimum distant elements
    
    min_dist= []
    h = len(BD.axes[0])                                                             #Calls the total length of building elements being asses (n elements * query elements = h )
    n=0                                                                             #set the query range to 0 to allow iteration 
    
    while n < h:
            f = n+(TC)                                                              #TC = count of total buildings allowing to index output results
            select = BD.iloc[n:f,]                                                  #calls a series of elemets identified by range n+TC
            n = f                                                                   #reassign n so it starts at the new index range in the loop
    
            select_min = select.loc[select['Distance'].idxmin()]                    #returns the minimum 'Distance' and 'Building' as series object
            min_dist.append(select_min)                                             #append the min per query index to a series list                         

#finalise and combine the final reuslts into dataframe

    QF = pd.DataFrame(Q,columns=['Query'])                                          #create df with Query locations only
    DF = pd.DataFrame(min_dist,columns= ['Building','Distance'])                    #Create df with Buildings and Distannces
    DF = DF.reset_index(drop = True)                                                #reset index to start at 0 to n elements
    
    results = pd.concat([DF,QF], axis= 1, sort = False)                             #Join the query locations with buildings and distance off of the index position
         
#Save out the results to designated path tagged as Distance_Results
    
    out_file = ("{0}{1}".format(outpath,'\Distance_Results'))                       #creat the output file format
    results.to_csv(out_file, index = True)                                          #save out the results to a csv

if __name__ == "__main__":
    os.chdir(outpath)
    csv_query_dist(building_csv,queries_csv,epsg,outpath)
    



















