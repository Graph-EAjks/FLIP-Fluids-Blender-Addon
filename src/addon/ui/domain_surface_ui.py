# Blender FLIP Fluids Add-on
# Copyright (C) 2022 Ryan L. Guy
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bpy

from ..utils import version_compatibility_utils as vcu
from ..utils import installation_utils

    
class FLIPFLUID_PT_DomainTypeFluidSurfacePanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"
    bl_category = "FLIP Fluid"
    bl_label = "FLIP Fluid Surface"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj_props = vcu.get_active_object(context).flip_fluid
        return obj_props.is_active and obj_props.object_type == "TYPE_DOMAIN"

    def draw(self, context):
        obj = vcu.get_active_object(context)
        sprops = obj.flip_fluid.domain.surface
        show_advanced = not vcu.get_addon_preferences(context).beginner_friendly_mode
        show_documentation = vcu.get_addon_preferences(context).show_documentation_in_ui

        if show_documentation:
            column = self.layout.column(align=True)
            column.operator(
                "wm.url_open", 
                text="Surface and Meshing Documentation", 
                icon="WORLD"
            ).url = "https://github.com/rlguy/Blender-FLIP-Fluids/wiki/Domain-Surface-Settings"
            column.operator(
                "wm.url_open", 
                text="How do I make my surface smoother?", 
                icon="WORLD"
            ).url = "https://github.com/rlguy/Blender-FLIP-Fluids/wiki/Domain-Surface-Settings#mesh-smoothing"
            column.operator(
                "wm.url_open", 
                text="Mesh banding against curved obstacles", 
                icon="WORLD"
            ).url = "https://github.com/rlguy/Blender-FLIP-Fluids/wiki/Scene-Troubleshooting#mesh-banding-artifacts-against-curved-obstacles"

        box = self.layout.box()
        column = box.column(align=True)

        column.label(text="Surface Mesh:")
        column.prop(sprops, "subdivisions")
        row = column.row(align=True)
        if sprops.particle_scale < 0.999:
            row.alert = True
        row.prop(sprops, "particle_scale")

        if not show_advanced:
            return

        object_collection = vcu.get_scene_collection()
        if vcu.is_blender_28():
            search_group = "all_objects"
        else:
            search_group = "objects"

        box = self.layout.box()
        box.label(text="Meshing Volume:")
        row = box.row(align=True)
        row.prop(sprops, "meshing_volume_mode", expand=True)
        column = box.column(align=True)
        split = column.split(align=True)
        column_left = split.column(align=True)
        column_right = split.column(align=True)
        column_right.enabled = sprops.meshing_volume_mode == "MESHING_VOLUME_MODE_OBJECT"
        column_right.prop_search(sprops, "meshing_volume_object", object_collection, search_group, text="Object")
        column_right.prop(sprops, "export_animated_meshing_volume_object")

        box = self.layout.box()
        box.label(text="Meshing Against Boundary:")
        column = box.column(align=True)
        split = column.split(align=True)
        column_left = split.column()
        column_left.prop(sprops, "remove_mesh_near_domain")
        column_right = split.column()
        column_right.enabled = sprops.remove_mesh_near_domain
        column_right.prop(sprops, "remove_mesh_near_domain_distance")

        box = self.layout.box()
        box.label(text="Meshing Against Obstacles:")
        column = box.column(align=True)
        column.prop(sprops, "enable_meshing_offset")
        row = box.row(align=True)
        row.enabled = sprops.enable_meshing_offset
        row.prop(sprops, "obstacle_meshing_mode", expand=True)

        if show_documentation:
            column = box.column(align=True)
            column.operator(
                "wm.url_open", 
                text="Which meshing offset mode to use?", 
                icon="WORLD"
            ).url = "https://github.com/rlguy/Blender-FLIP-Fluids/wiki/Domain-Surface-Settings#which-offset-mode-to-use"

        # Removed surface smoothing options. These are better set
        # using a Blender smooth modifier.
        """
        box = self.layout.box()
        box.label(text="Smoothing:")
        row = box.row(align=True)
        row.prop(sprops, "smoothing_value")
        row.prop(sprops, "smoothing_iterations")
        """

        # Motion Blur is no longer supported
        #column = self.layout.column(align=True)
        #column.separator()
        #column.prop(sprops, "generate_motion_blur_data")

        if vcu.get_addon_preferences().is_developer_tools_enabled():
            box = self.layout.box()
            box.label(text="Geometry Attributes:")
            if vcu.is_blender_293():

                subbox = box.box()
                subbox.label(text="Velocity Based Attributes:")
                column = subbox.column(align=True)
                split = column.split(align=True)
                column_left = split.column(align=True)
                column_right = split.column(align=True)
                column_right.enabled = sprops.enable_velocity_vector_attribute or sprops.enable_speed_attribute or sprops.enable_vorticity_vector_attribute
                column_left.prop(sprops, "enable_velocity_vector_attribute", text="Velocity Attributes")
                column_right.prop(sprops, "enable_velocity_vector_attribute_against_obstacles", text="Generate Against Obstacles")
                column.prop(sprops, "enable_speed_attribute", text="Speed Attributes")
                column.prop(sprops, "enable_vorticity_vector_attribute", text="Vorticity Attributes")
                

                subbox = box.box()
                subbox.label(text="Color and Mixing Attributes:")
                column = subbox.column(align=True)
                split = column.split(align=True)
                column_left = split.column(align=True)
                column_right = split.column(align=True)
                column_left.prop(sprops, "enable_color_attribute", text="Color Attributes")
                column_right.prop(sprops, "color_attribute_radius", text="Smoothing", slider=True)

                column = subbox.column(align=True)
                split = column.split(align=True)
                column_left = split.column(align=True)
                column_right = split.column(align=True)
                column_left.enabled = sprops.enable_color_attribute
                column_left.prop(sprops, "enable_color_attribute_mixing", text="Enable Mixing")
                column_right.enabled = sprops.enable_color_attribute and sprops.enable_color_attribute_mixing
                column_right.prop(sprops, "color_attribute_mixing_rate", text="Mix Rate", slider=True)
                column_right.prop(sprops, "color_attribute_mixing_radius", text="Mix Radius", slider=True)

                column = subbox.column(align=True)
                column.enabled = sprops.enable_color_attribute and sprops.enable_color_attribute_mixing
                column.label(text="Mixing Mode:")
                row = column.row(align=True)
                row.enabled = sprops.enable_color_attribute
                row.prop(sprops, "color_attribute_mixing_mode", expand=True)

                if sprops.color_attribute_mixing_mode == 'COLOR_MIXING_MODE_MIXBOX':
                    if not installation_utils.is_mixbox_supported():
                        column.label(text="Mixbox feature is not supported", icon="ERROR")
                        column.label(text="in this version of the FLIP Fluids Addon", icon="ERROR")

                    if installation_utils.is_mixbox_supported():
                        if installation_utils.is_mixbox_installation_complete():
                            column.label(text="Mixbox Plugin Status: Installed", icon="CHECKMARK")
                        else:
                            column.label(text="Install the Mixbox plugin in the", icon="INFO")
                            column.label(text="FLIP Fluids Addon preferences", icon="INFO")
                            column.operator("flip_fluid_operators.open_preferences", text="Open Preferences", icon="PREFERENCES")
                else:
                    pass

                subbox = box.box()
                subbox.label(text="Other Attributes:")
                column = subbox.column(align=True)
                row = column.row(align=True)
                row.prop(sprops, "enable_age_attribute", text="Age Attributes")
                row.prop(sprops, "age_attribute_radius", text="Smoothing", slider=True)
                column.prop(sprops, "enable_source_id_attribute", text="Source ID Attributes")

                # Viscosity attribute is enabled in the FLIP Fluid World panel as 'Variable Viscosity'
                #column.prop(sprops, "enable_viscosity_attribute", text="Viscosity Attributes")
            else:
                column = box.column(align=True)
                column.enabled = False
                column.label(text="Geometry attribute features are only available in", icon='ERROR')
                column.label(text="Blender 2.93 or later", icon='ERROR')

            if show_documentation:
                column = box.column(align=True)
                column.operator(
                    "wm.url_open", 
                    text="Domain Attributes Documentation", 
                    icon="WORLD"
                ).url = "https://github.com/rlguy/Blender-FLIP-Fluids/wiki/Domain-Attributes-and-Data-Settings"
                column.operator(
                    "wm.url_open", 
                    text="Attributes and Motion Blur Example Scenes", 
                    icon="WORLD"
                ).url = "https://github.com/rlguy/Blender-FLIP-Fluids/wiki/Example-Scene-Descriptions#attribute-and-motion-blur-examples"


def register():
    bpy.utils.register_class(FLIPFLUID_PT_DomainTypeFluidSurfacePanel)


def unregister():
    bpy.utils.unregister_class(FLIPFLUID_PT_DomainTypeFluidSurfacePanel)
