# Measurement data from Field Registration
Semicolon-separated file with one measurement per line. First line contains column names.
Must include following columns:
* **CaseName** - text
* **CaseDescription** - text
* **Groundwater-potential-location** - location as a point in WKT format in projection EPSG:25832
* **Groundwater-potential-level-below-surface** - measurement in meters under terrain
* **Groundwater-potential-measurementtime** - time of measurement. Formats can be
dd-MM-yyy HH:mm | dd-MM-yyy HH:mm:ss | dd/MM/yyyy H:mm | dd/MM/yyyy H:mm:ss | dd/MM/yyyy HH:mm | dd/MM/yyyy HH:mm:ss
* **Groundwater-potential-sensor-id** - Unique id of sensor/borehole. If there are multiple measurements from same borehole, they must have same identifier for data to be displayed in timeseries.


# Measurement data from Metro data
Semicolon-separated file with one measurement per line. First line contains column names.
Must include following columns:
* **Boring** - Unique ID for borehole. Measurements from same borehole must have same identifier. 
* **Placering** - Location name for measurement (e.g. København H)
* **Adresse** - Address for location (eg. Colbjørnsengade 15, 1652 København V)
* **DGU** -
* **Utm koordinat X**
* **Utm koordinat Y**
* **Name** - Sensorname (can be made optional or removed?)
* **Date** - (Rename this?) Date and time of measurement formats can be: 
dd-MM-yyy HH:mm | dd-MM-yyy HH:mm:ss | dd/MM/yyyy H:mm | dd/MM/yyyy H:mm:ss | dd/MM/yyyy HH:mm | dd/MM/yyyy HH:mm:ss
* **terræn (Z)** - terrain level (number - can have decimals)
* **Value (m)** - number (can have decimals)
* **m u.t.** - groundwater level in meters below terrain - number (can have decimals) 