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
bl_info = {
    "name": "UE Bridge",
    "author": "Paul Arnould",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "description": "",
}

#
import bpy
import os
import subprocess
#
import bridge.bridge_functions as bridge_functions
from . import unreal_cmd

import EU5_remote.EU5_remote as remote
import config.config as config


class VIEW3D_PT_UEBridge_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    panel_name = "UE Bridge Panel"
    bl_category = panel_name
    bl_label = panel_name

    def draw(self, context):
        row = self.layout.row()
        row.operator("uebridge.export", text="Export Selection")
        self.layout.separator()
        row = self.layout.row()
        row.operator("uebridge.add_box_collision", text="Add Box Collision")
        row = self.layout.row()
        row.operator("uebridge.add_sphere_collision", text="Add Sphere Collision")
        row = self.layout.row()
        row.operator("uebridge.add_convex_collision", text="Add Convex Collision")
        self.layout.separator()
        row = self.layout.row()
        row.operator("uebridge.refresh_materials", text="Refresh Material Library")


class VIEW3D_OT_add_box_collision(bpy.types.Operator):
    bl_idname = "uebridge.add_box_collision"
    bl_label = "Add Box Collision"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.view_layer.objects.active
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        for selected_object in selected_objects:
            bb = selected_object.bound_box
            x_min = bb[0][0]
            x_max = bb[6][0]
            y_min = bb[0][1]
            y_max = bb[6][1]
            z_min = bb[0][2]
            z_max = bb[6][2]
            bpy.ops.mesh.primitive_cube_add(location=((x_max+x_min)*0.5, (y_max+y_min)*0.5, (z_max+z_min)*0.5), scale=((x_max-x_min)*0.5, (y_max-y_min)*0.5, (z_max-z_min)*0.5))
            bpy.ops.object.transform_apply(scale=True)
            collision = bpy.context.active_object
            name = f"UBX_{selected_object.name}_"
            collision_count = 0
            for mesh in bpy.data.meshes:
                if name in mesh.name:
                    collision_count += 1
            collision.name = f"{name}{collision_count}"
            
            for collection in collision.users_collection:
                collection.objects.unlink(collision)
            
            for collection in selected_object.users_collection:
                collection.objects.link(collision)
            
            collision.parent = selected_object.parent
            
            # Display collision as Wire
            bpy.context.object.display_type = 'WIRE'
        
        # Reselect all  
        for selected_object in selected_objects:
            selected_object.select_set(True)
        # Reset active
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class VIEW3D_OT_add_sphere_collision(bpy.types.Operator):
    bl_idname = "uebridge.add_sphere_collision"
    bl_label = "Add Sphere Collision"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.view_layer.objects.active
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        for selected_object in selected_objects:
            bb = selected_object.bound_box
            x_min = bb[0][0]
            x_max = bb[6][0]
            y_min = bb[0][1]
            y_max = bb[6][1]
            z_min = bb[0][2]
            z_max = bb[6][2]
            bpy.ops.mesh.primitive_ico_sphere_add(radius=max((x_max-x_min)*0.5, (y_max-y_min)*0.5, (z_max-z_min)*0.5), align='WORLD', location=((x_max+x_min)*0.5, (y_max+y_min)*0.5, (z_max+z_min)*0.5), scale=(1.0, 1.0, 1.0))
            bpy.ops.object.transform_apply(scale=True)
            collision = bpy.context.active_object
            name = f"USP_{selected_object.name}_"
            collision_count = 0
            for mesh in bpy.data.meshes:
                if name in mesh.name:
                    collision_count += 1
            collision.name = f"{name}{collision_count}"
            
            for collection in collision.users_collection:
                collection.objects.unlink(collision)
            
            for collection in selected_object.users_collection:
                collection.objects.link(collision)
            
            collision.parent = selected_object.parent
            
            # Display collision as Wire
            bpy.context.object.display_type = 'WIRE'
        
        # Reselect all  
        for selected_object in selected_objects:
            selected_object.select_set(True)
        # Reset active
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class VIEW3D_OT_add_capsule_collision(bpy.types.Operator):
    bl_idname = "uebridge.add_box_collision"
    bl_label = "Add Box Collision"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.view_layer.objects.active
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        for selected_object in selected_objects:
            bb = selected_object.bound_box
            x_min = bb[0][0]
            x_max = bb[6][0]
            y_min = bb[0][1]
            y_max = bb[6][1]
            z_min = bb[0][2]
            z_max = bb[6][2]
            bpy.ops.mesh.primitive_cube_add(location=((x_max+x_min)*0.5, (y_max+y_min)*0.5, (z_max+z_min)*0.5), scale=((x_max-x_min)*0.5, (y_max-y_min)*0.5, (z_max-z_min)*0.5))
            bpy.ops.object.transform_apply(scale=True)
            collision = bpy.context.active_object
            name = f"UBX_{selected_object.name}_"
            collision_count = 0
            for mesh in bpy.data.meshes:
                if name in mesh.name:
                    collision_count += 1
            collision.name = f"{name}{collision_count}"
            
            for collection in collision.users_collection:
                collection.objects.unlink(collision)
            
            for collection in selected_object.users_collection:
                collection.objects.link(collision)
            
            collision.parent = selected_object
            
            # Display collision as Wire
            bpy.context.object.display_type = 'WIRE'
        
        # Reselect all  
        for selected_object in selected_objects:
            selected_object.select_set(True)
        # Reset active
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class VIEW3D_OT_add_convex_collision(bpy.types.Operator):
    bl_idname = "uebridge.add_convex_collision"
    bl_label = "Add Convex Collision"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.view_layer.objects.active
        
        bpy.ops.object.select_all(action='DESELECT')
        for selected_object in selected_objects:
            bpy.ops.object.select_all(action='DESELECT')
            collision = selected_object.copy()
            collision.data = selected_object.data.copy()
            bpy.data.scenes['Scene'].collection.objects.link(collision)
            
            bpy.context.view_layer.objects.active = collision
            for modifier in collision.modifiers:
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.convex_hull()
            bpy.ops.object.mode_set(mode='OBJECT')
        
            name = f"UCX_{selected_object.name}_"
            collision_count = 0
            for mesh in bpy.data.meshes:
                if name in mesh.name:
                    collision_count += 1
            collision.name = f"{name}{collision_count}"
            
            for collection in collision.users_collection:
                collection.objects.unlink(collision)
            
            for collection in selected_object.users_collection:
                collection.objects.link(collision)
            
            collision.parent = selected_object.parent
            
            # Display collision as Wire
            bpy.context.object.display_type = 'WIRE'
        
        # Reselect all  
        for selected_object in selected_objects:
            selected_object.select_set(True)
        # Reset active
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}


class VIEW3D_OT_export_to_unreal(bpy.types.Operator):
    bl_idname = "uebridge.export"
    bl_label = "Export to UE"

    def execute(self, context):
        try:
            bpy.ops.wm.save_mainfile()
        except:
            self.report({"ERROR"}, "Error: Could not save blend file. Check your source control if any.")
            return {'CANCELLED'}
    
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.view_layer.objects.active
        file_list = []
        fbx_file_list = []
        object_name_list = []
        export_success = True
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        for selected_object in selected_objects:
            if selected_object.type == "EMPTY" and selected_object.parent is None:
                children = selected_object.children
                
                meshes = []
                box_collisions = []
                sphere_collisions = []
                capsule_collisions = []
                convex_collisions = []
                sockets = []
                is_there_collision = False
                
                for child in children:
                    if child.type == "MESH":
                        if child.name[:4] == "UBX_":
                            box_collisions.append(child)
                            is_there_collision = True
                        elif child.name[:4] == "USP_":
                            sphere_collisions.append(child)
                            is_there_collision = True
                        elif child.name[:4] == "UCP_":
                            capsule_collisions.append(child)
                            is_there_collision = True
                        elif child.name[:4] == "UCX_":
                            convex_collisions.append(child)
                            is_there_collision = True
                        else:
                            meshes.append(child)
                    if child.type == "EMPTY":
                        if child.name[:7] == "Socket_":
                            sockets.append(child)
                
                
                # 
                pivot_location = selected_object.location.copy()
                pivot_name_backup = selected_object.name
                pivot_name = f"SM_{selected_object.name}"
                
                selected_object.name = "on_export"
                selected_object.location[0] = 0
                selected_object.location[1] = 0
                selected_object.location[2] = 0
                
                # Join meshes
                meshes_copy = []
                for mesh_to_copy in meshes:
                    copy = mesh_to_copy.copy()
                    copy.data = mesh_to_copy.data.copy()
                    bpy.data.scenes['Scene'].collection.objects.link(copy)
                    meshes_copy.append(copy)
                    
                    bpy.context.view_layer.objects.active = copy
                    for modifier in copy.modifiers:
                        bpy.ops.object.modifier_apply(modifier=modifier.name)
                
                bpy.ops.object.select_all(action='DESELECT')
                for mesh in meshes_copy:
                    mesh.select_set(True)
                bpy.context.view_layer.objects.active = meshes_copy[0]
                
                bpy.ops.object.join()
                joined_meshes = bpy.context.view_layer.objects.active
                joined_meshes.name = pivot_name
                
                # Rename Collisions
                i = 0
                box_collisions_copy = []
                for col in box_collisions:
                    copy = col.copy()
                    bpy.data.scenes['Scene'].collection.objects.link(copy)
                    copy.name = f"UCX_{pivot_name}_{i}"
                    box_collisions_copy.append(copy)
                    i = i+1
                i = 0
                sphere_collisions_copy = []
                for col in sphere_collisions:
                    copy = col.copy()
                    bpy.data.scenes['Scene'].collection.objects.link(copy)
                    copy.name = f"USP_{pivot_name}_{i}"
                    sphere_collisions_copy.append(copy)
                    i = i+1
                i = 0
                capsule_collisions_copy = []    
                for col in capsule_collisions:
                    copy = col.copy()
                    bpy.data.scenes['Scene'].collection.objects.link(copy)
                    copy.name = f"USX_{pivot_name}_{i}"
                    capsule_collisions_copy.append(copy)
                    i = i+1
                i = 0
                convex_collisions_copy = []    
                for col in convex_collisions:
                    copy = col.copy()
                    bpy.data.scenes['Scene'].collection.objects.link(copy)
                    copy.name = f"UCX_{pivot_name}_{i}"
                    convex_collisions_copy.append(copy)
                    i = i+1
                
                # Select all
                bpy.ops.object.select_all(action='DESELECT')
                joined_meshes.select_set(True)
                for obj in box_collisions_copy:
                    obj.select_set(True)
                for obj in sphere_collisions_copy:
                    obj.select_set(True)
                for obj in capsule_collisions_copy:
                    obj.select_set(True)
                for obj in convex_collisions_copy:
                    obj.select_set(True)
                for obj in sockets:
                    obj.scale[0] = obj.scale[0]*0.01
                    obj.scale[1] = obj.scale[1]*0.01
                    obj.scale[2] = obj.scale[2]*0.01
                    obj.select_set(True)
                
                export_path = bpy.path.abspath(f"//{pivot_name}.fbx")
                bpy.ops.export_scene.fbx(filepath=export_path, use_selection=True, axis_up='Z', bake_anim=False)
                
                # Import fbx in Unreal
                unreal_directory = bridge_functions.get_UE_directory_from_blend()
                
                obj_export_success = unreal_cmd.import_fbx(export_path, unreal_directory, pivot_name, auto_generate_collision=False)
                
                if obj_export_success is not False:
                    if is_there_collision is False:
                        unreal_cmd.set_no_collision_preset(f"{unreal_directory}{pivot_name}")
                    else:
                        unreal_cmd.set_block_all_preset(f"{unreal_directory}{pivot_name}")
                else:
                    export_success = obj_export_success
                
                bpy.ops.object.select_all(action='DESELECT')
                joined_meshes.select_set(True)
                for obj in box_collisions_copy:
                    obj.select_set(True)
                for obj in sphere_collisions_copy:
                    obj.select_set(True)
                for obj in capsule_collisions_copy:
                    obj.select_set(True)
                for obj in convex_collisions_copy:
                    obj.select_set(True)
                bpy.ops.object.delete()
                for obj in sockets:
                    obj.scale[0] = obj.scale[0]*100
                    obj.scale[1] = obj.scale[1]*100
                    obj.scale[2] = obj.scale[2]*100
                
                selected_object.location = pivot_location
                selected_object.name = pivot_name_backup
        
        # Reselect all  
        bpy.ops.object.select_all(action='DESELECT')
        for selected_object in selected_objects:
            selected_object.select_set(True)
        # Reset active
        bpy.context.view_layer.objects.active = active_object
        
        if export_success is False:
            self.report({"ERROR"}, """Failed to export to Unreal.
Check that Unreal is running. If it is, please restart Unreal and Blender.""")
            return {'CANCELLED'}
        
        return {'FINISHED'}
        """        
                # Copy collision meshes
                collisions_copy = []
                i = 0
                for col in collision_body:
                    copy = col.copy()
                    bpy.data.scenes['Scene'].collection.objects.link(copy)
                    copy.name = f"UCX_{mesh.name}_{i}"
                    collisions_copy.append(copy)
                    i = i+1     
                

        # Select, export, deselect
        for selected_object in selected_objects:
            split_name = selected_object.name.split("_")
            prefix = split_name[0]
            if prefix == "UBX" or prefix == "UCP" or prefix == "USP" or prefix == "UCX":
                pass
            else:
                selected_object.select_set(True)
                selected_object_name = f"SM_{selected_object.name}"
                export_path = bpy.path.abspath(f"//{selected_object_name}.fbx")
                prev_location = selected_object.location.copy()
                selected_object.location[0] = 0
                selected_object.location[1] = 0
                selected_object.location[2] = 0
                
                collisions = False
                for child in selected_object.children:
                    split_name = child.name.split("_")
                    prefix = split_name[0]
                    if prefix == "UBX" or prefix == "UCP" or prefix == "USP" or prefix == "UCX":
                        child.select_set(True)
                        collisions = True
                bpy.ops.export_scene.fbx(filepath = export_path, use_selection=True, axis_up='Z')
                selected_object.location = prev_location
                bpy.ops.object.select_all(action='DESELECT')
                
                # Import fbx in Unreal
                unreal_directory = bridge_functions.get_UE_directory_from_blend()
                unreal_cmd.import_fbx(export_path, unreal_directory, selected_object_name, auto_generate_collision=False)
                
                if collisions is False:
                    unreal_cmd.set_no_collision_preset(f"{unreal_directory}{selected_object_name}")
                else:
                    unreal_cmd.set_block_all_preset(f"{unreal_directory}{selected_object_name}")
                    
                os.remove(export_path)

        # Reselect all  
        for selected_object in selected_objects:
            selected_object.select_set(True)
        # Reset active
        bpy.context.view_layer.objects.active = active_object

        return {'FINISHED'}
"""


class VIEW3D_OT_refresh_materials(bpy.types.Operator):
    bl_idname = "uebridge.refresh_materials"
    bl_label = "Refresh Materials"
    
    def execute(self, context):
        unreal_cmd.export_material_json()
        refresh_script = os.path.normpath(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(remote.__file__))), "refresh_materials"), "refresh_materials.py"))
        subprocess.Popen(["blender", "--background", config.BLENDER_MATERIAL_INSTANCE_LIBRARY_FILE_PATH, "--python", refresh_script])
        return {'FINISHED'}


class ASSET_OT_assign_material(bpy.types.Operator):
    bl_idname = "asset.assign_material"
    bl_label = "Assgin Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        asset = context.asset
        
        materials = []
        mesh_name = ""
        with bpy.data.libraries.load(asset.full_library_path, assets_only=True, link=True) as (data_from, data_to):
            data_to.materials = data_from.materials.copy()
            materials = data_from.materials.copy()
            if len(data_from.objects) > 0:
                for asset_name in data_from.objects:
                    if asset_name == asset.name:
                        data_to.objects = [asset_name]
                        mesh_name = asset_name
        
        selected_objects = bpy.context.selected_objects
        
        if mesh_name != "":
            _mesh = data_to.objects[0]
            _material_slots = _mesh.material_slots
            for obj in selected_objects:
                if obj.type == "MESH":
                    with bpy.context.temp_override(selected_objects=[obj], object=obj, active_object=obj):
                        
                        if len(_material_slots) < len(obj.material_slots):
                            for m in range(len(obj.material_slots))[len(_material_slots):]:
                                bpy.active_material_index = m
                                bpy.ops.object.material_slot_remove()
                        
                        
                        for m in range(len(_material_slots)):
                            if m < len(obj.material_slots):
                                obj.material_slots[m].material = _material_slots[m].material
                            else:
                                obj.data.materials.append(_material_slots[m].material)
                        
        elif len(materials)>0:
            _material = data_to.materials[0]
            for obj in selected_objects:
                obj.data.materials.clear()
                obj.data.materials.append(_material)
            
        return {'FINISHED'}
    

def assign_asset_material_function(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'

    layout.separator()
    layout.operator("asset.assign_material", text = 'Assign Material')
    layout.separator()


def register():
    bpy.utils.register_class(VIEW3D_OT_export_to_unreal)
    bpy.utils.register_class(VIEW3D_OT_refresh_materials)
    bpy.utils.register_class(VIEW3D_PT_UEBridge_panel)
    bpy.utils.register_class(VIEW3D_OT_add_box_collision)
    bpy.utils.register_class(VIEW3D_OT_add_sphere_collision)
    bpy.utils.register_class(VIEW3D_OT_add_convex_collision)
    bpy.utils.register_class(ASSET_OT_assign_material)
    
    bpy.types.Object.auto_generate_collision = bpy.props.IntProperty()
    
    bpy.types.ASSETBROWSER_MT_context_menu.append(assign_asset_material_function)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_export_to_unreal)
    bpy.utils.unregister_class(VIEW3D_OT_refresh_materials)
    bpy.utils.unregister_class(VIEW3D_PT_UEBridge_panel)
    bpy.utils.unregister_class(VIEW3D_OT_add_box_collision)
    bpy.utils.unregister_class(VIEW3D_OT_add_sphere_collision)
    bpy.utils.unregister_class(VIEW3D_OT_add_convex_collision)
    bpy.utils.unregister_class(ASSET_OT_assign_material)
    
    del bpy.types.Object.auto_generate_collision
    
    bpy.types.ASSETBROWSER_MT_context_menu.remove(assign_asset_material_function)