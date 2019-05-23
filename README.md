# Introduction 
This is repository contains a proof of concept and feasibility of using Jupiter data and IoT sensors data to create an
interpolation of the groundwater level in a given area using the natural nearest neighbour algorithm from SAGA GIS.
The idea is to auto-generate the interpolation by using the scrips.

# [Wiki](/Wiki)

# Getting Started
1. Anaconda3.6.5 (Anaconda Distribution) or higher (Python 3.7.x) from https://www.anaconda.com/distribution/
2. Create virtual environment: https://salishsea-meopar-docs.readthedocs.io/en/latest/work_env/python3_conda_environment.html
3. Activate the environment 
4. Install Anaconda packages:
	* conda install numpy pandas scikit-learn matplotlib
	* conda install -c anaconda psycopg2
	* conda install -c conda-forge gdal
	* conda install -c conda-forge pandas
	* conda install -c conda-forge psycopg2
	* conda install -c anaconda numpy 
	* conda install -c conda-forge matplotlib
	* conda install -c conda-forge fiona 
5. Install Python packages
	* pip install psycopg2
	* pip install GDAL
	* pip install Shapely
6. Install SAGA GIS 6.3.0 - https://sourceforge.net/projects/saga-gis/files/SAGA%20-%206/SAGA%20-%206.3.0/saga-6.3.0_x64_setup.exe/download
7. Install PostgreSQL 9.5 or 10 if running locally some of the databases
8. Install PGAdmin 4 as client more then welcome to use the command line as well
9. Make a secret.py with default hardcoded values:
	* gues_url =  '<Value>'
	* gues_database = '<Value>'
	* gues_port = <Value>
	* gues_username = '<Value>'
	* gues_password = '<Value>'
	* customer_url =  '<Value>'
	* customer_database = '<Value>'
	* customer_port = <Value>
	* customer_username = '<Value>'
	* customer_password = '<Value>'
10. Create a postgis terrain database
11. Create a database groundwater_geus and import jupiter data
12. Create a database groundwater_level with views, tables from wiki and insert necessary data 
13. Run create_GW_Pot_interpolation.py

## Data sources
* coast lines data from https://kortforsyningen.dk
* elevation data from https://kortforsyningen.dk
* streams data from Orbicon internally refined by other department based on https://kortforsyningen.dk 
* jupiter data  https://www.geus.dk/produkter-ydelser-og-faciliteter/data-og-kort/national-boringsdatabase-jupiter/
* SensorHub database - proprietary database schema from Orbicon SensorHub solution. Can be replaced with your sensor database 
using PostGIS database 
## Data import from data sources
* Streams imported via QGIS 3.6+
* Coast imported via QGIS 3.6+
* jupiter recreated from dump - http://gerda.geus.dk/Gerda/exportfiles/?filename=pcjupiterxlpluspg_xl.zip
* elevation data was downloaded a long time ago and imported. Data is about 2.3+TB
* SensorHub database - proprietary database schema from Orbicon SensorHub solution. Can be replaced with your sensor database 
using PostGIS database 
## Filters on the data
* Depth of intake < 7m under terrain elevation
* Avoid duplication of boreholes (example when duplication occurs: join with intake)
* Negative or missing elevation join with terrain database to validate the data
* Add data validation 
* Pump situation - ro or unknown
* Date of sample always take the newest

# Contact infortmation
[link](https://www.orbiconinformatik.dk/)
