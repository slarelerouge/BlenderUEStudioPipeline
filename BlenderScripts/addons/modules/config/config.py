# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


#
import configparser

import os
import pathlib

from logger.logger import log

log.info("Loading config...")

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
# To not lowercase the keys
config.optionxform = str


local_path = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(local_path, "config.ini")
config.read(config_file_path)


# Unreal
UNREAL_ROOT_DIRECTORY = config["UNREAL"]["root_directory_unreal"]
UNREAL_MASTER_MATERIAL_DIRECTORY = config["UNREAL"]["master_material_directory"]
UNREAL_MATERIAL_LIBRARY_DIRECTORY = config["UNREAL"]["material_library_directory"]


# Blender
BLENDER_ROOT_DIRECTORY = config["BLENDER_ASSETS"]["root_directory_blender"]
BLENDER_MASTER_MATERIAL_LIBRARY_FILE_NAME = config["BLENDER_ASSETS"]["master_material_library_file"]
BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE = config["BLENDER_ASSETS"]["material_instance_library_file"]
# Get library paths
library_items = config.items("BLENDER_LIBRARIES")
BLENDER_ASSET_LIBRARIES = {}
for library_name, path in library_items:
    BLENDER_ASSET_LIBRARIES[library_name] = os.path.normpath(path)
BLENDER_MASTER_MATERIAL_LIBRARY_FILE_PATH = ""
for asset_library in BLENDER_ASSET_LIBRARIES:
    library_path = pathlib.Path(BLENDER_ASSET_LIBRARIES[asset_library])
    blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
    for blend_file in blend_files:
        if blend_file.name == BLENDER_MASTER_MATERIAL_LIBRARY_FILE_NAME:
            BLENDER_MASTER_MATERIAL_LIBRARY_FILE_PATH = str(blend_file)
            break
BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE_PATH = ""
for asset_library in BLENDER_ASSET_LIBRARIES:
    library_path = pathlib.Path(BLENDER_ASSET_LIBRARIES[asset_library])
    blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
    for blend_file in blend_files:
        if blend_file.name == BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE:
            BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE_PATH = str(blend_file)
            break
MATERIAL_INSTANCE_CATALOG_ID = config["BLENDER_ASSETS"]["material_instance_catalog_id"]


# Pipeline
RAW_DATA_ROOT_DIRECTORY = os.path.normpath(config["PIPELINE"]["root_directory_raw_data"]+"/")
MATERIAL_PARAMETER_JSON_FILE_PATH = os.path.normpath(config["PIPELINE"]["material_parameter_json_file_path"])
UNREAL_INSTALL_DIRECTORY = os.path.normpath(config["PIPELINE"]["unreal_install_directory"])
#UNREAL_PROJECT_DIRECTORY = os.path.normpath(config["PIPELINE"]["unreal_project_directory"])
UNREAL_REMOTE_CONTROL_MODULE_DIRECTORY = os.path.normpath(os.path.join(UNREAL_INSTALL_DIRECTORY, r"Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python/"))

# Cache
#MATERIAL_GLB_CACHE = os.path.normpath(config["CACHE"]["material_glb"]+"/")

#
MATERIAL_PARAMETER_LUT = {}
parameter_items = config.items( "PARAMETER_LUT" )
for parameter_name, unreal_parameter_name in parameter_items:
    MATERIAL_PARAMETER_LUT[parameter_name] = unreal_parameter_name

#
REMOTE_DEFAULT_RECEIVE_BUFFER_SIZE = int(config["UNREAL_REMOTE"]["default_receive_buffer_size"])

log.debug("CONFIG CONSTANT")
log.debug(f"    RAW_DATA_ROOT_DIRECTORY: {RAW_DATA_ROOT_DIRECTORY}")
log.debug(f"    UNREAL_INSTALL_DIRECTORY: {UNREAL_INSTALL_DIRECTORY}")
log.debug(f"    UNREAL_REMOTE_CONTROL_MODULE_DIRECTORY: {UNREAL_REMOTE_CONTROL_MODULE_DIRECTORY}")
log.debug(f"    UNREAL_ROOT_DIRECTORY: {UNREAL_ROOT_DIRECTORY}")
log.debug(f"    UNREAL_MASTER_MATERIAL_DIRECTORY: {UNREAL_MASTER_MATERIAL_DIRECTORY}")
log.debug(f"    UNREAL_MATERIAL_LIBRARY_DIRECTORY: {UNREAL_MATERIAL_LIBRARY_DIRECTORY}")
log.debug(f"    BLENDER_ROOT_DIRECTORY: {BLENDER_ROOT_DIRECTORY}")
log.debug(f"    BLENDER_ASSET_LIBRARIES: {BLENDER_ASSET_LIBRARIES}")
log.debug(f"    BLENDER_MASTER_MATERIAL_LIBRARY_FILE_NAME: {BLENDER_MASTER_MATERIAL_LIBRARY_FILE_NAME}")
log.debug(f"    BLENDER_MASTER_MATERIAL_LIBRARY_FILE_PATH: {BLENDER_MASTER_MATERIAL_LIBRARY_FILE_PATH}")
log.debug(f"    BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE_NAME: {BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE}")
log.debug(f"    BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE_PATH: {BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE_PATH}")
log.debug(f"    MATERIAL_INSTANCE_CATALOG_ID: {MATERIAL_INSTANCE_CATALOG_ID}")
#log.debug(f"    MATERIAL_GLB_CACHE: {MATERIAL_GLB_CACHE}")
log.debug(f"    MATERIAL_PARAMETER_JSON_FILE_PATH: {MATERIAL_PARAMETER_JSON_FILE_PATH}")
log.debug(f"    MATERIAL_PARAMETER_LUT: {MATERIAL_PARAMETER_LUT}")
log.debug(f"    REMOTE_DEFAULT_RECEIVE_BUFFER_SIZE: {REMOTE_DEFAULT_RECEIVE_BUFFER_SIZE}")