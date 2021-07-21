import os, glob, argparse
import rasterio
import numpy

debug_level = 0

def sdb(lvl, msg):
    """Simple Debug messages

    Args:
        lvl (int): Integer for a debug, lower the value the more the message will show up
        msg (str): Message to be printed
    """
    if lvl <= debug_level:
        print(msg)

def cmd_line():
    """Grabs the command line arguments when calling the script
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder")
    parser.add_argument("-ndvi", action="store_true", default=False)
    parser.add_argument("-rgbi", action="store_true", default=False)
    return(parser.parse_args())

def rgbi_processing(image_dict_entry, img_dict, d):
    """Processes a .SAFE file into a JPEG-2000 4-band RGB and Near-Infrared unsigned int16 raster. 

    Args:
        image_dict_entry (dict): A single entry from main's img_data
        img_dict (dict): The full img_data
        d (str): Directory as a string
    """
    file_list = [img_dict[image_dict_entry]["red"], img_dict[image_dict_entry]["green"], img_dict[image_dict_entry]["blue"], img_dict[image_dict_entry]["infrared"]]
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta
    meta.update(count = len(file_list))
    out_file_name = d + os.sep + image_dict_entry + ".jp2"
    meta.update(count = len(file_list))
    #print(meta)
    if os.path.exists(out_file_name) == False:
        with rasterio.open(out_file_name, "w", **meta) as dst:
            for id, layer in enumerate(file_list, start=1):
                with rasterio.open(layer) as src1:
                    dst.write_band(id, src1.read(1))

def ndvi_processing(image_dict_entry, img_dict, d):
    """Processes a .SAFE file into a JPEG-2000 NDVI signed int16 raster. 

    Args:
        image_dict_entry (dict): A single entry from main's img_data
        img_dict (dict): The full img_data
        d (str): Directory as a string
    """
    band_infrared, band_red, ndvi_kwargs = rasterio.open(img_dict[image_dict_entry]["infrared"]).read(1), rasterio.open(img_dict[image_dict_entry]["red"]).read(1), rasterio.open(img_dict[image_dict_entry]["infrared"]).meta
    numpy.seterr(divide='ignore', invalid='ignore')
    ndvi = ((band_infrared.astype(float) - band_red.astype(float)) / (band_infrared + band_red)) * (2**15)
    ndvi = numpy.floor(ndvi)
    ndvi = ndvi.astype(int)
    ndvi_kwargs.update(dtype=rasterio.int16, count=1)
    out_file_name = d + os.sep + image_dict_entry + ".jp2"
    ndvi_file_name = out_file_name.replace(".jp2", "_ndvi.jp2")
    print(ndvi_file_name)
    if os.path.exists(ndvi_file_name) == False:
        with rasterio.open(ndvi_file_name, 'w', **ndvi_kwargs) as dst:
            dst.write_band(1, ndvi.astype(rasterio.int16))

def main():
    """The main part of the program, requires command line arguments to function. 
        Works with Sentinel 2 .SAFE unzipped folders in a single directory. 
        Will process a .SAFE into JPEG-2000 files for easy usage in GIS. 
        Does not take into account a lot of data that is also included with a full .SAFE directory, 
            should only be used for visualization purposes. 
    """
    args = cmd_line()
    d = args.folder
    rgbi_process = args.rgbi
    ndvi_process = args.ndvi
    safe_dirs = glob.glob(d + os.sep + "S2*.SAFE")
    sdb(1, f"Found {len(safe_dirs)} .SAFE Sentinel 2 Directories")
    granules = []
    for i in safe_dirs:
        granules.append(glob.glob(i + os.sep + "GRANULE" + os.sep + "*")[0])
    sdb(1, f"Found {len(granules)} granules, this value should match the number of SAFE directories")
    img_data = {}
    for i in granules:
        sdb(2, f"currently finding files from granule {i}")
        img_dir = i + os.sep + "IMG_DATA"
        red = glob.glob(img_dir + os.sep + "*_B04.jp2")[0]
        green = glob.glob(img_dir + os.sep + "*_B03.jp2")[0]
        blue = glob.glob(img_dir + os.sep + "*_B02.jp2")[0]
        infrared = glob.glob(img_dir + os.sep + "*_B08.jp2")[0]
        tile = red.split(os.sep)[-1].split("_")[0]
        date = red.split(os.sep)[-1].split("_")[1].split("T")[0]
        orbit = red.split(d + os.sep)[-1].split(os.sep)[0].split("_")[4]
        satellite = red.split(d + os.sep)[-1].split(os.sep)[0].split("_")[0]
        img_name = f"{tile}_{orbit}_{satellite}_{date}"
        img_data[img_name] = {"red": red, "green": green, "blue": blue, "infrared": infrared}
    sdb(1, f"Found {len(list(img_data.keys()))} complete image files,\n\tthis value should match the number of SAFE directories")
    sdb(2, str(img_data))
    for image in list(img_data.keys()):
        if rgbi_process == True:
            rgbi_processing(image, img_data, d)
        if ndvi_process == True:
            ndvi_processing(image, img_data, d)
        
if __name__ == "__main__":
    main()
