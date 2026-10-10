"""
PROJECT REVOLUTION — Cinematic Camera & Shading Render Script
Renders Courtyard_Rooftop_Gym_Scene.blend with Cycles (32 samples)
showing full architectural framing, materials, and golden hour lighting.
"""

import bpy
import os
import math
from mathutils import Vector

PROJECT_ROOT = r"C:\Users\npal7\PROJECT\REVOLUTION"
SCENE_PATH = os.path.join(PROJECT_ROOT, "Art", "Blender", "Courtyard_Rooftop_Gym_Scene.blend")
OUTPUT_RENDER = os.path.join(PROJECT_ROOT, "Art", "Exports", "Courtyard_Rooftop_Gym_Cinematic_50mm.png")

bpy.ops.wm.open_mainfile(filepath=SCENE_PATH)

cam = bpy.data.objects.get("Cam_Cinematic_Kabir_EyeLevel")
if cam:
    # Position camera back to view full two-story facade, stairs, and rooftop
    cam.location = Vector((-2.0, -11.0, 3.2))
    cam.rotation_euler = (math.radians(76.0), 0.0, math.radians(-12.0))
    cam.data.lens = 38.0  # Wider 38mm cinematic lens
    cam.data.dof.use_dof = False

# Configure Render Engine
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'  # CPU is reliable in headless
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.filepath = OUTPUT_RENDER

# Enhance sun lamp for dramatic contrast
sun = bpy.data.objects.get("Sun_GoldenHour_Punjab")
if sun:
    sun.data.energy = 5.5
    sun.data.color = (1.0, 0.78, 0.52) # Rich golden hour
    sun.rotation_euler = (math.radians(55.0), math.radians(20.0), math.radians(-40.0))

print("Rendering cinematic frame with Cycles (32 samples)...")
bpy.ops.render.render(write_still=True)
print(f"SUCCESS: Rendered -> {OUTPUT_RENDER}")
