#====================== BEGIN GPL LICENSE BLOCK ======================
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
#======================= END GPL LICENSE BLOCK ========================

from mathutils import *
from bpy.props import *
import bpy
import bmesh

# Version history
# 1.0.0 - 2022-04-08: Original version.
# 1.0.1 - 2022-04-28: Added bl_options = {"REGISTER", "UNDO"} so Blender won't crash when you undo the action.
# 1.0.2 - 2022-08-07: Misc formatting cleanup before uploading to GitHub.

###############################################################################
SCRIPT_NAME = 'good_vibrations'

# Allows an animator to easily construct a 'Side to Side Vibration' (as
# described by Richard Williams in The Animator's Survival Kit).
#
###############################################################################

bl_info = {
    "name": "Good Vibrations",
    "author": "Jeff Boller",
    "version": (1, 0, 2),
    "blender": (2, 93, 0),
    "location": "View3D > Properties > Animation",
    "description": "Allows an animator to easily construct a 'Side to Side Vibration' (as described by Richard Williams in The Animator's Survival Kit).",
    "wiki_url": "https://github.com/sundriftproductions/blenderaddon-good-vibrations/wiki",
    "tracker_url": "https://github.com/sundriftproductions/blenderaddon-good-vibrations",
    "category": "3D View"}

def set_obnoxious_headers_when_autokeying(self):
    # The obnoxious_autokeying_headers add-on does not work when the autokeying setting is changed via code; it only
    # gets triggered when you click on the UI. So we're imitating the behavior of that add-on here; when we change
    # the state of the autokeying setting, it's very, very obvious in Blender.
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
        bpy.context.preferences.themes[0].dopesheet_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].graph_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].nla_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].image_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].sequence_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].text_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].node_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].properties.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].outliner.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].info.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].console.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].clip_editor.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
        bpy.context.preferences.themes[0].topbar.space.header = (1.000000, 0.000000, 0.000000, 1.000000)
    else:
        bpy.context.preferences.themes[0].dopesheet_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].graph_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].nla_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].image_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].sequence_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].text_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].node_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].properties.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].outliner.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].info.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].console.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].clip_editor.space.header = (0.137255, 0.137255, 0.137255, 1.000000)
        bpy.context.preferences.themes[0].topbar.space.header = (0.137255, 0.137255, 0.137255, 1.000000)

def select_name( name = "", extend = True ):
    if extend == False:
        bpy.ops.object.select_all(action='DESELECT')
    ob = bpy.data.objects.get(name)
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob

def DoFrameRangesConflict():
    if bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end < bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start:
        vib1_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end
        vib1_frame_end = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start
    else:
        vib1_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start
        vib1_frame_end = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end

    vib2_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start
    vib2_frame_end = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start + (vib1_frame_end - vib1_frame_start)

    dest_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.dest_frame_start
    dest_frame_end = bpy.context.preferences.addons['good_vibrations'].preferences.dest_frame_start + (vib1_frame_end - vib1_frame_start)

    for dest_frame in range(dest_frame_start, dest_frame_end + 1):
        for vib1_frame in range(vib1_frame_start, vib1_frame_end + 1):
            if vib1_frame == dest_frame: return True

        for vib2_frame in range(vib2_frame_start, vib2_frame_end + 1):
            if vib2_frame == dest_frame: return True

    return False

class GOODVIBRATIONS_PT_Vib1RecordStartFrame(bpy.types.Operator):
    bl_idname = "vibr.vib1_record_start_frame"
    bl_label = "Start Frame"

    def execute(self, context):
        bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start = bpy.context.scene.frame_current
        return {'FINISHED'}

class GOODVIBRATIONS_PT_Vib1RecordEndFrame(bpy.types.Operator):
    bl_idname = "vibr.vib1_record_end_frame"
    bl_label = "End Frame"

    def execute(self, context):
        bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end = bpy.context.scene.frame_current
        return {'FINISHED'}

class GOODVIBRATIONS_PT_Vib2RecordStartFrame(bpy.types.Operator):
    bl_idname = "vibr.vib2_record_start_frame"
    bl_label = "Start Frame"

    def execute(self, context):
        bpy.context.preferences.addons['good_vibrations'].preferences.vib2_frame_start = bpy.context.scene.frame_current
        return {'FINISHED'}

class GOODVIBRATIONS_PT_DestRecordStartFrame(bpy.types.Operator):
    bl_idname = "vibr.dest_record_start_frame"
    bl_label = "Start Frame"

    def execute(self, context):
        bpy.context.preferences.addons['good_vibrations'].preferences.dest_frame_start = bpy.context.scene.frame_current
        return {'FINISHED'}

class GOODVIBRATIONS_PT_CreateKeyframes(bpy.types.Operator):
    bl_idname = "vibr.create_keyframes"
    bl_label = "Create Keyframes"
    bl_options = {"REGISTER", "UNDO"} # Required for when we do a bpy.ops.ed.undo_push(), otherwise Blender will crash when you try to undo the action in this class.

    def execute(self, context):
        self.report({'INFO'}, '**********************************')
        self.report({'INFO'}, SCRIPT_NAME + ' - START')

        bpy.ops.ed.undo_push()  # Manually record that when we do an undo, we want to go back to this exact state.

        ########## INPUT PARAMS #############
        obj_name = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object
        bone_name = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_bone

        if bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end < bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start:
            vib1_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end
            vib1_frame_end = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start
        else:
            vib1_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start
            vib1_frame_end = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end

        if vib1_frame_start == vib1_frame_end:
            self.report({'ERROR'}, '  ERROR: Vibration #1 Start Frame and End Frame cannot be the same frame.')
            return {'CANCELLED'}

        vib2_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.vib2_frame_start
        output_frame_start = bpy.context.preferences.addons['good_vibrations'].preferences.dest_frame_start
        frames_to_stay_on_vibrate = bpy.context.preferences.addons['good_vibrations'].preferences.vib_stay_on
        create_keyframe_every_x_frames = bpy.context.preferences.addons['good_vibrations'].preferences.create_keyframe_frame_interval
        flag_object_location = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object_location
        flag_object_rotation = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object_rotation
        flag_object_scale = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object_scale
        flag_bone_location = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_bone_location
        flag_bone_rotation = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_bone_rotation
        flag_bone_scale = bpy.context.preferences.addons['good_vibrations'].preferences.vibration_bone_scale
        #####################################

        using_vib1 = True  # Always start with using vib1.

        # Remember our original state for use_keyframe_insert_auto, so we can restore it at the end.
        original_use_keyframe_insert_auto = bpy.context.scene.tool_settings.use_keyframe_insert_auto

        # Remember our original frame number so we can restore it at the end.
        original_current_frame = bpy.context.scene.frame_current

        # Remember our original mode so we can restore it at the end.
        original_mode = bpy.context.active_object.mode

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        select_name(obj_name)
        bpy.context.view_layer.update()

        obj = bpy.data.objects[obj_name]

        if obj.type == 'ARMATURE':
            # Remember the state of all of the bone layers, so we can restore things to how they were at the end.
            original_bone_layers = [False, False, False, False, False, False, False, False, False, False, False,
                                    False, False, False, False, False, False, False, False, False, False, False,
                                    False, False, False, False, False, False, False, False, False, False]
            for i in range(0, 32):
                original_bone_layers[i] = obj.data.layers[i]

            # Now that we stored the state of the bone layers, show them all.
            for i in range(0, 32):
                obj.data.layers[i] = True

            bpy.ops.object.mode_set(mode='POSE')

            if bpy.context.object.data.pose_position == 'REST':
                self.report({'WARNING'},
                            '  WARNING: The rig is in REST position. We are automatically going to switch it to POSE position so we can move bones around.')
                bpy.context.object.data.pose_position = 'POSE'

        bpy.context.scene.tool_settings.use_keyframe_insert_auto = True

        self.report({'INFO'}, '  Walling off the beginning and ending of the destination frames...')
        bpy.context.scene.frame_set(output_frame_start)

        # Wall off the beginning.
        try:
            if obj.type == 'ARMATURE':
                bpy.ops.object.mode_set(mode='OBJECT')  # We can't use the "Available" key set in Pose Mode; we have to dip into Object Mode for a moment.
                # bpy.context.view_layer.update()
                bpy.ops.anim.keyframe_insert_menu(type='Available', confirm_success=True)
                bpy.ops.object.mode_set(mode='POSE')
            else:
                bpy.ops.anim.keyframe_insert_menu(type='Available', confirm_success=True)
        except: # If we have no animation data to copy, 'Available' won't be an option. We only need to check the first time we try this.
            self.report({'ERROR'}, "No existing animation data to copy for '" + obj_name + "'!")
            if obj.type == 'ARMATURE':
                # Restore the original bone layer states.
                for i in range(0, 32):
                    obj.data.layers[i] = original_bone_layers[i]
            bpy.context.scene.tool_settings.use_keyframe_insert_auto = original_use_keyframe_insert_auto
            set_obnoxious_headers_when_autokeying(self)  # ...and change back our headers to however they should be.
            bpy.context.scene.frame_current = original_current_frame
            bpy.context.view_layer.update()
            bpy.ops.object.mode_set(mode=original_mode) # Go back to whatever mode we were in.
            return {'CANCELLED'}

        # Wall off the ending.
        bpy.context.scene.frame_set(output_frame_start + (vib1_frame_end - vib1_frame_start))
        if obj.type == 'ARMATURE':
            bpy.ops.object.mode_set(mode='OBJECT')  # We can't use the "Available" key set in Pose Mode; we have to dip into Object Mode for a moment.
            # bpy.context.view_layer.update()
            bpy.ops.anim.keyframe_insert_menu(type='Available', confirm_success=True)
            bpy.ops.object.mode_set(mode='POSE')
        else:
            bpy.ops.anim.keyframe_insert_menu(type='Available', confirm_success=True)

        self.report({'INFO'}, '  Writing destination frames...')
        number_of_frames_on_a_vibrate = 0

        for offset in range(0, vib1_frame_end - vib1_frame_start + 1):
            if offset % create_keyframe_every_x_frames == 0:
                # It's OK to write a frame.
                if using_vib1:
                    frame = vib1_frame_start + offset
                else:
                    frame = vib2_frame_start + offset

                bpy.context.scene.frame_current = frame
                bpy.context.view_layer.update()

                locationAll = obj.location.copy()
                rotation_eulerAll = obj.rotation_euler.copy()
                rotation_quaternionAll = obj.rotation_quaternion.copy()
                scaleAll = obj.scale.copy()

                if obj.type == 'ARMATURE':
                    all_bone_info = []
                    for bone in obj.pose.bones[:]:
                        if bone_name == None or bone_name == '' or bone_name == bone.name:
                            bone_info = [bone.name, bone.location.copy(), bone.rotation_euler.copy(), bone.rotation_quaternion.copy(), bone.scale.copy()]
                            all_bone_info.append(bone_info)

                # Now go to the frame where we want to write the keyframe and make the appropriate changes to the object.
                frame_to_write_to = output_frame_start + offset
                bpy.context.scene.frame_current = frame_to_write_to
                bpy.context.view_layer.update()

                # Set the object location/scale/rotation appropriately.
                if flag_object_location:
                    obj.location = locationAll

                if flag_object_rotation:
                    obj.rotation_euler = rotation_eulerAll
                    obj.rotation_quaternion = rotation_quaternionAll

                if flag_object_scale:
                    obj.scale = scaleAll

                if obj.type == 'ARMATURE':
                    for bone_info in all_bone_info:
                        if flag_bone_location:
                            obj.pose.bones[bone_info[0]].location = bone_info[1]

                        if flag_bone_rotation:
                            obj.pose.bones[bone_info[0]].rotation_euler = bone_info[2]
                            obj.pose.bones[bone_info[0]].rotation_quaternion = bone_info[3]

                        if flag_bone_scale:
                            obj.pose.bones[bone_info[0]].scale = bone_info[4]

                if obj.type == 'ARMATURE':
                    bpy.ops.object.mode_set(mode='OBJECT') # We can't use the "Available" key set in Pose Mode; we have to dip into Object Mode for a moment.
                    #bpy.context.view_layer.update()
                    bpy.ops.anim.keyframe_insert_menu(type='Available', confirm_success=True)
                    bpy.ops.object.mode_set(mode='POSE')
                else:
                    bpy.ops.anim.keyframe_insert_menu(type='Available', confirm_success=True)

                # Now let's find ONLY the keyframes we just inserted and ensure that those interpolation types are set to CONSTANT.
                for fcu in obj.animation_data.action.fcurves:
                    for keyframe in fcu.keyframe_points:
                        frame = keyframe.co[0]
                        # self.report({'INFO'}, (str(dir(keyframe))))

                        if frame == frame_to_write_to:
                            keyframe.interpolation = 'CONSTANT'  # This changes the interpolation.

            number_of_frames_on_a_vibrate += 1
            if number_of_frames_on_a_vibrate >= frames_to_stay_on_vibrate:
                number_of_frames_on_a_vibrate = 0
                using_vib1 = not using_vib1  # Use the other vibration range on the next iteration.

        if obj.type == 'ARMATURE':
            # Restore the original bone layer states.
            for i in range(0, 32):
               obj.data.layers[i] = original_bone_layers[i]

        # Restore the original use_keyframe_insert_auto.
        bpy.context.scene.tool_settings.use_keyframe_insert_auto = original_use_keyframe_insert_auto
        set_obnoxious_headers_when_autokeying(self)  # ...and change back our headers to however they should be.
        bpy.context.scene.frame_current = original_current_frame
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode=original_mode)  # Go back to whatever mode we were in.

        self.report({'INFO'}, SCRIPT_NAME + ' - END')
        self.report({'INFO'}, '**********************************')
        self.report({'INFO'}, 'Done running script ' + SCRIPT_NAME)

        return {'FINISHED'}

class GoodVibrationsPreferencesPanel(bpy.types.AddonPreferences):
    bl_idname = __module__
    vibration_object: bpy.props.StringProperty(name="Object", description='Which object should vibrate')
    vibration_object_location: bpy.props.BoolProperty(default=True, description="Vibrate object location")
    vibration_object_rotation: bpy.props.BoolProperty(default=True, description="Vibrate object rotation")
    vibration_object_scale: bpy.props.BoolProperty(default=True, description="Vibrate object scale")
    vibration_bone: bpy.props.StringProperty(name="Bone", description='Which bone should vibrate? Leave empty if all bones should vibrate')
    vibration_bone_location: bpy.props.BoolProperty(default=True, description="Vibrate bone location")
    vibration_bone_rotation: bpy.props.BoolProperty(default=True, description="Vibrate bone rotation")
    vibration_bone_scale: bpy.props.BoolProperty(default=True, description="Vibrate bone scale")
    vib1_frame_start: bpy.props.IntProperty(name='Start Frame', default=301, description='The frame where Vibration #1 starts')
    vib1_frame_end: bpy.props.IntProperty(name='End Frame', default=400, description='The frame where Vibration #1 ends')
    vib2_frame_start: bpy.props.IntProperty(name='Start Frame', default=401, description='The frame where Vibration #2 starts')
    vib_stay_on: bpy.props.IntProperty(name='Switch Vibration Frame Interval', default=1, description='How many frames should we continue pulling keys from either Vibration #1 or Vibration #2 before switching to the other vibration')
    dest_frame_start: bpy.props.IntProperty(name='Start Frame', default=101, description='The frame where the new keyframes will start')
    create_keyframe_frame_interval: bpy.props.IntProperty(name='Create Keyframe Frame Interval', default=1, description='How often do we create a keyframe in the Destination Frames output')

    def draw(self, context):
        self.layout.label(text="Current values")

class GOODVIBRATIONS_PT_Main(bpy.types.Panel):
    bl_idname = "GOODVIBRATIONS_PT_Main"
    bl_label = "Good Vibrations"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        do_frame_ranges_conflict = DoFrameRangesConflict()

        box = self.layout.box()
        row = box.row(align=True)
        row.label(text="Object to Vibrate")

        icon_type = 'OBJECT_DATA'
        try:
            obj = bpy.data.objects[bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object]
            if obj is not None:
                if obj.type == 'ARMATURE':
                    icon_type = 'ARMATURE_DATA'
        except:
            pass

        row = box.row(align=True)
        row.prop_search(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_object", bpy.data, "objects", icon=icon_type)

        row = box.row(align=True)
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_object_location", text="Location")
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_object_rotation", text="Rotation")
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_object_scale", text="Scale")

        try:
            obj = bpy.data.objects[bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object]
            if obj is not None:
                if obj.type == 'ARMATURE':
                    armature = obj.data
                    row = box.row(align=True)
                    row.prop_search(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_bone", armature, "bones", icon='BONE_DATA')

                    row = box.row(align=True)
                    row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_bone_location", text="Location")
                    row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_bone_rotation", text="Rotation")
                    row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vibration_bone_scale", text="Scale")
        except:
            pass

        row = box.row(align=True)

        box = self.layout.box()
        row = box.row(align=True)
        row.label(text="Source Frames")

        row = box.row(align=True)
        row.label(text="Vibration #1")

        row = box.row(align=True)
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vib1_frame_start")
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vib1_frame_end")

        row = box.row(align=True)
        row.operator("vibr.vib1_record_start_frame", text='Start Frame', icon='TRIA_UP')
        row.operator("vibr.vib1_record_end_frame", text='End Frame', icon='TRIA_UP')

        row = box.row(align=True)

        if bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end < bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start:
            total_number_of_frames = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start - bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end
        else:
            total_number_of_frames = bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_end - bpy.context.preferences.addons['good_vibrations'].preferences.vib1_frame_start

        row = box.row(align=True)
        row.label(text="Vibration #2")
        row = box.row(align=True)
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vib2_frame_start")
        end_frame = total_number_of_frames + bpy.context.preferences.addons['good_vibrations'].preferences.vib2_frame_start
        row.label(text=" End Frame: " + str(end_frame))

        row = box.row(align=True)
        row.operator("vibr.vib2_record_start_frame", text='Start Frame', icon='TRIA_UP')
        row.label(text=" ")

        row = box.row(align=True)

        row = box.row(align=True)
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "vib_stay_on")

        box = self.layout.box()
        row = box.row(align=True)
        row.label(text="Destination Frames")

        row = box.row(align=True)
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "dest_frame_start")
        end_frame = total_number_of_frames + bpy.context.preferences.addons['good_vibrations'].preferences.dest_frame_start
        row.label(text=" End Frame: " + str(end_frame))

        row = box.row(align=True)
        row.operator("vibr.dest_record_start_frame", text='Start Frame', icon='TRIA_UP')
        if do_frame_ranges_conflict:
            row.label(text="*** CONFLICT WITH SOURCE FRAMES! ***")
        else:
            row.label(text=" ")

        row = box.row(align=True)
        row = box.row(align=True)
        row.prop(bpy.context.preferences.addons['good_vibrations'].preferences, "create_keyframe_frame_interval")

        row = self.layout.row(align=True)
        row.operator("vibr.create_keyframes",icon='KEYFRAME')

        # Now let's see if we have any invalid parameters so that we would need to disable the Create Keyframes button.
        if do_frame_ranges_conflict == True:
            row.enabled = False
        else:
            if bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object == None or bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object == "":
                row.enabled = False
            else:
                try:
                    obj = bpy.data.objects[bpy.context.preferences.addons['good_vibrations'].preferences.vibration_object]
                    if obj is None:
                        row.enabled = False
                except:
                    row.enabled = False

def register():
    bpy.utils.register_class(GoodVibrationsPreferencesPanel)
    bpy.utils.register_class(GOODVIBRATIONS_PT_CreateKeyframes)
    bpy.utils.register_class(GOODVIBRATIONS_PT_Vib1RecordStartFrame)
    bpy.utils.register_class(GOODVIBRATIONS_PT_Vib1RecordEndFrame)
    bpy.utils.register_class(GOODVIBRATIONS_PT_Vib2RecordStartFrame)
    bpy.utils.register_class(GOODVIBRATIONS_PT_DestRecordStartFrame)
    bpy.utils.register_class(GOODVIBRATIONS_PT_Main)

def unregister():
    bpy.utils.unregister_class(GoodVibrationsPreferencesPanel)
    bpy.utils.unregister_class(GOODVIBRATIONS_PT_CreateKeyframes)
    bpy.utils.unregister_class(GOODVIBRATIONS_PT_Vib1RecordStartFrame)
    bpy.utils.unregister_class(GOODVIBRATIONS_PT_Vib1RecordEndFrame)
    bpy.utils.unregister_class(GOODVIBRATIONS_PT_Vib2RecordStartFrame)
    bpy.utils.unregister_class(GOODVIBRATIONS_PT_DestRecordStartFrame)
    bpy.utils.unregister_class(GOODVIBRATIONS_PT_Main)

if __name__ == "__main__":
    register()
