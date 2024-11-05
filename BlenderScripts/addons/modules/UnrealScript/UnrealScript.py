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
import unreal
import os
import sys

#
blender_startup_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))), "startup")
#print("STARTUP DIRECTORY", blender_startup_directory)
#sys.path.append(blender_startup_directory)

from config import config as config

asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
mat_editor = unreal.MaterialEditingLibrary
static_mesh_editor = unreal.EditorStaticMeshLibrary


def get_material_instances(material):
    result_instances = []
    print(material)
    material_instances = mat_editor.get_child_instances(material)
    if len(material_instances) > 0:
        material_instances = list(map(lambda x: {"name": str(x.asset_name), "material": x.get_asset(), "package":x.package_name}, material_instances))
        result_instances = material_instances.copy()
        for material_instance in material_instances:
            sub_instances = get_material_instances(material_instance["material"])
            result_instances.extend(sub_instances)
    return result_instances


def get_data_asset_list(folder_path, recursive):
    return asset_reg.get_assets_by_path(folder_path, recursive=recursive, include_only_on_disk_assets=False)


def import_static_asset(source_file, destination_path, uasset_name="", auto=True, auto_generate_collision=True, should_save=True, replace_existing=True, import_textures=False, import_materials=False, material_search_location="UNDER_ROOT", reset_to_fbx_on_material_conflict=True, reorder_material_to_fbx_order=True, bake_pivot_in_vertex=True, combine_meshes=True, build_nanite=True, delete_fbx_after_import = False):
    """
        Import aa FBX in Unreal as a static mesh.
    """
    AssetImportTask = unreal.AssetImportTask()
    AssetImportTask.automated = auto
    AssetImportTask.destination_path = destination_path
    
    if uasset_name != "":
        AssetImportTask.destination_name = uasset_name
        AssetImportTask.filename = source_file
        AssetImportTask.replace_existing = True
        AssetImportTask.save = should_save
        
    if source_file.split(".")[-1].lower() == "fbx":
        # Import vertex color
        # unreal.FbxImportUI? or unreal.FbxStaticMeshImportData?
        # https://docs.unrealengine.com/5.2/en-US/PythonAPI/class/FbxImportUI.html
        fbx_import_ui = unreal.FbxImportUI()
        fbx_import_ui.import_textures = import_textures
        fbx_import_ui.import_materials  = import_materials
        fbx_import_ui.reset_to_fbx_on_material_conflict = reset_to_fbx_on_material_conflict
        
        static_mesh_import_data = unreal.FbxStaticMeshImportData()
        static_mesh_import_data.vertex_color_import_option = unreal.VertexColorImportOption.REPLACE
        static_mesh_import_data.bake_pivot_in_vertex = bake_pivot_in_vertex
        static_mesh_import_data.combine_meshes = combine_meshes
        static_mesh_import_data.build_nanite = build_nanite
        static_mesh_import_data.reorder_material_to_fbx_order = reorder_material_to_fbx_order
        static_mesh_import_data.auto_generate_collision = auto_generate_collision
        
        texture_import_data = unreal.FbxTextureImportData()
        
        if material_search_location == "UNDER_ROOT":
            material_search_location = unreal.MaterialSearchLocation.UNDER_ROOT
        elif material_search_location == "ALL_ASSETS":
            material_search_location = unreal.MaterialSearchLocation.ALL_ASSETS
        elif material_search_location == "DO_NOT_SEARCH":
            material_search_location = unreal.MaterialSearchLocation.DO_NOT_SEARCH
        elif material_search_location == "LOCAL":
            material_search_location = unreal.MaterialSearchLocation.LOCAL
        elif material_search_location == "UNDER_PARENT":
            material_search_location = unreal.MaterialSearchLocation.UNDER_PARENT
        texture_import_data.material_search_location = material_search_location
        
        fbx_import_ui.static_mesh_import_data = static_mesh_import_data
        fbx_import_ui.texture_import_data = texture_import_data
        
        AssetImportTask.options = fbx_import_ui
    
    asset_tools.import_asset_tasks([AssetImportTask])
    
    if delete_fbx_after_import is True:
        os.remove(source_file)


def import_skeletal_asset(source_file, destination_path, uasset_name, auto=True, should_save=True, replace_existing=True, import_textures=True, import_materials=False):
    """
        Import aa FBX in Unreal as a skeletal mesh.
    """
    AssetImportTask = unreal.AssetImportTask()
    AssetImportTask.automated = auto
    AssetImportTask.destination_path = destination_path
    
    if uasset_name != "":
        AssetImportTask.destination_name = uasset_name
        AssetImportTask.filename = source_file
        AssetImportTask.replace_existing = True
        AssetImportTask.save = should_save
        
    if source_file.split(".")[-1].lower() == "fbx":
        # Import vertex color
        # unreal.FbxImportUI? or unreal.FbxStaticMeshImportData?
        # https://docs.unrealengine.com/5.2/en-US/PythonAPI/class/FbxImportUI.html
        fbx_import_ui = unreal.FbxImportUI()
        fbx_import_ui.import_textures = import_textures
        fbx_import_ui.import_materials  = import_materials
        
        skeletal_mesh_import_data  = unreal.FbxSkeletalMeshImportData()
        
        fbx_import_ui.skeletal_mesh_import_data = skeletal_mesh_import_data
        
        AssetImportTask.options = fbx_import_ui
    
    asset_tools.import_asset_tasks([AssetImportTask])


def get_unreal_package_path(asset_path):
    return f"{asset_path}.{asset_path.split('/')[-1]}"


def get_data_asset(asset_path):
    return asset_reg.get_asset_by_object_path(get_unreal_package_path(asset_path))


def get_asset(asset_path):
    #return get_data_asset(asset_path).get_asset()
    return unreal.load_asset(asset_path)


def assign_material(static_mesh_path, material_path_list):
    asset = get_asset(static_mesh_path)
    for m in range(len(material_path_list)):
        material = get_asset(material_path_list[m])
        asset.set_material(m, material)


def create_physical_asset(destination_directory, phys_name):
    new_phys = get_asset(f"{destination_directory}{phys_name}.{phys_name}")
    
    if new_phys is None:
        phys_factory = unreal.PhysicsAssetFactory()
       
        new_phys = asset_tools.create_asset(asset_name=phys_name,
                                            package_path=destination_directory,
                                            asset_class=unreal.PhysicsAsset,
                                            factory=phys_factory)
    return new_phys

        
def create_data_table(destination_directory, dt_name, struct_path):
    table_asset = get_asset(f"{destination_directory}{dt_name}.{dt_name}")
    
    if table_asset is None:
        struct = get_asset(struct_path)
        
        data_table_factory = unreal.DataTableFactory()
        data_table_factory.struct = struct
        
        table_asset = asset_tools.create_asset(asset_name=dt_name,
                                            package_path=destination_directory,
                                            asset_class=unreal.DataTable,
                                            factory=data_table_factory)
    return table_asset


def fill_data_table_from_csv(data_table, csv_file_path):
    ret = unreal.DataTableFunctionLibrary.fill_data_table_from_csv_file(data_table, csv_file_path)
    save_asset(data_table.get_path_name())
    return ret


def create_and_fill_data_table(destination_directory, dt_name, struct_path, csv_path):
    dt = create_data_table(destination_directory, dt_name, struct_path)
    fill_data_table_from_csv(dt, csv_path)


def get_component_handles_from_asset(asset):
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    subobject_data_handles = subsystem.k2_gather_subobject_data_for_blueprint(asset)
    return subobject_data_handles


def get_components_from_asset(asset):
    components = []
    handles = get_component_handles_from_asset(asset)
    for handle in handles:
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        #object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
        object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object_for_blueprint(data, asset)
        components.append(object)
    return components


def get_component_from_asset_by_name(asset, name):
    components = get_components_from_asset(asset)
    for component in components:
        if name in component.get_name().replace('_GEN_VARIABLE', ''):
            return component


def get_component_from_asset_by_class(asset, cls):
    output = []
    components = get_components_from_asset(asset)
    for component in components:
        if component.__class__ == cls:
            output.append(component)
    return output


def get_bp_class(bp_asset):
    asset_gc = bp_asset.generated_class()
    return asset_gc


def create_blueprint_from_class(destination_directory, bp_name, cls):
    new_bp = get_asset(f"{destination_directory}{bp_name}.{bp_name}")
    if new_bp is None:
        bp_factory = unreal.BlueprintFactory()
        bp_factory.set_editor_property("parent_class", cls)
        
        new_bp = asset_tools.create_asset(asset_name=bp_name,
                                            package_path=destination_directory,
                                            asset_class=None,
                                            factory=bp_factory)
    return new_bp


def create_blueprint_from_parent(destination_directory, bp_name, bp_parent_path):
    bp_parent = get_asset(bp_parent_path)
    bp_parent_cls = get_bp_class(bp_parent)

    new_bp = create_blueprint_from_class(destination_directory, bp_name, bp_parent_cls)
    
    return new_bp


def create_animblueprint_from_class(destination_directory, bp_name, skeleton, cls):
    new_animbp = get_asset(f"{destination_directory}{bp_name}.{bp_name}")
    if new_animbp is None:
        animbp_factory = unreal.BlueprintFactory()
        animbp_factory.set_editor_property("parent_class", cls)
        animbp_factory.set_editor_property("target_skeleton ", skeleton)
        
        new_bp = asset_tools.create_asset(asset_name=bp_name,
                                            package_path=destination_directory,
                                            asset_class=None,
                                            factory=animbp_factory)
    return new_animbp


def save_directory(directory_path):
    return unreal.EditorAssetLibrary.save_directory(directory_path, only_if_is_dirty=True, recursive=True)
    

def save_asset(asset_path):
    return unreal.EditorAssetLibrary.save_asset(asset_path, only_if_is_dirty=True)


def rename_asset(asset_path, new_name):
    asset = get_asset(asset_path)
    path = asset_path.replace(asset_path.split("/")[-1], "")
    rename = [unreal.AssetRenameData(asset=asset, new_package_path=path, new_name=new_name)]
    return asset_tools.rename_assets(rename)


def copy_asset(source_asset_path, destination_asset_path):
    copy_asset = get_asset(destination_asset_path)
    if copy_asset is None:
        copy_asset = unreal.EditorAssetLibrary.duplicate_asset(source_asset_path, destination_asset_path)
    return copy_asset
 

def delete_asset(asset_path):
    unreal.EditorAssetLibrary.delete_asset(asset_path)


def uncheck_contribute_to_mass_on_convex_collision(asset_path):
    asset = get_asset(asset_path)
    body_setup = asset.get_editor_property("body_setup")
    agg_geom = body_setup.get_editor_property("agg_geom")
    convex_elems = agg_geom.get_editor_property("convex_elems")
    new_convex = []
    for e in convex_elems:
        new_convex.append(e.__copy__())
        new_convex[-1].set_editor_property("contribute_to_mass", False)
    agg_geom.set_editor_property("convex_elems", new_convex)
    body_setup.set_editor_property("agg_geom", agg_geom)
    asset.set_editor_property('body_setup', body_setup)
    
    
def export_to_gltf(asset_path, export_path):
    asset = get_asset(asset_path)
    export_options = unreal.GLTFExportOptions()
    unreal.GLTFExporter.export_to_gltf(asset, export_path, export_options, set())
    

def get_asset_system_path(asset_path):
    return unreal.SystemLibrary.get_system_path(get_asset(asset_path))


def get_source_file_pathes(asset_path):
    return get_asset(asset_path).get_editor_property("asset_import_data").extract_filenames()


def set_collision_preset(asset_path, collision_preset_name):
    asset = get_asset(asset_path)
    body_setup = asset.get_editor_property("body_setup")
    body_instance = body_setup.get_editor_property("default_instance")
    body_instance.set_editor_property("collision_profile_name", collision_preset_name)
    body_setup.set_editor_property("default_instance", body_instance)
    asset.set_editor_property('body_setup', body_setup)