bl_info = {
    "name": "Join_Hair_Curves",
    "author": "Morzio",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Join Curves",
    "description": "Add Geometry Node Modifier that joins selected hair curves.",
    "warning": "",
    "wiki_url": "https://github.com/Morzio/Join-Hair-Curves",
    "category": "3D View",
}

import bpy
from numpy import array
from bpy.types import Panel, Operator
from bpy.utils import register_class, unregister_class

from .join_curves import join_curves_to_active



class JOINHAIRCURVES_PT_Panel(Panel):
    """
    """
    bl_idname = "JOINHAIRCURVES_PT_Panel"
    bl_label = "JOIN HAIR CURVES"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Join Hair Curves"
    
    @classmethod
    def poll(cls, context):
        return context.object.mode == 'OBJECT'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        main_box = layout.box()
        header_row = main_box.row()
        header_row.label(text="JOIN HAIR CURVES")
        body_row = main_box.row()
        body_row.operator("scene.join_hair_curves", text="Join", icon='CURVES')




class JOINHAIRCURVES_OT_Join(Operator):
    """
    """
    bl_idname = "scene.join_hair_curves"
    bl_label = "Join Hair Curves"
    bl_description = "Join Hair Curves."
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        selected = context.selected_objects
        sel_types = array([ob.type for ob in selected])
        is_curves = (sel_types == 'CURVES').all()
        return context.active_object and len(selected) > 1 and is_curves
    
    def execute(self, context):
        join_curves_to_active()
        return{'FINISHED'}



classes = [
    JOINHAIRCURVES_PT_Panel,
    JOINHAIRCURVES_OT_Join,
    ]


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()


