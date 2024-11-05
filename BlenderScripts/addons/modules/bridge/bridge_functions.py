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
import os
import re
#
import bpy
#
import config.config as config


def get_UE_directory_from_blend():
    local_path = bpy.path.abspath("//")
    destination_path = os_raw_data_path_to_unreal_path(local_path)
    return destination_path
    

def os_raw_data_path_to_unreal_path(os_path):
    rel_path = re.compile(re.escape(config.RAW_DATA_ROOT_DIRECTORY), re.IGNORECASE)
    rel_path = rel_path.sub("", os_path)
    
    folder_tree = rel_path.split(os.sep)
    unreal_path = config.UNREAL_ROOT_DIRECTORY
    for folder in folder_tree[:-1]:
            if folder != "":
                unreal_path += f"{folder}/"
    return unreal_path
    
    
def unreal_path_to_os_path(unreal_path):
    rel_path = re.compile(re.escape(config.UNREAL_ROOT_DIRECTORY), re.IGNORECASE)
    rel_path = rel_path.sub("", unreal_path)
    
    folder_tree = rel_path.split("/")
    os_path = config.RAW_DATA_ROOT_DIRECTORY
    for folder in folder_tree:
            if folder != "":
                os_path = os.path.join(os_path, folder)
    return os_path