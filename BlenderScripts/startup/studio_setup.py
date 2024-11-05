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
import sys
import os
import bpy
# 
import config.config as config
from logger.logger import log

def set_up_preferences_asset_libraries():
    log.info("Setting up Libraries...")
    studio_libraries = config.BLENDER_ASSET_LIBRARIES
    for library_name in studio_libraries:
        library_path = studio_libraries[library_name]
        library_default_name = os.path.basename(library_path)
        log.debug(f"Setting up Library {library_name} at {library_path}")

        if library_name in bpy.context.preferences.filepaths.asset_libraries:
            bpy.context.preferences.filepaths.asset_libraries[library_name].path = library_path
            bpy.context.preferences.filepaths.asset_libraries[library_name].import_method = "LINK"
        else:
            bpy.ops.preferences.asset_library_add(directory=library_path)
            bpy.context.preferences.filepaths.asset_libraries[library_default_name].name = library_name
            bpy.context.preferences.filepaths.asset_libraries[library_name].import_method = "LINK"


# Use an handler to defer the ops, as Blender refuse to use ops on startup
@bpy.app.handlers.persistent
def set_up_preferences_handler(dummy):
    set_up_preferences_asset_libraries()

def register():
    bpy.app.handlers.load_post.append(set_up_preferences_handler)

def unregister():
    pass
