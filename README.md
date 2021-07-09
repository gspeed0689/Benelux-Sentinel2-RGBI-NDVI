## Benelux-Sentinel2-RGBI-NDVI
Preprocessing script for easy creation of RGB &amp; Near Infrared and NDVI JPEG-2000 Sentinel 2 imagery files from .SAFE

## Purpose

The purpose of this code repository is to accompany the Geo-Yoda data repository of Benelux (Belgium, Netherlands, Luxembourg) Sentinel 2 satellite imagery preprocessed for easy use from the .SAFE format that the European Space Agency (ESA) Developed. The dataset consists of JPEG-2000 (JP2) multi-band image files containing the red, green, blue, and near-infrared (RGBI) bands, and pre-processed NDVI single-band JPEG-2000 image files. The initial data is collected from the Sentinel data hub, extracted to directories from the .SAFE zip files, and using the `rasterio` library it takes the individual band JP2 files and combines them into a single multi-band image file. 

## NDVI Calculation

The NDVI calculation used is as follows. 

![NDVI Equation](https://github.com/gspeed0689/Benelux-Sentinel2-RGBI-NDVI/raw/main/NDVI_Equation.PNG)

The `Infrared - Red / Infrared + Red` is a standard NDVI calculation, multiplying by 2^15 is to fill the signed 16-bit number space `(2^16 - (2^16)/2)`. The `floor`function is to return the values from floats to integer values. 

NDVI is stored in a separate file due to the nature of the data and the JP2 file format; the optical data (RGBI) data is stored as unsigned integers (`0 - (2^16 - 1)`), and NDVI requires signed number formats. The JP2 driver in `rasterio` does not have a floating point encoder, so the values must be stored as integers, and thus the 2^15 multiplier, and the floor function, so we can then fit the NDVI results into a signed 16-bit integer encoding. 

## Script Usage

The notebook folder is the working IPython notebooks I originally created to develope the script and is there for reference only. 

The Sentinel2_RGBI_NDVI.py file is the entirely self contained script. 

Basic use: 

`python3 Sentinel2_RGBI_NDVI.py -f /path/to/folder`

Add `-ndvi` to tell the script to generate NDVI JP2 files. 
Add `-rgbi` to tell the script to generate Red, Green, Blue, Near-Infrared JP2 files. 

## Current version 0.1.0

## Future versions 

1.0 - Rewritten in an object oriented class based way. 
1.1 - File Name Parsing for custom file name conventions, aim to be like `%yyyy-%mm-%dd` style. 
