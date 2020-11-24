#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 11:38:44 2020

@author: katsi578 
"""

# import modules
import arcpy
import os
from arcpy.sa import*

# general parameters
masterfolder = r"U:\ThirdYear\SURV319\tutorials\Lab3\cities" #arcpy.GetParameterAsText(0)
geodatabase = arcpy.GetParameterAsText(1)

#environment settings
arcpy.CheckOutExtension = ("spatial")
arcpy.env.workspace = geodatabase
arcpy.env.overwriteOutput = True

   
# Main Geoprocessing function that inlcudes clipping buffering converting polygons to rasters 
# for all the different shapefiles, and adding all these rasters together to create a final
#  raster showing the best places to live each of the 4 different cities"""

def geoprocessing(currentcity):
    
    # defining local variables for the geoprocessing function
    
    statehighway_Clip = 'statehighway_clip'
    supermarkets_Clip = 'supermarkets_clip'
    airports_Clip = 'airports_clip'
    hospitals_Clip = 'hospitals_clip'
    statehighway_buffer = 'statehighway_buffer'
    supermarkets_buffer = 'supermarkets_buffer'
    airports_buffer = 'airports_buffer'
    hospitals_buffer = 'hospitals_buffer'
    statehighway_raster = 'statehighway_raster'
    supermarkets_raster = 'supermarkets_raster'
    airports_raster = 'airports_raster'
    hospitals_raster = 'hospitals_raster'
    cellsize = 10
    
# Editing and cleaning up of the geoprocessing function

# the first variable is the state highgway - best place to live needs to be far from a highway but not too far
# this funstion clips the nationwide shapefile according to the city's citybound shapefile , same process was done
# for the 3 remaining variables - supermarkets, airports and hospitals

  
    #clip state highways to city boundary
    arcpy.AddMessage("For " + city + " clip state highway")
    arcpy.Clip_analysis(statehighway, citybound, statehighway_Clip, "")
    
# thw clipped statehighway was then buffered to the distance of 0.5 to 10 kilometers and same was done 
# to the clipped shapefiles of other variables 
# supermarkets had buffered distances of 0.5 to 5 kilometers
# airports had buffered distances of 3 to 30 kilometers
# hospitals had buffered distances of 0.5 to 5 kilometers
    
    #buffer the clipped state highway
    arcpy.AddMessage("For " + city + " buffer state highway")
    arcpy.MultipleRingBuffer_analysis(statehighway_Clip, statehighway_buffer, [0.5, 10], "Kilometers", "", "ALL", "FULL")
    
    #clip supermarkets to city boundary
    arcpy.AddMessage("For " + city + " clip supermarkets ")
    arcpy.Clip_analysis(supermarkets, citybound, supermarkets_Clip, "")
    
    #buffer the clipped supermarkets
    arcpy.AddMessage("For " + city + " buffer supermarkets")
    arcpy.MultipleRingBuffer_analysis(supermarkets_Clip, supermarkets_buffer, [0.5, 5], "Kilometers", "", "ALL", "FULL")
    
     #clip airports to city boundary
    arcpy.AddMessage("For " + city + " clip airports")
    arcpy.Clip_analysis(airports, citybound, airports_Clip, "")
    
    #buffer the clipped airports
    arcpy.AddMessage("For " + city + " buffer airports")
    arcpy.MultipleRingBuffer_analysis(airports_Clip, airports_buffer, [3, 30], "Kilometers", "", "ALL", "FULL")
    
     #clip hospitals to city boundary
    arcpy.AddMessage("For " + city + " clip hospitals")
    arcpy.Clip_analysis(hospitals, citybound, hospitals_Clip, "")
    
    #buffer the clipped hospitals
    arcpy.AddMessage("For " + city + " buffer hospitals")
    arcpy.MultipleRingBuffer_analysis(hospitals_Clip, hospitals_buffer, [0.5, 5], "Kilometers", "", "ALL", "FULL")
    
# takes the vector shapefiles created by the the clip and multiring buffer and converts them into a raster
    
    arcpy.AddMessage("Convert " + city + " buffered shapefiles to raster")
    arcpy.PolygonToRaster_conversion(statehighway_buffer, "distance", statehighway_raster, "CELL_CENTER", "NONE", cellsize)
    arcpy.PolygonToRaster_conversion(supermarkets_buffer, "distance", supermarkets_raster, "CELL_CENTER", "NONE", cellsize)
    arcpy.PolygonToRaster_conversion(airports_buffer, "distance", airports_raster, "CELL_CENTER", "NONE", cellsize)
    arcpy.PolygonToRaster_conversion(hospitals_buffer, "distance", hospitals_raster, "CELL_CENTER", "NONE", cellsize)
    
# different rasters that were created were then multiplied together to obtain a final raster 
#  that combines all the previous conditions together
#  teh funstion used here is the Times function that multiplies the rasters together
    # raster calculator
    arcpy.AddMessage("Combine all rasters")
    
    raster_calc1 = Times(supermarkets_raster, hospitals_raster)
    raster_calc2 = Times(statehighway_raster, airports_raster)
    raster_calc3 = Times(raster_calc1, raster_calc2 )

# mxd funstions defines a map document , df function defines data frame
# arcpy.makerasterlayermanagement() tells arcmap to identify the raster file and identify its transparency
# we then add the layer to the map and then and set map extent using df.extent
    
    #add raster to the map
    arcpy.AddMessage("Add final raster to the Map")
    mxd = arcpy.mapping.MapDocument('CURRENT')
    df = arcpy.mapping.ListDataFrames(mxd, 'Layers')[0]
    arcpy.MakeRasterLayer_management(raster_calc3, 'Site raster')
    final_raster = arcpy.mapping.Layer('Site Raster')
    final_raster.transparency = 50;
    arcpy.mapping.AddLayer(df, final_raster, 'TOP')
    
    #set map extent
    df.extent = final_raster.getExtent()

# funvtion to write pdf per each city run as part of the loop and reset for next 
def writepdf(currentcity):
    
    global city
    
    pdfPath = masterfolder + "\\zAtlas" + "\\CityAtlas.pdf"
    
    try:
        os.remove(pdfPath)
    except:
        arcpy.AddMessage("Didn't delete City Atlas!")
        pass
    
    mxd = arcpy.mapping.MapDocument("current")
    
    try:
        os.close(pdfPath)
    except:
        pass
    
    #checks for previous city file and deletes any existing
    arcpy.AddMessage("delete existing pdf")
    pdfcity = str(masterfolder + "\\zAtlas\\" +  city + ".pdf") 
    if os.path.exists(pdfcity):
        os.remove(pdfcity)
    
    #complete map with pecific data
    arcpy.AddMessage("Title and Page Number")
    for elem in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elem.text == "<FNT size='18'>TITLE</FNT>":
            elem.text == "<FNT size='18'>" + "Best areas to live in" + str(currentcity) + "</FNT>"
        if elem.text == "<FNT size='12'>Page" + str(i + 1) + "of 4</FNT>":
            elem.text == "<FNT size='12'>PAGE</FNT>"
    arcpy.RefreshActiveView()
    
    #Export map to pdf
    arcpy.AddMessage("Export map to PDF")
    arcpy.mapping.ExportToPDF(mxd, pdfcity)
    
    #resets text elements for next map
    arcpy.AddMessage("Title and Page Number")
    for elem in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elem.text == "<FNT size='18'>" + "Best areas to live in" + str(currentcity) + "</FNT>":
            elem.text == "<FNT size='18'>TITLE</FNT>"
        if elem.text == "<FNT size='12'>Page" + str(i + 1) + "of 4</FNT>":
            elem.text == "<FNT size='12'>PAGE</FNT>"
    arcpy.RefreshActiveView()
    
    

def CreateAtlas(folder):
    #define workspace and assign pdf_folder as a function of the master folder
    pdf_folder = folder + "\\zAtlas"
    arcpy.env.workspace = pdf_folder
    pdf_list = arcpy.ListFiles("*.pdf")
    arcpy.AddMessage(pdf_list)
    #defines path for final atlas
    pdfPath = folder + "\\CityAtlas.pdf"
    if os.path.exists(pdfPath):
        os.remove(pdfPath)
    pdfDoc = arcpy.mapping.PDFDocumentCreate(pdfPath)
    
    
    for i in range(0, 3):
        file=pdf_list[i]
        pdfDoc.appendPages(pdf_folder + "\\" + file )
        
# this part of the code sets loop for the code to effectively go through each folder (individual city) in the masterfolder
#  and run analysis for each
citiesfolder = os.listdir(masterfolder)
#set up code to loop through all cities
for i in range(0, 3):
    city = citiesfolder[i]
    print (city)
    arcpy.AddMessage(city)
    citybound = masterfolder + "\\" + city + "\\cityboundary" + "\\citybound.shp"
    statehighway = masterfolder + "\\" + city + "\\statehighway" + "\\statehighway.shp"
    supermarkets = masterfolder + "\\" + city + "\\supermarkets" + "\\supermarkets.shp"
    airports = masterfolder + "\\" + city + "\\airports" + "\\airports.shp"
    hospitals = masterfolder + "\\" + city + "\\hospital" + "\\hospitals.shp"
    
    
    #run functions
    geoprocessing(city)
    writepdf(city)
    
    
#runs CreateAtlas at the end of the script after all pdfs have been created
CreateAtlas(masterfolder)        