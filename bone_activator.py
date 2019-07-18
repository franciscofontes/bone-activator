bl_info = {
    "name": "Bone Activator",
    "author": "Francisco Fontes",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Armature > Select",
    "description": "Active a bone selected",
    "warning": "",
    "wiki_url": "",
    "support": "TESTING",
    "category": "Rigging",
}

import bpy

class BoneActivator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "armature.bone_activator"
    bl_label = "Activate Bone"
    bl_description = (
        "Activates a selected bone"
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def msgwarning_select(self):        
        self.report({'WARNING'}, 'Please select a bone') 
        
    def msginfo_actived(self, bone):        
        self.report({'INFO'}, bone.name + ' Actived')

    def execute(self, context):
        if bpy.context.mode == 'EDIT_ARMATURE':                 
            obj = bpy.context.view_layer.objects.active
            bones = bpy.context.selected_bones
            if len(bones) > 0 :
                bone = bones[0]
                bone.select = True;
                bone.select_head = True;
                bone.select_tail = True;
                obj.data.edit_bones.active = bone
                self.msginfo_actived(bone)
            else:
                self.msgwarning_select()
        elif bpy.context.mode == 'POSE': 
            obj = bpy.context.view_layer.objects.active
            bones = bpy.context.selected_pose_bones_from_active_object
            if len(bones) > 0 :
                bone = bones[0].bone
                bone.select = True;
                bone.select_head = True;
                bone.select_tail = True;
                obj.data.bones.active = bone
                self.msginfo_actived(bone)
            else:
                self.msgwarning_select()
        else:
            self.report({'WARNING'}, 'Only in Edit mode or Pose mode') 
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(BoneActivator.bl_idname)

addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:        
        km = kc.keymaps.new(name = "Armature",space_type='EMPTY', region_type='WINDOW')
        kmi = km.keymap_items.new('armature.bone_activator', 'A', 'PRESS', ctrl=True)
        addon_keymaps.append((km,kmi))

def unregister_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    bpy.utils.register_class(BoneActivator)  
    bpy.types.VIEW3D_MT_select_edit_armature.append(menu_func)
    bpy.types.VIEW3D_MT_select_pose.append(menu_func)
    bpy.types.VIEW3D_MT_armature_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.append(menu_func) 
    register_keymaps()
    
def unregister():    
    bpy.utils.unregister_class(BoneActivator)
    bpy.types.VIEW3D_MT_select_edit_armature.remove(menu_func)
    bpy.types.VIEW3D_MT_select_pose.remove(menu_func)
    bpy.types.VIEW3D_MT_armature_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(menu_func)    
    unregister_keymaps()
        
if __name__ == "__main__":
    register()
