bl_info = {
    "name": "MeshCleaner",
    "author": "Anthony Dimovski",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Item Tab"
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy


class EnableAutoSmooth(bpy.types.Operator):
    """This enables Auto Smooth and sets a value of 180"""
    bl_idname = "object.enable_auto_smooth"
    bl_label = "Enable Auto Smooth"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.data.use_auto_smooth = True
                obj.data.auto_smooth_angle = 3.14159  # 180 degrees in radians
        return {'FINISHED'}


class ObjNameToMeshName(bpy.types.Operator):
    """Obj Name to Data Name"""
    bl_idname = "object.objname_to_meshname"
    bl_label = "Obj Name to Data Name"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.data.name = obj.name
        return {'FINISHED'}


class RemoveVertexGroups(bpy.types.Operator):
    """Remove Vertex Groups"""
    bl_idname = "object.remove_vertex_groups"
    bl_label = "Remove Vertex Groups"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.vertex_groups.clear()
        return {'FINISHED'}


class RemoveShapeKeys(bpy.types.Operator):
    """Remove Shape Keys"""
    bl_idname = "object.remove_shape_keys"
    bl_label = "Remove Shape Keys"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj.data.shape_keys is not None:
                key_blocks = obj.data.shape_keys.key_blocks
                if key_blocks:
                    while len(key_blocks) > 0:
                        obj.shape_key_remove(key_blocks[0])
        return {'FINISHED'}


class RemoveVertexColors(bpy.types.Operator):
    """Remove Vertex Colors, not to be confused with Color Attributes"""
    bl_idname = "object.remove_vertex_colors"
    bl_label = "Remove Vertex Colors"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                while obj.data.vertex_colors:
                    obj.data.vertex_colors.remove(obj.data.vertex_colors[0])
        return {'FINISHED'}


class RemoveCustomAttributes(bpy.types.Operator):
    """This will remove every custom property, except for any UDP3DSMAX codes"""
    bl_idname = "object.remove_custom_attributes"
    bl_label = "Remove Custom Properties"
    
    def execute(self, context):
        for obj in context.selected_objects:
            custom_properties = list(obj.keys())
            to_remove = [prop for prop in custom_properties if prop != 'UDP3DSMAX']
            for prop in to_remove:
                del obj[prop]
        return {'FINISHED'}


class RemoveAttrIndices(bpy.types.Operator):
    """Remove Attribute Indices"""
    bl_idname = "object.remove_attr_indices"
    bl_label = "Remove Attribute Indices"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                attributes_to_remove = [attr for attr in obj.data.attributes]
                for attr in attributes_to_remove:
                    obj.data.attributes.remove(attr)
        return {'FINISHED'}


class RemoveUnusedMaterialsSlots(bpy.types.Operator):
    """Remove Unused Material Slots"""
    bl_idname = "object.remove_unused_materials_slots"
    bl_label = "Remove Unused Materials Slots"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if not slot.material:
                        bpy.ops.object.material_slot_remove({'object': obj})
        return {'FINISHED'}


class DoAllOperations(bpy.types.Operator):
    """Does all of the above operations except for Auto Smooth"""
    bl_idname = "object.do_all_operations"
    bl_label = "Do all operations"

    def execute(self, context):
        bpy.ops.object.objname_to_meshname()
        bpy.ops.object.remove_vertex_groups()
        bpy.ops.object.remove_shape_keys()
        bpy.ops.object.remove_vertex_colors()
        bpy.ops.object.remove_custom_attributes()
        bpy.ops.object.remove_attr_indices()
        bpy.ops.object.remove_unused_materials_slots()
        return {'FINISHED'}


class MeshCleanerPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mesh Cleaner"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('object.enable_auto_smooth', icon='NORMALS_VERTEX')
        row = layout.row()
        row.operator('object.objname_to_meshname', icon='MESH_DATA')
        row = layout.row()
        row.operator('object.remove_vertex_groups', icon='GROUP_VERTEX')
        row = layout.row()
        row.operator('object.remove_shape_keys', icon='SHAPEKEY_DATA')
        row = layout.row()
        row.operator('object.remove_vertex_colors', icon='COLOR')
        row = layout.row()
        row.operator('object.remove_custom_attributes', icon='DUPLICATE')
        row = layout.row()
        row.operator('object.remove_attr_indices', icon='HAND')
        row = layout.row()
        row.operator('object.remove_unused_materials_slots', icon='MATERIAL')
        row = layout.row()
        row.operator('object.do_all_operations', icon='ERROR')

def register():
    bpy.utils.register_class(MeshCleanerPanel)
    bpy.utils.register_class(EnableAutoSmooth)
    bpy.utils.register_class(ObjNameToMeshName)
    bpy.utils.register_class(RemoveVertexGroups)
    bpy.utils.register_class(RemoveShapeKeys)
    bpy.utils.register_class(RemoveVertexColors)
    bpy.utils.register_class(RemoveCustomAttributes)
    bpy.utils.register_class(RemoveAttrIndices)
    bpy.utils.register_class(RemoveUnusedMaterialsSlots)
    bpy.utils.register_class(DoAllOperations)


def unregister():
    bpy.utils.unregister_class(MeshCleanerPanel)
    bpy.utils.unregister_class(EnableAutoSmooth)
    bpy.utils.unregister_class(ObjNameToMeshName)
    bpy.utils.unregister_class(RemoveVertexGroups)
    bpy.utils.unregister_class(RemoveShapeKeys)
    bpy.utils.unregister_class(RemoveVertexColors)
    bpy.utils.unregister_class(RemoveCustomAttributes)
    bpy.utils.unregister_class(RemoveAttrIndices)
    bpy.utils.unregister_class(RemoveUnusedMaterialsSlots)
    bpy.utils.unregister_class(DoAllOperations)


if __name__ == "__main__":
    register()
