import sys
from kernel_density_config import config
import arcpy, arcinfo
from arcpy.sa import *
import zipfile
import shutil
import os

def createRequiredFolders():
	print 'Create the folders we need'

def unzipMatrikkelFiles(zip_files, temp_folder):
	print 'Unzipping files'
	unzipped_shape_files = []
	for zip_file in zip_files:
		zip = zipfile.ZipFile(zip_file['zip_name'], 'r')
		zip_names = zip.namelist()
		for zip_name in zip_names:
			if zip_name.startswith(zip_file['target_shape_prefix']):
				extracted_file = zip.extract(zip_name, temp_folder)
				print "\tUnzipped " + extracted_file
				if zip_name.endswith('.shp'):
					unzipped_shape_files.append(extracted_file)
		zip.close()
	return unzipped_shape_files
	
def filterLayers():
	print 'Select only the wanted features from the files. Output is smaller shape files'

def mergeMatrikkelFiles(source_files, merge_target):
	print 'Merging files'
	fieldMappings = arcpy.FieldMappings()
	for file in source_files:
		fieldMappings.addTable(file)
		
	arcpy.Merge_management(source_files, merge_target)
	
def peformKernelDensity(source_shape, target_raster, cell_size, search_radius):
	print 'Performing kernel density'
	arcpy.CheckOutExtension("spatial")
	kdens = KernelDensity(source_shape, "NONE", cell_size, search_radius)
	kdens.save(target_raster)
	arcpy.CheckInExtension("spatial")
	
	
def clipRasterMap(source_file, clip_target, clip_rectangle):
	print 'Clipping raster, saving into ' + clip_target
	#arcpy.Clip_management(source_file, clip_rectangle, clip_target, "#", "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
	arcpy.Clip_management(source_file, clip_rectangle, clip_target)


def cleanup_temp_files(temp_files):
	print 'Delete all files from ' + temp_files
	shutil.rmtree(temp_files)
	
def create_temp_dir(directory):
	print 'Create temp directory'
	if not os.path.exists(directory):
		os.makedirs(directory)

create_temp_dir(config['temp_directory'])
cleanup_temp_files(config['temp_directory'])
unzipped_files = unzipMatrikkelFiles(config['matrikkel_zip_files'], config['temp_directory'])
merged_file = config['temp_directory'] + config['file_name_raw_merged_temp']
mergeMatrikkelFiles(unzipped_files, merged_file)
raw_raster_file = config['temp_directory'] + config['file_name_raw_kernel_density_temp']
peformKernelDensity(merged_file, raw_raster_file, config['kernel_density_cell_size'], config['kernel_density_search_radius'])
clipRasterMap(raw_raster_file, config['file_name_kernel_density'], config['area_rectangle'])
cleanup_temp_files(config['temp_directory'])
sys.exit(0)	
	
	
#from arcpy.sa import *


#outKdens = KernelDensity("C:\\Users\\marius.blomli\\Documents\\NTNU-Prosjekt\\Larvik\\Matrikkeldata\\SOSIuttrekk\\07_Vestfold\\0709_Larvik\\UTM32_Euref89\\Shape\\32_Matrikkeldata_0709\\32_0709adresse_punkt.shp", "NONE", 1, 5)
#outKdens.save("C:\\Users\\marius.blomli\\Documents\\NTNU-Prosjekt\\testing\\larvik_kernel_density.img")

#ext = arcpy.CheckExtension("Spatial")
#arcpy.CheckOutExtension("spatial")
#outKdens = KernelDensity("C:\\Users\\marius.blomli\\Documents\\NTNU-Prosjekt\\Larvik\\Matrikkeldata\\SOSIuttrekk\\07_Vestfold\\0709_Larvik\\UTM32_Euref89\\Shape\\32_Matrikkeldata_0709\\32_0709adresse_punkt.shp", "NONE", 100, 50)
#outKdens.save("C:\\Temp\\ntnu_temp\\test.img")
#arcpy.CheckInExtension("spatial")
#sys.exit(0)

unzipped_files = unzipMatrikkelFiles(config['matrikkel_zip_files'], config['temp_directory'])
merged_file = config['temp_directory'] + config['file_name_raw_merged']
mergeMatrikkelFiles(unzipped_files, merged_file)
raw_raster_file = config['temp_directory'] + config['file_name_raw_kernel_density']
peformKernelDensity(merged_file, raw_raster_file, 100, 500)
sys.exit(0)

fc = "C:\\Temp\\ntnu_temp\\32_0709adresse_punkt.shp"
fc2 = "C:\\Temp\\ntnu_temp\\32_0706adresse_punkt.shp"

out = "C:\\Temp\\ntnu_temp\\larvik_sandefjort_test.shp"

fieldMappings = arcpy.FieldMappings()

fieldMappings.addTable(fc)
fieldMappings.addTable(fc2)

arcpy.Merge_management([fc, fc2], out)

sys.exit(0)

rows = arcpy.SearchCursor(fc)
rows2 = arcpy.SearchCursor(fc2)

fields = arcpy.ListFields(fc, "", "String")

for row in rows:
    for field in fields:
        if field.type != "Geometry":
            print "%s: Value = %s" % (field.name, row.getValue(field.name))