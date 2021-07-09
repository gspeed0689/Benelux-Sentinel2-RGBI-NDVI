## Benelux-Sentinel2-RGBI-NDVI
Preprocessing script for easy creation of RGB &amp; Near Infrared and NDVI JPEG-2000 Sentinel 2 imagery files from .SAFE

## Purpose

The purpose of this code repository is to accompany the Geo-Yoda data repository of Benelux (Belgium, Netherlands, Luxembourg) Sentinel 2 satellite imagery preprocessed for easy use from the .SAFE format that the European Space Agency (ESA) Developed. The dataset consists of JPEG-2000 (JP2) multi-band image files containing the red, green, blue, and near-infrared bands, and pre-processed NDVI single-band JPEG-2000 image files. The initial data is collected from the Sentinel data hub, extracted to directories from the .SAFE zip files, and using the `rasterio` library it takes the individual band JP2 files and combines them into a single multi-band image file. 

## NDVI Calculation

The NDVI calculation used is as follows. 

![NDVI Equation](https://github.com/gspeed0689/Benelux-Sentinel2-RGBI-NDVI/raw/main/NDVI_Equation.PNG)

The `Infrared - Red / Infrared + Red` is a standard NDVI calculation, multiplying by 2^15 is to fill the signed 16-bit number space `(2^16 - (2^16)/2)`. The `floor`function is to return the values from floats to integer values. 
