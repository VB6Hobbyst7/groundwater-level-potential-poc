# Schemas
* public - In this schema, the interesting table is hovedvandloeb an Orbicon refined data for all major streams in Denmark
* data - This schema contains tables with data about lakes, coastal line, harbours used in gw_pot schema views 
* gw_pot - Interesting in this schema, is a table for the interpolation gwpot_dvr90_contour_polygon, materialized views for support points, data for the interpolation and streams used in the interpolation, views for support point, data for the interpolation and sensor data.

## public
Hovedvandloeb table  <br>
![hovedvandloeb.png](/Wiki/.attachments/hovedvandloeb-35e12223-767f-4514-a033-f9df46682d2a.png)

## data
Tables in data  <br>
![data.png](/Wiki/.attachments/data-7208f9e6-2d0d-4641-bb08-2788b02a2598.png)

## gw_pot
### Streams
#### v_streams_kbh
View based on the table hovedvandloeb (major streams) for Copenhagen area
#### v_stream_as_points_kbh
Represntation of the streams as points <br>
![v_stream_as_points_kbh.png](/Wiki/.attachments/v_stream_as_points_kbh-0a914df8-4f39-40d0-b31b-2e39623099e8.png)
#### v_gwpot_stream_dtm_kbh
A view combining v_stream_as_points_kbh with terrain elevation data  <br>
![v_gwpot_stream_dtm.png](/Wiki/.attachments/v_gwpot_stream_dtm-57c4ea73-97c0-4781-9a29-f226331bee41.png)
### Coasts
#### v_coast_as_points
![v_coast_as_points_kbh.png](/Wiki/.attachments/v_coast_as_points_kbh-9f118ae9-96ee-45a8-b44d-6d47ab51df01.png)
#### v_gwpot_coast_dtm_kbh
![v_gwpot_coast_dtm_kbh.png](/Wiki/.attachments/v_gwpot_coast_dtm_kbh-a7fe25aa-6a87-4a2b-90a9-958107eef781.png)
### Sensors and Field Registration
#### v_theregionaldatahub_fieldreg_measurements_last_known_kbh
A view with latest field registration discrete measurments used for the layer in the map <br>
![v_theregionaldatahub_fieldreg_measurements_last_known_kbh.png](/Wiki/.attachments/v_theregionaldatahub_fieldreg_measurements_last_known_kbh-4c9f540b-f26e-4d47-b792-b7c9624301d1.png)
#### v_theregionaldatahub_metro_measurements_last_known_kbh
A view with latest imported reading from copenhagen metro used for the layer in the map <br>
![v_theregionaldatahub_metro_measurements_last_known_kbh.png](/Wiki/.attachments/v_theregionaldatahub_metro_measurements_last_known_kbh-9b29b7d2-c478-4c08-b63c-6251495dd219.png)
#### v_theregionaldatahub_measurements_last_known_kbh
A view used by the interpolation to import latest data from the sensorhub database <br>
![v_theregionaldatahub_measurements_last_known_kbh.png](/Wiki/.attachments/v_theregionaldatahub_measurements_last_known_kbh-24e657cd-3f1f-41b5-a4a5-1c76fa243e6e.png)
