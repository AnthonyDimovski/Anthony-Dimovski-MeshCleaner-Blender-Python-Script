bl_info = {
    "name": "Cleanup Utilities",
    "author": "Anthony Dimovski",
    "version": (1, 0),
    "blender": (4, 0, 1),
    "category": "Tool"
}

import bpy

class ObjectNameToMeshNameOperator(bpy.types.Operator):
    bl_idname = "object.objname_to_meshname"
    bl_label = "Obj Name to Data Name"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Converts the object name into the data mesh name for parity"

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data.name = obj.name

        self.report({'INFO'}, 'Object Name to Mesh Name executed successfully')
        return {'FINISHED'}

class OBJECT_OT_remove_all_vertex_groups(bpy.types.Operator):
    bl_idname = "object.remove_all_vertex_groups"
    bl_label = "Remove All Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Removes Vertex Groups"

    def execute(self, context):
        # Use a list comprehension to filter only mesh objects
        mesh_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

        # Remove all vertex groups from the filtered mesh objects
        for obj in mesh_objects:
            for vertex_group in obj.vertex_groups:
                obj.vertex_groups.remove(vertex_group)

        return {'FINISHED'}

class OBJECT_OT_remove_all_shape_keys(bpy.types.Operator):
    bl_idname = "object.remove_all_shape_keys"
    bl_label = "Remove All Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Removes Shape Keys"

    def execute(self, context):
        # Iterate over all selected objects
        for obj in bpy.context.selected_objects:
            # Check if the object is a mesh and has shape keys
            if obj.type == 'MESH' and obj.data.shape_keys:
                # Remove all shape keys
                for shape_key in obj.data.shape_keys.key_blocks:
                    obj.shape_key_remove(shape_key)

        return {'FINISHED'}
    
class OBJECT_OT_remove_all_color_attributes(bpy.types.Operator):
    bl_idname = "object.remove_all_color_attributes"
    bl_label = "Remove All Color Attributes"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Removes Color Attributes and Vertex Colors"

    def execute(self, context):
        # Iterate over all selected objects
        for obj in bpy.context.selected_objects:
            # Check if the object is a mesh
            if obj.type == 'MESH':
                # Set the object as active
                bpy.context.view_layer.objects.active = obj

                # Remove all color attributes
                for color_attribute in reversed(obj.data.color_attributes):
                    bpy.ops.geometry.color_attribute_remove()

        return {'FINISHED'}

class OBJECT_OT_remove_unused_material_slots(bpy.types.Operator):
    bl_idname = "object.remove_unused_material_slots"
    bl_label = "Remove Unused Material Slots"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Removes unused material slots"

    def execute(self, context):
        # Iterate over all selected objects
        for obj in bpy.context.selected_objects:
            # Check if the object is a mesh
            if obj.type == 'MESH':
                # Remove all unused material slots
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.material_slot_remove_unused()

        return {'FINISHED'}

class ExecuteAllOperatorsOperator(bpy.types.Operator):
    bl_idname = "object.execute_all_operators"
    bl_label = "Execute All Above Operators"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Excecutes all above operations"
    
    def execute(self, context):
        bpy.ops.object.objname_to_meshname()
        bpy.ops.object.remove_all_vertex_groups()
        bpy.ops.object.remove_all_shape_keys()
        bpy.ops.object.remove_all_color_attributes()
        bpy.ops.object.remove_unused_material_slots()
        
        self.report({'INFO'}, 'All operators executed successfully')
        return {'FINISHED'}




class OBJECT_OT_remove_custom_properties(bpy.types.Operator):
    bl_idname = "object.remove_custom_properties"
    bl_label = "Remove Custom Properties"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Removes all Custom Properties that are NOT EQUAL TO 'UDP3DSMAX'"

    def execute(self, context):
        # Specify the name of the custom property to keep
        property_to_keep = "UDP3DSMAX"

        # Iterate over all selected objects
        for obj in bpy.context.selected_objects:
            # Create a list of custom properties to remove
            properties_to_remove = [prop_name for prop_name in obj.keys() if prop_name != property_to_keep]

            # Iterate over the list and remove the custom properties
            for prop_name in properties_to_remove:
                del obj[prop_name]

        return {'FINISHED'}

class OBJECT_OT_Add_Custom_Property(bpy.types.Operator):
    bl_idname = "object.add_custom_property"
    bl_label = "Add Custom Property"
    bl_description = "Adds a 'UDP3DSMAX' string custom property"
    
    def execute(self, context):
        # Specify the name of the custom property
        property_name = "UDP3DSMAX"
        default_value = ""
        
        # Iterate through all selected objects
        for obj in bpy.context.selected_objects:
            # Add the string custom property to each selected object
            obj[property_name] = default_value
        
        return {'FINISHED'}
    
class OBJECT_OT_Remove_UDP3DSMAX_Property(bpy.types.Operator):
    bl_idname = "object.remove_udp3dsmax_property"
    bl_label = "Remove Custom Property"
    bl_description = "Removes the 'UDP3DSMAX' string custom property"
    
    def execute(self, context):
        # Specify the name of the custom property
        property_name = "UDP3DSMAX"
        
        # Iterate through all selected objects
        for obj in bpy.context.selected_objects:
            # Check if the property exists before removing
            if property_name in obj:
                del obj[property_name]
        
        return {'FINISHED'}

class VIEW3D_PT_CleanupUtilities(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_label = "Cleanup Utilities"
    
    def draw(self, context):
        """Define the layout of the panel"""

        row = self.layout.row()
        row.operator("object.objname_to_meshname", text="Obj Name -> Data Name", icon='MESH_DATA')
        
        row = self.layout.row()
        row.operator("object.remove_all_vertex_groups", text="Remove Vertex Groups", icon='GROUP_VERTEX')

        row = self.layout.row()
        row.operator("object.remove_all_shape_keys", text="Remove Shape Keys", icon='SHAPEKEY_DATA')

        row = self.layout.row()
        row.operator("object.remove_all_color_attributes", text="Remove Color Attributes", icon='COLOR')

        row = self.layout.row()
        row.operator("object.remove_unused_material_slots", text="Remove Unused Material Slots", icon='MATERIAL')
        
        row = self.layout.row()
        row.operator("object.execute_all_operators", text="Execute All Above Operations", icon='ERROR')

        # UDP3DSMAX section
        self.layout.separator(factor=1.0,)
        row = self.layout.row(align=True)
        row.label(text="UDP3DSMAX")

        row = self.layout.row()
        row.operator("object.remove_custom_properties", text="!= UDP3DSMAX")
        
        row = self.layout.row()
        row.operator("object.add_custom_property", text="Add UDP3DSMAX")
        
        row = self.layout.row()
        row.operator("object.remove_udp3dsmax_property", text="Remove UDP3DSMAX")


def register():
    bpy.utils.register_class(ObjectNameToMeshNameOperator)
    bpy.utils.register_class(OBJECT_OT_remove_all_vertex_groups)
    bpy.utils.register_class(OBJECT_OT_remove_all_shape_keys)
    bpy.utils.register_class(OBJECT_OT_remove_all_color_attributes)
    bpy.utils.register_class(OBJECT_OT_remove_unused_material_slots)
    bpy.utils.register_class(ExecuteAllOperatorsOperator)
    
    # UDP3DSMAX section
    bpy.utils.register_class(OBJECT_OT_remove_custom_properties)
    bpy.utils.register_class(OBJECT_OT_Add_Custom_Property)
    bpy.utils.register_class(OBJECT_OT_Remove_UDP3DSMAX_Property)
    bpy.utils.register_class(VIEW3D_PT_CleanupUtilities)

def unregister():
    bpy.utils.unregister_class(ObjectNameToMeshNameOperator)
    bpy.utils.unregister_class(OBJECT_OT_remove_all_vertex_groups)
    bpy.utils.unregister_class(OBJECT_OT_remove_all_shape_keys)
    bpy.utils.unregister_class(OBJECT_OT_remove_all_color_attributes)
    bpy.utils.unregister_class(OBJECT_OT_remove_unused_material_slots)
    bpy.utils.unregister_class(ExecuteAllOperatorsOperator)
    
    # UDP3DSMAX section
    bpy.utils.unregister_class(OBJECT_OT_remove_custom_properties)
    bpy.utils.unregister_class(OBJECT_OT_Add_Custom_Property)
    bpy.utils.unregister_class(OBJECT_OT_Remove_UDP3DSMAX_Property)
    bpy.utils.unregister_class(VIEW3D_PT_CleanupUtilities)

if __name__ == "__main__":
    register()
