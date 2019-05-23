# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from osgeo import ogr, osr, gdal
import numpy as np
from math import ceil, floor
from psycopg2 import connect as psycopg2_connect

def create_isobands(input_file, output_file):

    raster = gdal.Open(input_file)

    rast_array = raster.ReadAsArray()

    rast_array[rast_array==-99999] = np.nan

    x_size = raster.RasterXSize
    y_size = raster.RasterYSize

    geotransform = raster.GetGeoTransform()

    srs = osr.SpatialReference()
    srs.ImportFromWkt(raster.GetProjectionRef())  

    x_array = np.fromiter(((geotransform[0] + geotransform[1]/2) + x*geotransform[1] for x in range(x_size)), np.float32, x_size)
    y_array = np.fromiter(((geotransform[3] +geotransform[5]/2) + y*geotransform[5] for y in range(y_size)), np.float32, y_size)
    x_grid, y_grid = np.meshgrid(x_array, y_array)


    min_level = np.nanmin(rast_array)
    max_level = np.nanmax(rast_array)

    levels = [x for x in range(floor(min_level), ceil(max_level)+1)]
    print(levels)


    contours = plt.contourf(x_grid, y_grid, rast_array, levels)


    #Creating the output vectorial file
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource(output_file)
    layer = data_source.CreateLayer("Contour", srs, ogr.wkbPolygon)

    field_name_level = 'level'
    attribute = ogr.FieldDefn(field_name_level, ogr.OFTReal) 
    layer.CreateField(attribute)

    
    i = 1
    for level in range(len(contours.collections)):
        paths = contours.collections[level].get_paths()
        
        for path in paths:
            
            feat_out = ogr.Feature(layer.GetLayerDefn())
            
            feat_out.SetField(field_name_level, contours.levels[level])
            
            pol = ogr.Geometry(ogr.wkbPolygon)


            ring = None            
            
            for i in range(len(path.vertices)):
                point = path.vertices[i]
                if path.codes[i] == 1:
                    if ring != None:
                        pol.AddGeometry(ring)
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    
                ring.AddPoint_2D(point[0], point[1])
            

            pol.AddGeometry(ring)
            
            feat_out.SetGeometry(pol)
            if layer.CreateFeature(feat_out) != 0:
                print("Failed to create feature in shapefile.\n")
                exit( 1 )
            
            i += 1
            
            feat_out.Destroy()
        
    data_source.Destroy()

if __name__ == '__main__':
    create_isobands(r'C:\Temp\klar\result_mut_without_stream_suppot\gwpot_mut.sdat', 
                    r'C:\Temp\test.shp')
