# Lab Project
 Living Suitability Analysis
 Introduction: 
The living suitability analysis toolbox helps you analyze and detect areas of a city which are best to live in. The toolbox is created in the ArcMAP from the script lets you input specific features/ places of interest in a city and the output would be buffered polygons around the data that you specified as input and are overlaid on the map of the city of your interest. These buffered polygons are based on the distances specified in the script in linear units in this case Kilometers. 
Data: 
-	Point features for supermarkets, airports and hospitals (nationwide) will be referred to as commercial data 
-	Line features for the state highways which are nationwide
-	Polygon features for the boundary of the cities 

The input that were used for this analysis pertain to the 4 New Zealand cities that were chosen for the analysis. 
For this script you would need to follow a specific naming convention for the folders where the data for each city is saved. Each city would have the above listed feature ‘shapefiles’ as a .shp format and they would have to have a same name which would be inside the cities sub-folder so that the underlying script that runs the tool can recognise them. 
Note :  all the input features should be in a folder and not the geodatabase, geoprocessing tools 
Toolbox:
	 

The user will specify a folder in which their output will be saved. This can be any folder they wish to save their output to but the script is program is set up in a way that it go will go and add it to the end of the sub-folder list in whatever folder you are saving it in.
Another parameter is the workspace environment to run the tool - a geodatabse which a user will have to specify in the ArcMAP. If not already present, you will have to create a file geodatabase in the same folder where your folder for all the cities are. 
NOTE: the user will need to define a template and have an ArcMAP document with the basemap for that specific city to be able to see the 
How the toolbox runs – as specified in the underlying script the it runs the geoprocessing function on the input data (shapefiles), it clips those commercial input features to the city bounds of each city and creates a buffer around them with the distances that are specified in the program. These buffers that are created are in the form of polygons. These buffered polygons are transferred into rasters and are added together to get the final raster output will have values ranging from Low to High from which the user will be able to determine the best places to live in the city (as shown in the figure below).
After creating the suitability rasters, they will be saved as a pdf with the template map document that the user will create for a particular city. In this case 4 cities were used namely Auckland, Christchurch, Dunedin and Wellington and their commercial data as inputs analyse where in these cities were the best areas to live.

Parameters:
	Examples of input and output parameters of the tool are explained below-
For the clip analysis geoprocessing tool, 
Parameter	Parameter name	Explanation	Data type
in_features	supermarkets.shp	Feature to be clipped	Feature layer
clip_features	citybound.shp	Feature used to clip input feature	Feature layer
out_feature_class	supermarkets_Clip.shp	Feature to be created	Feature class

For the buffer analysis geoprocessing tool,
Parameter	Parameter name	Explanation	Data Type
in_features	supermarkets_Clip	The input point, line, or polygon features to be buffered.	Feature Layer
out_feature_class	supermarkets_buffer	The feature class containing the output buffers.	Feature Class
buffer_distance_or_field	[0.5, 5]	The distance around the input features that will be buffered. Distances can be provided as either a value representing a linear distance or as a field from the input features that contains the distance to buffer each feature.
If linear units are not specified the linear unit of the input features' spatial reference is used.	Linear Unit; Field
line_side	FULL	For point input features buffers will be generated around the point.	String
dissolve_option	ALL	All buffers are dissolved together into a single feature removing any overlap	String





Output:
The final output would look like the one below, with exported output of the map as specified by the user in the template map document. 







Limitations and further possibility of development:
	The developed script has a few limitations which are in a way hard coded in the script or simply put cannot be changed by the user. These limitations are the buffer distances, specified in the program code and are based on the distances in the context of cities in New Zealand. For further extension, there is a possibility of extending the script with user specified buffer distances. The function of calculation of time taken to travel out of a certain buffer distance could also be added. There is also possibility of extending the number of cities data you can input by user specification. 
