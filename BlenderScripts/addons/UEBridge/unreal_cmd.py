import EU5_remote.EU5_remote as remote
import bridge.bridge_functions as bridge_functions
import config.config as config
import os


def import_fbx(export_path, unreal_directory, name, *args, **kwargs):
    try:
        ret = remote.execute_python_function("UnrealScript.UnrealScript", "import_static_asset", export_path, unreal_directory, name, *args, delete_fbx_after_import=True, **kwargs)
        return ret
    except:
        return False


def set_no_collision_preset(asset_path):
    command = f"""from UnrealScript import UnrealScript

UnrealScript.set_collision_preset("{asset_path}", 'NoCollision')
UnrealScript.save_asset("{asset_path}")"""

    ret = remote.execute_python_script(command)
    return ret


def set_block_all_preset(asset_path):
    command = f"""from UnrealScript import UnrealScript

UnrealScript.set_collision_preset("{asset_path}", 'BlockAll')
UnrealScript.save_asset("{asset_path}")"""

    ret = remote.execute_python_script(command)
    return ret
    
    
def export_material_json():
    command = """import json
    
from UnrealScript import UnrealScript
import config.config as config
    
material_dict = {}

assets = UnrealScript.asset_reg.get_assets_by_path(config.UNREAL_MASTER_MATERIAL_DIRECTORY, recursive=True)
print(config.UNREAL_MASTER_MATERIAL_DIRECTORY)
print(assets)
for asset_data in assets:
    material_name = str(asset_data.asset_name)
    material = unreal.AssetRegistryHelpers.get_asset(asset_data)
    print(material)
    if material.__class__ == unreal.Material:
        material_instances = UnrealScript.get_material_instances(material)
        material_dict[material_name] = {}

        for material_instance in material_instances:
            package_name = str(material_instance["package"])
            if config.UNREAL_MATERIAL_LIBRARY_DIRECTORY in package_name:
                mat_editor = UnrealScript.mat_editor
            
                scalars = mat_editor.get_scalar_parameter_names(material_instance["material"])
                scalars = list(map(lambda x: {"name": str(x), "value": mat_editor.get_material_instance_scalar_parameter_value(material_instance["material"], x)}, scalars))

                def vector_dict(vector_parameter_name):
                    linear_color = mat_editor.get_material_instance_vector_parameter_value(material_instance["material"], vector_parameter_name)
                    return {"name": str(vector_parameter_name), "value":  (linear_color.r, linear_color.g, linear_color.b)}

                vectors = mat_editor.get_vector_parameter_names(material_instance["material"])
                vectors = list(map(vector_dict, vectors))

                def texture_dict(texture_parameter_name):
                    print(texture_parameter_name)
                    texture = mat_editor.get_material_instance_texture_parameter_value(material_instance["material"], texture_parameter_name)
                    if texture is None:
                        return {"name": str(texture_parameter_name), "value":  "None", "value2":  "None", }
                    print(UnrealScript.get_source_file_pathes(texture.get_path_name()))
                    source_file_path = UnrealScript.get_source_file_pathes(texture.get_path_name())
                    if len(source_file_path) > 0:
                        return {"name": str(texture_parameter_name), "value":  texture.get_path_name(), "value2":  source_file_path[0], }
                    else:
                        return {"name": str(texture_parameter_name), "value":  texture.get_path_name()}
                    

                textures = mat_editor.get_texture_parameter_names(material_instance["material"])
                textures = list(map(texture_dict, textures))

                static_switches = mat_editor.get_static_switch_parameter_names(material_instance["material"])
                static_switches = list(map(lambda x: {"name": str(x), "value": mat_editor.get_material_instance_static_switch_parameter_value(material_instance["material"], x)}, static_switches))

                material_dict[material_name][material_instance["name"]] = {"Scalars": scalars, "Vectors": vectors, "Textures": textures, "Static_switches": static_switches, "Package": package_name}

with open(config.MATERIAL_PARAMETER_JSON_FILE_PATH, 'w') as f:
    json.dump(material_dict, f, indent=4)"""
    
    ret = remote.execute_python_script(command)
    return ret

