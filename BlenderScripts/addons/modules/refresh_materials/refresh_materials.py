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
import bpy
import json
import time
import os
import uuid
#
import config.config as config
from logger.logger import log


def read_unreal_material_parameters():
    f = open(config.MATERIAL_PARAMETER_JSON_FILE_PATH)
    material_parameters_dict = json.load(f)
    return material_parameters_dict


def delete_all_material():
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)


def create_material_instances():
    material_parameters_dict = read_unreal_material_parameters()
    master_material_to_transfer = []
    # Load master material library and transfer
    with bpy.data.libraries.load(config.BLENDER_MASTER_MATERIAL_LIBRARY_FILE_PATH, assets_only=True, link=True) as (data_from, data_to):
        for master_material_name in material_parameters_dict:
            if master_material_name in data_from.materials:
                master_material_to_transfer.append(master_material_name)
        data_to.materials = master_material_to_transfer.copy()

    asset_cat_file_path = os.path.join(os.path.dirname(config.BLENDER_MASTER_MATERIAL_LIBRARY_FILE_PATH), "blender_assets.cats.txt")
    content = ""
    cat = {}
    new_cat = {}
    all_cat = {}
    with open(asset_cat_file_path, "r") as asset_cat_file:
        for line in asset_cat_file:
            if line.startswith("#") or line.isspace() or line.startswith("VERSION"):
                content += line
            elif len(line.split(":")) == 3:
                line_split = line.split(":")
                content += line
                cat[line_split[1]] = line_split[0]
                all_cat[line_split[1]] = line_split[0]
        
    for master_material_name in master_material_to_transfer:
        for material_instance_name in material_parameters_dict[master_material_name]:
            package_name = material_parameters_dict[master_material_name][material_instance_name]["Package"]
            bl_cat = package_name.replace(config.UNREAL_MATERIAL_LIBRARY_DIRECTORY, "MaterialInstance/")
            bl_cat = bl_cat.replace(f"/{bl_cat.split('/')[-1]}", "")
            if bl_cat not in cat:
                cat_uuid = str(uuid.uuid4())
                new_cat[bl_cat] = cat_uuid
                all_cat[bl_cat] = cat_uuid
            
    with open(asset_cat_file_path, "w") as asset_cat_file_out:
        asset_cat_file_out.write(content)
        for bl_cat in new_cat:
            asset_cat_file_out.write(f"{new_cat[bl_cat]}:{bl_cat}:{bl_cat.replace('/', '-')}\n")
            

    for master_material_name in master_material_to_transfer:
        for material_instance_name in material_parameters_dict[master_material_name]:
            new_mat_instance = bpy.data.materials[master_material_name].copy()
            new_mat_instance.name = material_instance_name
            new_mat_instance["ue_package_name"] = material_parameters_dict[master_material_name][material_instance_name]["Package"]
            # Set node values
            for node in new_mat_instance.node_tree.nodes:
                for parameter_type in material_parameters_dict[master_material_name][material_instance_name]:
                    if parameter_type == "Vectors" or parameter_type == "Textures" or parameter_type == "Static_switches" or parameter_type == "Scalars":
                        for unreal_material_parameter in material_parameters_dict[master_material_name][material_instance_name][parameter_type]:
                            if parameter_type == "Textures":
                                value = [unreal_material_parameter["value"], unreal_material_parameter["value2"]]
                            else:
                                value = unreal_material_parameter["value"]
                            if node.label == unreal_material_parameter["name"]:
                                set_material_parameters(node, parameter_type, value)
                            elif node.label in config.MATERIAL_PARAMETER_LUT:
                                if config.MATERIAL_PARAMETER_LUT[node.label] == unreal_material_parameter["name"]:
                                    set_material_parameters(node, parameter_type, value)
                                        
            new_mat_instance.asset_mark()
            new_mat_instance.asset_generate_preview()
            bl_cat = new_mat_instance["ue_package_name"].replace(config.UNREAL_MATERIAL_LIBRARY_DIRECTORY, "MaterialInstance/")
            bl_cat = bl_cat.replace(f"/{bl_cat.split('/')[-1]}", "")
            new_mat_instance.asset_data.catalog_id = all_cat[bl_cat]
            #new_mat_instance.asset_data.catalog_id = config.MATERIAL_INSTANCE_CATALOG_ID


def set_material_parameters(node, parameter_type, value):
    if parameter_type == "Vectors":
        node.inputs[0].default_value = value[0]
        node.inputs[1].default_value = value[1]
        node.inputs[2].default_value = value[2]
    elif parameter_type == "Scalars":
        node.outputs[0].default_value = value
    elif parameter_type == "Textures":
        #value = value.replace(config.UNREAL_ROOT_DIRECTORY, f"{config.RAW_DATA_ROOT_DIRECTORY}/")
        #value = f"{value[:value.find('.')]}.png"
        #value = os.path.normpath(value)

        previous_colorspace = node.image.colorspace_settings.name
        #print("PREV", previous_colorspace)
        try:
            texture = bpy.data.images.load(os.path.normpath(value[1]))
            node.image = texture
            node.image.colorspace_settings.name = previous_colorspace
            #print(node.image.colorspace_settings.name)
        except:
            try:
                value[0] = value[0].replace(config.UNREAL_ROOT_DIRECTORY, f"{config.RAW_DATA_ROOT_DIRECTORY}/")
                value[0] = f"{value[0][:value[0].find('.')]}.png"
                value[0] = os.path.normpath(value[0])
            except:
                print(f"Could not load texture {value}")


def save():
    bpy.ops.wm.save_mainfile()


def quit():
    bpy.ops.wm.quit_blender()


delete_all_material()
create_material_instances()
save()