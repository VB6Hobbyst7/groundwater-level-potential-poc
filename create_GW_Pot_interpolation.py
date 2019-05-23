# -*- coding: utf-8 -*-
# Secrets
import secrets as secs

# Plotting dependencies
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from create_isobands import create_isobands

# Dataframe dependencies
import pandas as pd

# Numerical calc dependencies
import numpy as np

# ODBC dependencies
from psycopg2 import connect as psycopg2_connect

# Geospatial dependencies
from osgeo import ogr, osr, gdal
from subprocess import call
import os

from create_alpha_shape import (create_point_set, alpha_shape, sortList, create_wkt)


class jupiterAnalyser(object):

    def __init__(self, **kwargs):
        self.__params = {}
        accepted_params = ['cust_host', 'cust_dbname', 'cust_user', 'cust_password', 'cust_port',
                           'geus_host', 'geus_dbname', 'geus_user', 'geus_password', 'geus_port', ]

        if len(kwargs.items()) == 0:
            raise ValueError("No input parameters given - Viable input parameters are: {}".format(accepted_params))

        else:
            for param_name, param_value in kwargs.items():

                if param_name in accepted_params:
                    self.set_property_from_item(param_name, param_value, accepted_params)

    def set_property_from_item(self, paramName, paramValue, accepted_param):
        if paramName in accepted_param:
            setattr(self, paramName, paramValue)
        else:
            raise ValueError("Recieved unknown parameter {}".format(paramName))

    """

    Getter/Setter for customer setup

    """

    @property
    def cust_host(self):
        return self.__params["cust_host"]

    @cust_host.setter
    def cust_host(self, cust_host):

        if type(cust_host) != str:
            raise ValueError("Input is not a string")

        self.__params["cust_host"] = cust_host

    @property
    def cust_dbname(self):
        return self.__params["cust_dbname"]

    @cust_dbname.setter
    def cust_dbname(self, cust_dbname):

        if type(cust_dbname) != str:
            raise ValueError("Input is not a string")

        self.__params["cust_dbname"] = cust_dbname

    @property
    def cust_user(self):
        return self.__params["cust_user"]

    @cust_user.setter
    def cust_user(self, cust_user):

        if type(cust_user) != str:
            raise ValueError("Input is not a string")

        self.__params["cust_user"] = cust_user

    @property
    def cust_password(self):
        return self.__params["cust_password"]

    @cust_password.setter
    def cust_password(self, cust_password):

        if type(cust_password) != str:
            raise ValueError("Input is not a string")

        self.__params["cust_password"] = cust_password

    @property
    def cust_port(self):
        return self.__params["cust_port"]

    @cust_port.setter
    def cust_port(self, cust_port):

        if type(cust_port) != int:
            raise ValueError("Input is not an integer")

        self.__params["cust_port"] = cust_port

    """

    Getter/Setter for GEUS setup

    """

    @property
    def geus_host(self):
        return self.__params["geus_host"]

    @geus_host.setter
    def geus_host(self, geus_host):

        if type(geus_host) != str:
            raise ValueError("Input is not a string")

        self.__params["geus_host"] = geus_host

    @property
    def geus_dbname(self):
        return self.__params["geus_dbname"]

    @geus_dbname.setter
    def geus_dbname(self, geus_dbname):

        if type(geus_dbname) != str:
            raise ValueError("Input is not a string")

        self.__params["geus_dbname"] = geus_dbname

    @property
    def geus_user(self):
        return self.__params["geus_user"]

    @geus_user.setter
    def geus_user(self, geus_user):

        if type(geus_user) != str:
            raise ValueError("Input is not a string")

        self.__params["geus_user"] = geus_user

    @property
    def geus_password(self):
        return self.__params["geus_password"]

    @geus_password.setter
    def geus_password(self, geus_password):

        if type(geus_password) != str:
            raise ValueError("Input is not a string")

        self.__params["geus_password"] = geus_password

    @property
    def geus_port(self):
        return self.__params["geus_port"]

    @geus_port.setter
    def geus_port(self, geus_port):

        if type(geus_port) != int:
            raise ValueError("Input is not an integer")

        self.__params["geus_port"] = geus_port

    def listFiles(self, directory, extension):
        full_directory_for_files = []

        file_names = []

        for name in os.listdir(directory):

            if name.endswith(extension):
                full_directory = os.path.join(directory, name)
                full_directory_for_files.append(full_directory)
                file_names.append(name)

        return (full_directory_for_files, file_names)

    def connectToPsycopg2Database(self, host, dbname, user, password, port):
        return psycopg2_connect(
            "host='{0}' dbname='{1}' user='{2}' password='{3}' port='{4}'".format(host, dbname, user, password, port))

    def runQuery(self, sql, host, dbname, user, password, port):
        with self.connectToPsycopg2Database(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
            return pd.read_sql(sql, conn)

    def getDiscreteMeasurementsAndSensorsData(self, index_column, sql="""
        set search_path to gw_pot;

        select
                           thingid,
                           messageid,
                           observationid,
                           name,
                           property,
                           value as avg_wl_watlevgrsu,
                           unitofmeasure,
                           time,
                           networkname,
                           tenantid,
                           xutm,
                           yutm,
                           geom
           from gw_pot.v_theregionaldatahub_measurements_last_known_kbh;
        """):
        # WHERE ST_Intersects(l.geom, ST_MakeEnvelope({0}, {1}, {2}, {3}, {4} )"""):
        # sql = sql.format(cord1a, cord1b, cord2a, cord2b, srid)
        return self.runQuery(sql, self.cust_host, self.cust_dbname, self.cust_user, self.cust_password,
                             self.cust_port).set_index(index_column)

    #         (date_part('year', current_timestamp) - date_part('year', "timeofmeas")) < {0} and
    def getPgsqlBorholeMeta(self, index_column, screen_bottom, mask_wkt, srid, sql="""
        set search_path to pcjupiterxlplusviews, public;

        select 
        replace(borehole.boreholeno, ' ', '') as boreholeno,
        "drilldepth" as drilldepth_mut,
        "elevation" as elevation,
        case
        	when screen."bottom" is not null
        	then abs("zdvr90" - screen."bottom")
        	else abs("zdvr90" - "drilldepth")
        end as calc_bottom_kote,
        "ctrpeleva" as pof_elevation, 
        "ctrpdescr" as pof_description, 
        "ctrpheight" as pof_height, 
        "location" as location, 
        "comments" as comments,
        intake."intakeno" as intakeno,
        screen."top" as screen_top_mut,
        screen."bottom" as screen_bottom_mut,
        screen."diametermm" as screen_diametermm,
        min(watlevel."watlevgrsu") as mi_wl_watlevgrsu,
        max(watlevel."watlevgrsu") as max_wl_watlevgrsu,
        avg(watlevel."watlevgrsu") as avg_wl_watlevgrsu,
        avg(watlevel."watlevmsl") as avg_wl_mut,
        count(watlevel."watlevmsl") as count_waterlevel_dvr90,
        "drilendate" as drilendate, 
        "abandondat" as abandondat, 
        "xutm" as xutm, 
        "yutm" as yutm,
        "utmzone" as utmzone,
        "zdvr90" as zdvr90,
        geom
        from borehole 
        left outer join intake on borehole."boreholeno" = intake."boreholeno" 
        left outer join screen on intake."boreholeno" = screen."boreholeno" and intake."intakeno" = screen."intakeno" 
        left outer join watlevel on intake."boreholeno" = watlevel."boreholeno" and intake."intakeno" = watlevel."intakeno"
        where "xutm" is not null 
        and "yutm" is not null
        and screen."bottom" < {0}
        and st_intersects(geom, st_geomfromtext('{1}', {2}))
        group by
        borehole."boreholeno",
        "drilldepth", 
        "elevation", 
        "ctrpeleva", 
        "ctrpdescr", 
        "ctrpheight", 
        "location", 
        "comments",
        intake."intakeno",
        screen."top",
        screen."bottom",
        screen."diametermm",
        "drilendate", 
        "abandondat", 
        "xutm", 
        "yutm", 
        "utmzone",
        "zdvr90",
        geom
        having 
        count(watlevel."watlevgrsu") > 0;
        """):

        """
        Method for extracting meta information for the requested sensor.
        It is based on a default sql statement where the sensor_id is parsed into.
        This is run directly into Pandas for faster parsing.

        The function is called as a part of the extractSingularSensor() function.

        input:
            sql: SQL statement used to extract the data (a default is provided)

        output:
            A Pandas dataframe with the data from the sql request
        """

        sql = sql.format(screen_bottom, mask_wkt, srid)

        return self.runQuery(sql, self.geus_host, self.geus_dbname, self.geus_user, self.geus_password,
                             self.geus_port).set_index(index_column)

    def getStratificationMeta(self, index_column, sql="""
            SELECT
            replace(boreholeno, ' ', '') as boreholeno,
            sampleno,
            "top",
            bottom,
            rocktype,
            rocksymbol,
            totaldescr
            FROM casj_orbicon_dk_1735901099_pcjupiter_xl.dbo.lithsamp
        """):

        """
        Method for extracting meta information for the requested sensor.
        It is based on a default sql statement where the sensor_id is parsed into.
        This is run directly into Pandas for faster parsing.

        The function is called as a part of the extractSingularSensor() function.

        input:
            sql: SQL statement used to extract the data (a default is provided)

        output:
            A Pandas dataframe with the data from the sql request
        """

        return pd.read_sql(sql, self.conn).set_index(index_column)

    def getMaskFeature(self, driver_name, file_dir, kom_field_name, kom_code):
        driver = ogr.GetDriverByName(driver_name)

        dataSource = driver.Open(file_dir)

        layer = dataSource.GetLayer()

        mask_list = []
        mask_geom = ogr.Geometry(ogr.wkbPolygon)

        for nfeat in range(layer.GetFeatureCount()):

            feature = layer.GetFeature(nfeat)

            if feature.GetFieldAsInteger(kom_field_name) == kom_code:
                mask_list.append(feature)

                geom = feature.GetGeometryRef()

                mask_geom = mask_geom.Union(geom)

        dataSource.Destroy()

        bounding_points = mask_geom.GetEnvelope()

        bounding_points = [(bounding_points[0], bounding_points[2]), (bounding_points[0], bounding_points[3]),
                           (bounding_points[1], bounding_points[2]), (bounding_points[1], bounding_points[3])]

        bounding_box = self.createConvexHull(bounding_points)

        return mask_list, mask_geom, bounding_box

    def createConvexHull(self, point_list):
        thisGeometry = ogr.Geometry(ogr.wkbLineString)

        for points in point_list:
            thisGeometry.AddPoint(points[0], points[1])

        convexHull = thisGeometry.ConvexHull()

        return convexHull

    def getLayerIntersects(self, driver_name, file_dir, mask_geom):
        driver = ogr.GetDriverByName(driver_name)

        dataSource = driver.Open(file_dir)

        layer = dataSource.GetLayer()

        intersect_feature = []

        for nfeat in range(layer.GetFeatureCount()):

            feature = layer.GetFeature(nfeat)
            geom = feature.GetGeometryRef()

            geom.Intersects(mask_geom)

            if geom.Intersects(mask_geom):
                intersect_feature.append(layer.GetFeature(nfeat))

        return layer.GetName(), intersect_feature

    def extractSupportPoints(self, feat_list):
        x_all = []
        y_all = []

        for elm in feat_list:
            geom = elm.GetGeometryRef()

            if geom.GetGeometryName() == 'LINESTRING':
                x_all += [geom.GetX(i) for i in range(geom.GetPointCount())]
                y_all += [geom.GetY(i) for i in range(geom.GetPointCount())]

            if geom.GetGeometryName() == 'POLYGON':
                x_all.append(geom.Centroid().GetX())
                y_all.append(geom.Centroid().GetY())

        return pd.DataFrame({'x': x_all, 'y': y_all})

    def extractRasterValueFromPoint(self, raster, x, y):
        geotransform = raster.GetGeoTransform()
        origin_x = geotransform[0]
        origin_y = geotransform[3]
        pixel_width = geotransform[1]
        pixel_height = geotransform[5]

        xOffset = int((x - origin_x) / pixel_width)
        yOffset = int((y - origin_y) / pixel_height)

        if raster.ReadAsArray(xOffset, yOffset, 1, 1) in [None, -9999]:
            pass

        else:
            return raster.ReadAsArray(xOffset, yOffset, 1, 1)[0][0]

    def expandDataFrameWithZ(self, raster, data_frame, x_name, y_name, origin):

        z_col = np.zeros(data_frame[x_name].shape)
        for i in range(len(data_frame)):
            z_col[i] = jupiter.extractRasterValueFromPoint(raster, data_frame[x_name].values[i],
                                                           data_frame[y_name].values[i])

        return data_frame.assign(expand_value=z_col)

    def meshGridBasedOnFixedCells(self, xMin, yMin, xMax, yMax, delta):
        # The project extend in MIKE is based on the corners of the cells even though
        # they in their HELP files list that the the position of UTM based map projections
        # are the center coordinate of the corner cells. If you import a center based
        # ascii file and set the coordinate system to ETRS 1989 UTM-32N you will find that
        # the .dfs2 grid is displaced delta/2.

        # We calculate the maximum coordinates of the defined extend range.
        nXCells = int(np.ceil((xMax - xMin) / delta))
        nYCells = int(np.ceil((yMax - yMin) / delta))

        """
        Generation of 2D matrix. As per standard raster definition the cells has to be
        defined from their respective midter points. Raster extend is defined from the
        outer most coordinates, which is why we adjust with regards to the raster
        resolution (delta).
        """

        # Code for x, y gridding based on extend. The grid coordinates have to be based
        # on center coordinates to make sense.

        x_grid = np.linspace(xMin, xMax, nXCells)
        y_grid = np.linspace(yMin, yMax, nYCells)

        # Test for correct x spacing f0r each grid element in the x direction
        x_size_test = []
        for i in range(len(x_grid)):
            if i == len(x_grid) - 1:
                break
            else:
                x_size_test.append(x_grid[i + 1] - x_grid[i])

        # Test for correct y spacing for each grid element in the y direction
        y_size_test = []
        for i in range(len(y_grid)):
            if i == len(y_grid) - 1:
                break
            else:
                y_size_test.append(y_grid[i + 1] - y_grid[i])

        # Calculates the average of the x, y spacing for each grind element
        print("X spacing = {0}, y spacing = {1}".format(round((sum(x_size_test) / len(x_size_test)), 10),
                                                        round((sum(y_size_test) / len(y_size_test)), 10)))

        # Create meshgrid
        x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)

        return x_mesh, y_mesh

    def plotDataExtend(self, title, x_coord, y_coord, z_coord, mask_geom):
        x_all = []
        y_all = []
        codes = []
        paths = []
        if mask_geom.GetGeometryName() == 'MULTIPOLYGON':
            for polygon in mask_geom:
                for ring in polygon:
                    nx = [ring.GetX(i) for i in range(ring.GetPointCount())]
                    ny = [ring.GetY(i) for i in range(ring.GetPointCount())]

                    codes += [mpath.Path.MOVETO] + \
                             (len(nx) - 1) * [mpath.Path.LINETO]
                    x_all += nx
                    y_all += ny

                path = mpath.Path(np.column_stack((x_all, y_all)), codes)
                paths.append(path)

        elif mask_geom.GetGeometryName() == 'POLYGON':
            for ring in mask_geom:
                nx = [ring.GetX(i) for i in range(ring.GetPointCount())]
                ny = [ring.GetY(i) for i in range(ring.GetPointCount())]

                codes += [mpath.Path.MOVETO] + \
                         (len(nx) - 1) * [mpath.Path.LINETO]
                x_all += nx
                y_all += ny

            path = mpath.Path(np.column_stack((x_all, y_all)), codes)
            paths.append(path)

        fig, ax = plt.subplots()

        for path in paths:
            patch = mpatches.PathPatch(path, \
                                       facecolor='0.8', edgecolor='black', zorder=1)
            ax.add_patch(patch)

        ax.set_aspect(1.0)

        sc_plot = ax.scatter(x_coord, y_coord, s=50, c=z_coord, cmap='RdYlBu_r', zorder=2)

        plt.colorbar(sc_plot, ticks=np.linspace(min(z_coord), max(z_coord), 5, endpoint=True), label='Colorbar')
        plt.title(title)
        fig.show()

    def closeCursor(self, conn):
        conn.close()

    def createShapeFile(self, input_data, x_col, y_col, output_file, srid, driver="ESRI Shapefile"):

        driver = ogr.GetDriverByName(driver)
        data_source = driver.CreateDataSource(output_file)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(srid)
        layer = data_source.CreateLayer("data", srs, ogr.wkbPoint)

        col_defn = {}

        for columns in input_data.columns:
            if input_data[columns].dtype.name == 'float64':
                col_defn.update({columns: {'field_type': ogr.OFTReal,
                                           'field_name': input_data[columns].dtype.name,
                                           'source': 'column'}})

            if input_data[columns].dtype.name == 'int64':
                col_defn.update({columns: {'field_type': ogr.OFTInteger64,
                                           'field_name': input_data[columns].dtype.name,
                                           'source': 'column'}})

            if input_data[columns].dtype.name == 'object':
                col_defn.update({columns: {
                    'field_type': ogr.OFTString,
                    'field_name': input_data[columns].dtype.name,
                    'width': 255,
                    'source': 'column'}})

        for fields in col_defn:
            if col_defn[fields]['source'] == 'column':
                attribute = ogr.FieldDefn(fields[0:10], col_defn[fields]['field_type'])
                if 'width' in col_defn[fields]:
                    attribute.SetWidth(255)

                layer.CreateField(attribute)

        for i in range(len(input_data)):
            feature = ogr.Feature(layer.GetLayerDefn())

            for fields in col_defn:
                try:
                    # setting gdal field from dtype numpy.int64 type i fucked somehow.
                    if col_defn[fields]['field_name'] == 'int64':
                        feature.SetField(fields[0:10], int(input_data[fields].values[i]))
                    else:
                        feature.SetField(fields[0:10], input_data[fields].values[i])
                except Exception as e:
                    print("Error setting setting field: {0} with error: \n {1}".format(fields, e))

            coordinate_WKT = "Point({0} {1})".format(input_data[x_col].values[i], input_data[y_col].values[i])
            point = ogr.CreateGeometryFromWkt(coordinate_WKT)
            feature.SetGeometry(point)

            layer.CreateFeature(feature)
            feature.Destroy()

        data_source.Destroy()

    def updateEnvironment(self, env_name, path):
        os.environ.update({env_name: path})

    def RunCommand_Logged(self, cmd, logstd, logerr):
        CREATE_NO_WINDOW = 0x08000000
        call(cmd, stdout=logstd, stderr=logerr, creationflags=CREATE_NO_WINDOW)

    def createInterpolationNN(self, input_file, attribute_column, output_file, cell_size, mask_geom, weights,
                              import_log, error_log):
        """

        The interpolation rutine is called from SAGA GIS via cmd calls.
        As such it requires file generation and a local installation of SAGA GIS.
		This means that this script cannot be executed directly in Azure, but has
		to be located in the xddocker1 instance.

        There does exists other libraries that can be utilized such as:
            https://doc.cgal.org/latest/Interpolation/index.html#Chapter_2D_and_Surface_Function_Interpolation
            https://pypi.python.org/pypi/naturalneighbor/0.1.8

       As far as I can tell cgal is the most maintained. I cannot however install naturalneighbor
		due to python not being able to see the c++ runtime library it needs to compile from.
		That library consists of a wrapper around c++ code.

		cgal does have a python wrapper also, but as far as I could tell none of the interpolation
		rutines have been implimented so far.

        The code used to do the interpolatio n in SAGA GIS is from:
            https://github.com/sakov/nn-c

        """

        logstd = open(import_log, 'a')
        logerr = open(error_log, 'a')

        data_source = ogr.Open(input_file)

        layer = data_source.GetLayer(0)

        interp_attr_indice = layer.GetLayerDefn().GetFieldIndex(attribute_column)

        bounding_points = mask_geom.GetEnvelope()

        bounding_points = [(bounding_points[0], bounding_points[2]), (bounding_points[0], bounding_points[3]),
                           (bounding_points[1], bounding_points[2]), (bounding_points[1], bounding_points[3])]

        print("Starting interpolation")

        cmd = [os.environ['SAGA_PATH'] + os.sep + r'saga_cmd', 'grid_gridding', '3',
               '-POINTS', input_file,
               '-TARGET_OUT_GRID', output_file,
               '-FIELD', str(interp_attr_indice),
               '-TARGET_DEFINITION', '0',
               '-TARGET_USER_SIZE', str(cell_size),
               '-TARGET_USER_XMIN', str(bounding_points[0][0]),
               '-TARGET_USER_XMAX', str(bounding_points[2][0]),
               '-TARGET_USER_YMIN', str(bounding_points[0][1]),
               '-TARGET_USER_YMAX', str(bounding_points[3][1]),
               '-TARGET_USER_FITS', '0',
               '-METHOD', '1',
               '-WEIGHT', str(weights)
               ]

        try:
            jupiter.RunCommand_Logged(cmd, logstd, logerr)

            logstd.close()
            logerr.close()

            print("Interpolation completed")
        except Exception as e:
            logerr.write("Exception thrown while processing file: " + input_file + "\n")
            logerr.write("ERROR: %s\n" % e)

            logstd.close()
            logerr.close()

            print("ERROR")

    def createContour(self, input_file, output_file_line, output_file_polygon, poly_parts, scale, zmin, zmax, step,
                      import_log, error_log):
        logstd = open(import_log, 'a')
        logerr = open(error_log, 'a')

        print("Starting contouring")

        cmd = [os.environ['SAGA_PATH'] + os.sep + r'saga_cmd', 'shapes_grid', '5',
               '-GRID', input_file,
               '-CONTOUR', output_file_line,
               '-POLYGONS', output_file_polygon,
               '-POLY_PARTS', str(poly_parts),
               '-SCALE', str(scale),
               '-ZMIN', str(zmin),
               '-ZMAX', str(zmax),
               '-ZSTEP', str(step)
               ]

        try:
            jupiter.RunCommand_Logged(cmd, logstd, logerr)

            logstd.close()
            logerr.close()

            print("Contouring completed")
        except Exception as e:
            logerr.write("Exception thrown while processing file: " + input_file + "\n")
            logerr.write("ERROR: %s\n" % e)

            logstd.close()
            logerr.close()


def createFolder(directory, folder_name):
    folder_directory = directory + os.sep + folder_name
    directory = os.path.dirname(folder_directory)
    if not os.path.exists(folder_directory):
        os.makedirs(folder_directory)

    return folder_directory


if __name__ == '__main__':

    prod_list = ['sven']

    border_schema_name = 'public'
    gw_pot_schema_name = 'gw_pot'

    age_cut_off = 30
    cut_off_drill_depth = 15
    screen_bottom = 7
    for i in range(len(prod_list)):
        print('Processing: {}'.format(prod_list[i]))
        customer_dump_site = r'C:\Temp\{}'.format(prod_list[i])
        jupiter = jupiterAnalyser(cust_host= self.cust_host, cust_dbname = self.cust_dbname, cust_user = self.cust_user,
                                  cust_password = self.cust_password, cust_port= self.cust_port,
                                  geus_host= self.geus_host , geus_dbname = self.geus_dbname, geus_user= self.geus_user,
                                  geus_password= self.geus_password, geus_port= self.geus_port)

        # Bounding box
        bbox = jupiter.runQuery(
            """ select ST_AsText(ST_Buffer(bbox, 5000)) as geom, ST_SRID(bbox) as srid from {0}.hardcoded_bbox """.format(
                border_schema_name),
            jupiter.cust_host, jupiter.cust_dbname, jupiter.cust_user, jupiter.cust_password, jupiter.cust_port)

        if i == 0:
            coast_support = jupiter.runQuery("""select 'coast' as origin, val, ST_X(geom) as x, ST_Y(geom) as y 
                                        from gw_pot.mv_gwpot_coast_dtm_kbh
                                        where val is not null""".format(gw_pot_schema_name),
                                             jupiter.cust_host, jupiter.cust_dbname, jupiter.cust_user,
                                             jupiter.cust_password, jupiter.cust_port)

            stream_support = jupiter.runQuery("""select 'stream' as origin, val, ST_X(geom) as x, ST_Y(geom) as y 
                                        from {0}.mv_gwpot_streams_dtm_kbh
                                        where val is not null""".format(gw_pot_schema_name),
                                              jupiter.cust_host, jupiter.cust_dbname, jupiter.cust_user,
                                              jupiter.cust_password, jupiter.cust_port)

            mask_wkt = bbox['geom'].values[0]
            srid = bbox['srid'].values[0]

            dgu_data = pd.concat([jupiter.getPgsqlBorholeMeta(index_column=['boreholeno', 'intakeno'],
                                                              screen_bottom=screen_bottom,
                                                              mask_wkt=mask_wkt,
                                                              srid=srid)])

        else:
            coast_support = pd.concat([coast_support, jupiter.runQuery("""select 'coast' as origin, val, ST_X(geom) as x, ST_Y(geom) as y 
                                        from gw_pot.mv_gwpot_coast_dtm_kbh
                                        where val is not null""".format(gw_pot_schema_name),
                                                                       jupiter.cust_host, jupiter.cust_dbname,
                                                                       jupiter.cust_user, jupiter.cust_password,
                                                                       jupiter.cust_port)])

            stream_support = pd.concat([stream_support, jupiter.runQuery("""select 'stream' as origin, val, ST_X(geom) as x, ST_Y(geom) as y 
                                        from {0}.mv_gwpot_streams_dtm_kbh
                                        where val is not null""".format(gw_pot_schema_name),
                                                                         jupiter.cust_host, jupiter.cust_dbname,
                                                                         jupiter.cust_user, jupiter.cust_password,
                                                                         jupiter.cust_port)])

            dgu_data = pd.concat([dgu_data, jupiter.getPgsqlBorholeMeta(index_column=['boreholeno', 'intakeno'],
                                                                        screen_bottom=screen_bottom,
                                                                        mask_wkt=mask_wkt,
                                                                        srid=srid)])

    print("Removing any boreholes with average water level lower than the bottom level of the borehole")
    dgu_data = dgu_data[(dgu_data['calc_bottom_kote'].notnull()) &
                        (dgu_data['avg_wl_watlevgrsu'] >= dgu_data['calc_bottom_kote'])].reindex()


    print("""Removing all boreholes where the measure water table exceeds the terrain.""")
    dgu_data['avg_wl_watlevgrsu'] = np.where(dgu_data['avg_wl_watlevgrsu'] < 0, 0, dgu_data['avg_wl_watlevgrsu'])


    dgu_data = dgu_data[(dgu_data['avg_wl_watlevgrsu'] >= 0)].reindex()

    print("""Adding Sensor and Decreed measure """)
    data_sensors = jupiter.getDiscreteMeasurementsAndSensorsData(index_column=['thingid', 'messageid', 'observationid'])
    print(data_sensors['avg_wl_watlevgrsu'].values)
    dgu_data = pd.concat([dgu_data, data_sensors])
    print(dgu_data['avg_wl_watlevgrsu'].values)

    print("Creating shapefile with relevant borehole information")
    filtered_file_path = createFolder(customer_dump_site, r"interp_data")
    jupiter.createShapeFile(pd.concat([dgu_data.index.to_frame(), dgu_data], axis=1, join='inner'), 'xutm', 'yutm',
                            filtered_file_path + os.sep + r"dgu_data_to_interp.shp", int(bbox['srid'].values[0]))

    print("Merging boundary and support points with relevant borehole information")
    x_concat = np.concatenate((dgu_data['xutm'], coast_support['x'], stream_support['x'],))
    y_concat = np.concatenate((dgu_data['yutm'], coast_support['y'], stream_support['y'],))
    z_concat = np.concatenate(
        (dgu_data['avg_wl_watlevgrsu'], coast_support['val'], stream_support['val'],))
    source_concat = np.concatenate((dgu_data.index.get_level_values('boreholeno').values, coast_support['origin'],
                                    stream_support['origin'],))

    collected = pd.DataFrame({'X': x_concat, 'Y': y_concat, 'Z': z_concat, 'Source': source_concat})

    print("Creating shapefile with merged dataset for DVR90")
    dvr_90_file_path = createFolder(customer_dump_site, r"result_dvr90")
    jupiter.createShapeFile(collected, 'X', 'Y', dvr_90_file_path + os.sep + r"interp_points_dvr90.shp",
                            int(bbox['srid'].values[0]))

    alpha = 3000
    if len(prod_list) > 1:
        print("Recalculating bounding box")
        points = create_point_set(dvr_90_file_path + os.sep + r"interp_points_dvr90.shp")
        edges, tri = alpha_shape(points, alpha=alpha, only_outer=True)
        sort = sortList(edges, 2)
        mask_wkt = create_wkt(points, sort)

    print("Setting SAGA GIS path")
    jupiter.updateEnvironment('SAGA_PATH', r'C:\Program Files (x86)\SAGA-GIS')

    print('Starting interpolation routine')
    jupiter.createInterpolationNN(dvr_90_file_path + os.sep + r"interp_points_dvr90.shp", 'Z',
                                  dvr_90_file_path + os.sep + r"gwpot_dvr90.sgrd", 25, \
                                  ogr.CreateGeometryFromWkt(mask_wkt), 0, \
                                  customer_dump_site + os.sep + "import.log",
                                  customer_dump_site + os.sep + "import.error.log")

    print("Creating polygonized contoures")
    create_isobands(dvr_90_file_path + os.sep + r"gwpot_dvr90.sdat",
                    dvr_90_file_path + os.sep + r"gwpot_dvr90_contour_polygon.shp")

    print("Creating shapefile with merged dataset for MUT without streams support points")
    mut_file_path = createFolder(customer_dump_site, r"result_mut_without_stream_suppot")

    coast_support['val'] = 0
    stream_support['val'] = 0

    x_concat = np.concatenate((dgu_data['xutm'], coast_support['x']))
    y_concat = np.concatenate((dgu_data['yutm'], coast_support['y']))
    z_concat = np.concatenate((dgu_data['avg_wl_watlevgrsu'], coast_support['val']))

    source_concat = np.concatenate(
        (dgu_data.index.get_level_values('boreholeno').values, coast_support['origin']))

    collected = pd.DataFrame({'X': x_concat, 'Y': y_concat, 'Z': z_concat, 'Source': source_concat})
    jupiter.createShapeFile(collected, 'X', 'Y', mut_file_path + os.sep + r"interp_points_mut.shp",
                            int(bbox['srid'].values[0]))

    print('Starting interpolation routine')
    jupiter.createInterpolationNN(mut_file_path + os.sep + r"interp_points_mut.shp", 'Z',
                                  mut_file_path + os.sep + r"gwpot_mut.sgrd", 25, \
                                  ogr.CreateGeometryFromWkt(mask_wkt), 0, \
                                  customer_dump_site + os.sep + "import.log",
                                  customer_dump_site + os.sep + "import.error.log")

    print("Creating polygonized contoures")
    create_isobands(mut_file_path + os.sep + r"gwpot_mut.sdat",
                    mut_file_path + os.sep + r"gwpot_mut_contour_polygon.shp")