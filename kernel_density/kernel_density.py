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
	
def transformShapeToWgs84(source, target):
	# This transform is used to make the coord sys explicit in the merged file
	ref = "WGS 1984 UTM Zone 32N"
	print 'Transforming file'
	print '\tSource ' + source 
	print '\tTarget ' + target
	print '\tWith ref ' + ref
	arcpy.Project_management(source, target, arcpy.SpatialReference(ref))
	
def peformKernelDensity(source_shape, target_raster, cell_size, search_radius):
	print 'Performing kernel density, saving ' + target_raster 
	arcpy.CheckOutExtension("spatial")
	kdens = KernelDensity(source_shape, "NONE", cell_size, search_radius)
	kdens.save(target_raster)
	arcpy.CheckInExtension("spatial")
	
def clipRasterMap(source_file, clip_target, clip_rectangle, raster_to_fit):
	print 'Clipping raster'
	print '\tsource ' + source_file 
	print '\ttarget ' + clip_target
	print '\trectangle ' + clip_rectangle
	print '\traster to fit ' + raster_to_fit
	arcpy.Clip_management(source_file, clip_rectangle, clip_target, raster_to_fit, 0.0000001, 'NONE', 'MAINTAIN_EXTENT')

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
merged_transformed_file = config['temp_directory'] + config['file_name_raw_merged_transformed_temp']
transformShapeToWgs84(merged_file, merged_transformed_file)
raw_raster_file = config['temp_directory'] + config['file_name_raw_kernel_density_temp']
peformKernelDensity(merged_transformed_file, raw_raster_file, config['kernel_density_cell_size'], config['kernel_density_search_radius'])
clipRasterMap(raw_raster_file, config['file_name_kernel_density'], config['area_rectangle'], config['file_name_raster_to_fit'])
cleanup_temp_files(config['temp_directory'])
