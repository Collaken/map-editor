import bpy
import os
import string
import re
from .operatorHelpers import *
from .updateTextures import *

# we are using this for <end> (exit door)
class addDoor(bpy.types.Operator):
    bl_idname = "wm.add_door"
    bl_label = "Add a door"
#    bl_description = "Add a door." # for the future
    bl_description = "Add an exit door (use only once)"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        addon_prefs = context.user_preferences.addons[__package__].preferences
        
        realpath = os.path.expanduser(addon_prefs.dataDir + "meshes/Door.obj")
        bpy.ops.import_scene.obj(filepath=realpath)
        bpy.ops.transform.translate(value=(bpy.context.scene.cursor_location))
        bpy.types.Object.glpType = bpy.props.StringProperty()
        
        mat = getMaterial('textures/door/door00.png', (1, 1, 1))
        mat.texture_slots[0].texture_coords = 'UV'
        mat.texture_slots[0].mapping = 'FLAT'
        
        # make sure to get all imported objects
        obj_objects = bpy.context.selected_objects[:]
        
        # iterate through all objects to find new
        for object in obj_objects:
            if object.glpTypes and object.glpTypes == "none":
                object.select = True
                object.glpTypes = "door"
                context.scene.objects.active = object

                me = object.data
                if (len(me.materials) == 0):
                    me.materials.append(mat)
                else:
                    me.materials[0] = mat
                
                fixDoorTexture(me)
        
        return {'FINISHED'}

class addLamp(bpy.types.Operator):
    bl_idname = "wm.add_lamp"
    bl_label = "Add a lamp"
    bl_description = "Add a lamp. (Not implemented)"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        addon_prefs = context.user_preferences.addons[__package__].preferences
        
        realpath = os.path.expanduser(addon_prefs.dataDir + "meshes/Lamp.obj")
        bpy.ops.import_scene.obj(filepath=realpath)
        bpy.ops.transform.translate(value=(bpy.context.scene.cursor_location))
        bpy.types.Object.glpType = bpy.props.StringProperty()
        object = bpy.context.active_object
        if object:
            object.glpTypes = "lamp"
        return {'FINISHED'}

class addButton(bpy.types.Operator):
    bl_idname = "wm.add_button"
    bl_label = "Add a button"
    bl_description = "Add a button. (Not implemented)"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        addon_prefs = context.user_preferences.addons[__package__].preferences
        
        realpath = os.path.expanduser(addon_prefs.dataDir + "meshes/Button.obj")
        bpy.ops.import_scene.obj(filepath=realpath)
        bpy.ops.transform.translate(value=(bpy.context.scene.cursor_location))
        bpy.types.Object.glpType = bpy.props.StringProperty()
        object = bpy.context.active_object
        if object:
            object.glpTypes = "button"
        return {'FINISHED'}

class setPortalable(bpy.types.Operator):
    bl_idname = "wm.set_portalable"
    bl_label = "Mark as portalable wall"
    bl_description = "Mark the selection as portalable wall."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        mat = getMaterial('textures/concrete/wall00.png', (1, 1, 1))
        bpy.types.Object.glpType = bpy.props.StringProperty()
        object = bpy.context.active_object
        if object:
            resetTriggerSettings(object)
            
            object.glpTypes = "wall"
            object.glpWallTypes = "portalable"
            me = object.data
            if (len(me.materials) == 0):
                me.materials.append(mat)
            else:
                me.materials[0] = mat
            
            UpdateTexture.updateTexture(object)
        return {'FINISHED'}

class setWall(bpy.types.Operator):
    bl_idname = "wm.set_wall"
    bl_label = "Merk as metal wall"
    bl_description = "Mark the selection as metal wall."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        mat = getMaterial('textures/metal/tiles00x3.jpg', (0.2, 0.2, 0.2))
        bpy.types.Object.glpType = bpy.props.StringProperty()
        object = bpy.context.active_object
        if object:
            resetTriggerSettings(object)
            
            object.glpTypes = "wall"
            object.glpWallTypes = "default"
            me = object.data
            if (len(me.materials) == 0):
                me.materials.append(mat)
            else:
                me.materials[0] = mat
            
            UpdateTexture.updateTexture(object)
        return {'FINISHED'}

class addWall(bpy.types.Operator):
    bl_idname = "wm.add_wall"
    bl_label = "Add a metal wall"
    bl_description = "Add a metal wall."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        setWall.execute(self, context)
        return {'FINISHED'}

class addPortalable(bpy.types.Operator):
    bl_idname = "wm.add_portalable"
    bl_label = "Add a portalable wall"
    bl_description = "Add a portalable wall."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        setPortalable.execute(self, context)
        return {'FINISHED'}