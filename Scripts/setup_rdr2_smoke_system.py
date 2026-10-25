import unreal
import os

def import_texture(source_file, destination_path, srgb=True, is_normal=False):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    task = unreal.AssetImportTask()
    task.filename = source_file
    task.destination_path = destination_path
    task.destination_name = os.path.splitext(os.path.basename(source_file))[0]
    task.replace_existing = True
    task.automated = True
    task.save = True
    
    asset_tools.import_asset_tasks([task])
    imported = unreal.EditorAssetLibrary.load_asset(f"{destination_path}/{task.destination_name}")
    if imported:
        imported.set_editor_property("srgb", srgb)
        if is_normal:
            imported.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        else:
            imported.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_DEFAULT)
        unreal.EditorAssetLibrary.save_loaded_asset(imported)
        unreal.log_warning(f"Successfully imported and configured texture: {imported.get_path_name()}")
    return imported

def create_rdr2_smoke_material(puff_tex, flow_tex):
    mat_path = "/Game/VFX/Smoke/Materials"
    mat_name = "M_RDR2_Pyroclastic_Smoke"
    full_path = f"{mat_path}/{mat_name}"
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_factory = unreal.MaterialFactoryNew()
    
    mat = unreal.EditorAssetLibrary.load_asset(full_path)
    if not mat:
        mat = asset_tools.create_asset(mat_name, mat_path, unreal.Material, material_factory)
        
    if not mat:
        unreal.log_error("Failed to create M_RDR2_Pyroclastic_Smoke!")
        return None
        
    mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    mat.set_editor_property("two_sided", True)
    
    # Clear existing expressions
    # In UE 5.5 delete_all_material_expressions might assert if not rooted, so we can build using expressions
    try:
        unreal.MaterialEditingLibrary.delete_all_material_expressions(mat)
    except Exception as e:
        unreal.log_warning(f"delete_all_material_expressions skipped: {e}")
        
    # Particle Color Expression
    part_color = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionParticleColor, -600, -200
    )
    
    # Texture Sample for Flow/Curl noise
    flow_sample = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionTextureSample, -800, 200
    )
    flow_sample.set_editor_property("texture", flow_tex)
    
    # Panner for Flow
    panner = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionPanner, -1000, 200
    )
    panner.set_editor_property("speed_x", 0.04)
    panner.set_editor_property("speed_y", 0.08)
    unreal.MaterialEditingLibrary.connect_material_expressions(panner, "", flow_sample, "Coordinates")
    
    # TexCoord for Puff
    tex_coord = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionTextureCoordinate, -600, 0
    )
    
    # Multiply flow distortion with intensity scalar
    distort_mult = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionMultiply, -600, 200
    )
    distort_scalar = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionScalarParameter, -800, 350
    )
    distort_scalar.set_editor_property("parameter_name", "CurlDistortionStrength")
    distort_scalar.set_editor_property("default_value", 0.06)
    
    unreal.MaterialEditingLibrary.connect_material_expressions(flow_sample, "R", distort_mult, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(distort_scalar, "", distort_mult, "B")
    
    # Add distortion to base TexCoord
    uv_add = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionAdd, -400, 100
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(tex_coord, "", uv_add, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(distort_mult, "", uv_add, "B")
    
    # Texture Sample for Pyroclastic Puff
    puff_sample = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionTextureSample, -200, 100
    )
    puff_sample.set_editor_property("texture", puff_tex)
    unreal.MaterialEditingLibrary.connect_material_expressions(uv_add, "", puff_sample, "Coordinates")
    
    # Fresnel node for RDR2 Forward Scattering Rim (Silver Lining)
    fresnel = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionFresnel, -400, -400
    )
    fresnel_exp = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionScalarParameter, -600, -400
    )
    fresnel_exp.set_editor_property("parameter_name", "SilverRimExponent")
    fresnel_exp.set_editor_property("default_value", 2.2)
    unreal.MaterialEditingLibrary.connect_material_expressions(fresnel_exp, "", fresnel, "Exponent")
    
    rim_color = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionVectorParameter, -400, -600
    )
    rim_color.set_editor_property("parameter_name", "SilverRimColor")
    rim_color.set_editor_property("default_value", unreal.LinearColor(1.0, 0.95, 0.85, 1.0))
    
    rim_mult = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionMultiply, -200, -500
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(fresnel, "", rim_mult, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(rim_color, "", rim_mult, "B")
    
    # Smoke Base Tint Parameter
    base_tint = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionVectorParameter, -400, -200
    )
    base_tint.set_editor_property("parameter_name", "SmokeBaseColor")
    base_tint.set_editor_property("default_value", unreal.LinearColor(0.42, 0.42, 0.44, 1.0))
    
    color_mult1 = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionMultiply, -200, -200
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(base_tint, "", color_mult1, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(part_color, "RGB", color_mult1, "B")
    
    # Combine Base Color and Rim Glow
    final_color_add = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionAdd, 0, -200
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(color_mult1, "", final_color_add, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(rim_mult, "", final_color_add, "B")
    
    # Depth Fade for smooth geometry contact (Haveli masonry, ground, chulha stove)
    depth_fade = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionDepthFade, 0, 200
    )
    fade_dist = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionScalarParameter, -200, 350
    )
    fade_dist.set_editor_property("parameter_name", "DepthFadeDistance")
    fade_dist.set_editor_property("default_value", 75.0)
    unreal.MaterialEditingLibrary.connect_material_expressions(fade_dist, "", depth_fade, "FadeDistance")
    
    # Multiply Puff Alpha * Particle Alpha * Depth Fade
    alpha_mult1 = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionMultiply, 0, 50
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(puff_sample, "A", alpha_mult1, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(part_color, "A", alpha_mult1, "B")
    
    final_opacity = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionMultiply, 200, 100
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(alpha_mult1, "", final_opacity, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(depth_fade, "", final_opacity, "B")
    
    # Connect to Material Outputs (Unlit uses EmissiveColor & Opacity)
    unreal.MaterialEditingLibrary.connect_material_property(final_color_add, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    unreal.MaterialEditingLibrary.connect_material_property(final_opacity, "", unreal.MaterialProperty.MP_OPACITY)
    
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_loaded_asset(mat)
    unreal.log_warning("M_RDR2_Pyroclastic_Smoke compiled and saved successfully!")
    return mat

def create_material_instances(master_mat):
    instances = [
        {
            "name": "MI_Smoke_Chulha_Campfire",
            "base_color": unreal.LinearColor(0.55, 0.48, 0.42, 1.0),
            "rim_color": unreal.LinearColor(1.0, 0.75, 0.35, 1.0), # Warm flame bounce
            "curl_strength": 0.07,
            "rim_exp": 1.8,
            "depth_fade": 50.0
        },
        {
            "name": "MI_Smoke_Haveli_Chimney",
            "base_color": unreal.LinearColor(0.35, 0.38, 0.42, 1.0),
            "rim_color": unreal.LinearColor(0.95, 0.98, 1.0, 1.0), # Silver sky lighting
            "curl_strength": 0.05,
            "rim_exp": 2.5,
            "depth_fade": 100.0
        },
        {
            "name": "MI_Smoke_Gunpowder_Muzzle",
            "base_color": unreal.LinearColor(0.70, 0.70, 0.72, 1.0),
            "rim_color": unreal.LinearColor(1.0, 0.95, 0.80, 1.0),
            "curl_strength": 0.12,
            "rim_exp": 1.5,
            "depth_fade": 30.0
        }
    ]
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialInstanceConstantFactoryNew()
    mat_path = "/Game/VFX/Smoke/Materials"
    
    for info in instances:
        inst_path = f"{mat_path}/{info['name']}"
        inst = unreal.EditorAssetLibrary.load_asset(inst_path)
        if not inst:
            inst = asset_tools.create_asset(info['name'], mat_path, unreal.MaterialInstanceConstant, factory)
        if inst:
            inst.set_editor_property("parent", master_mat)
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
                inst, "SmokeBaseColor", info["base_color"]
            )
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
                inst, "SilverRimColor", info["rim_color"]
            )
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
                inst, "CurlDistortionStrength", info["curl_strength"]
            )
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
                inst, "SilverRimExponent", info["rim_exp"]
            )
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
                inst, "DepthFadeDistance", info["depth_fade"]
            )
            unreal.MaterialEditingLibrary.update_material_instance(inst)
            unreal.EditorAssetLibrary.save_loaded_asset(inst)
            unreal.log_warning(f"Created & configured Material Instance: {info['name']}")

def main():
    unreal.log_warning("=== Building RDR2-Inspired Smoke Pipeline in Unreal Engine 5.5 ===")
    
    puff_tga = r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Content\VFX\Smoke\Textures\T_Smoke_Pyroclastic_Puff.tga"
    flow_tga = r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Content\VFX\Smoke\Textures\T_Smoke_CurlNoise_Flow.tga"
    dest_path = "/Game/VFX/Smoke/Textures"
    
    puff_tex = import_texture(puff_tga, dest_path, srgb=True, is_normal=False)
    flow_tex = import_texture(flow_tga, dest_path, srgb=False, is_normal=False)
    
    if not puff_tex or not flow_tex:
        unreal.log_error("Failed to import smoke textures!")
        return
        
    master_mat = create_rdr2_smoke_material(puff_tex, flow_tex)
    if master_mat:
        create_material_instances(master_mat)
        unreal.log_warning("=== RDR2 Smoke Materials Setup Complete! ===")

if __name__ == "__main__":
    main()
