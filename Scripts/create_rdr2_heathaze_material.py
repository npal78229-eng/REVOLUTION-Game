import unreal

def create_heathaze_material():
    mat_path = "/Game/VFX/Smoke/Materials"
    mat_name = "M_RDR2_HeatHaze"
    full_path = f"{mat_path}/{mat_name}"
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_factory = unreal.MaterialFactoryNew()
    
    mat = unreal.EditorAssetLibrary.load_asset(full_path)
    if not mat:
        mat = asset_tools.create_asset(mat_name, mat_path, unreal.Material, material_factory)
        
    if not mat:
        unreal.log_error("Failed to create M_RDR2_HeatHaze!")
        return False
        
    mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    mat.set_editor_property("two_sided", True)
    
    flow_tex = unreal.load_asset("/Game/VFX/Smoke/Textures/T_Smoke_CurlNoise_Flow")
    
    # 1. Panner node for rising heat convection
    panner = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionPanner, -800, 0
    )
    panner.set_editor_property("speed_x", 0.02)
    panner.set_editor_property("speed_y", -0.18) # Fast upward convection
    
    # 2. Texture Sample for Curl Flow Map
    flow_sample = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionTextureSample, -600, 0
    )
    if flow_tex:
        flow_sample.set_editor_property("texture", flow_tex)
    unreal.MaterialEditingLibrary.connect_material_expressions(panner, "", flow_sample, "Coordinates")
    
    # 3. Distortion scalar parameter
    distort_scalar = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionScalarParameter, -600, 200
    )
    distort_scalar.set_editor_property("parameter_name", "HeatRefractionStrength")
    distort_scalar.set_editor_property("default_value", 0.045)
    
    # 4. Subtract 0.5 to center displacement around 0 (-0.5 to +0.5)
    sub_half = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionSubtract, -400, 0
    )
    half_const = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionConstant, -600, 100
    )
    half_const.set_editor_property("r", 0.5)
    unreal.MaterialEditingLibrary.connect_material_expressions(flow_sample, "R", sub_half, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(half_const, "", sub_half, "B")
    
    # 5. Multiply by Distortion Strength
    mult_strength = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionMultiply, -200, 0
    )
    unreal.MaterialEditingLibrary.connect_material_expressions(sub_half, "", mult_strength, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(distort_scalar, "", mult_strength, "B")
    
    # 6. Add 1.0 (Base Refraction Index of air = 1.0)
    add_air = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionAdd, 0, 0
    )
    one_const = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionConstant, -200, 100
    )
    one_const.set_editor_property("r", 1.0)
    unreal.MaterialEditingLibrary.connect_material_expressions(mult_strength, "", add_air, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(one_const, "", add_air, "B")
    
    # 7. Radial Falloff (Fresnel / Sphere Mask) so heat haze edges are soft
    tex_coord = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionTextureCoordinate, -600, -200
    )
    dist_to_center = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionDistance, -400, -200
    )
    center_point = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionConstant2Vector, -600, -350
    )
    center_point.set_editor_property("r", 0.5)
    center_point.set_editor_property("g", 0.5)
    unreal.MaterialEditingLibrary.connect_material_expressions(tex_coord, "", dist_to_center, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(center_point, "", dist_to_center, "B")
    
    # Connect to Material Properties:
    # In UE5 Translucent Unlit, Refraction is MaterialProperty.MP_REFRACTION
    unreal.MaterialEditingLibrary.connect_material_property(add_air, "", unreal.MaterialProperty.MP_REFRACTION)
    
    # Set Emissive to 0
    zero_const = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionConstant, 0, -200
    )
    zero_const.set_editor_property("r", 0.0)
    unreal.MaterialEditingLibrary.connect_material_property(zero_const, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    
    # Opacity = 0.0 (Pure refractive distortion without tint)
    unreal.MaterialEditingLibrary.connect_material_property(zero_const, "", unreal.MaterialProperty.MP_OPACITY)
    
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_loaded_asset(mat)
    unreal.log_warning("M_RDR2_HeatHaze compiled and saved successfully!")
    return True

if __name__ == "__main__":
    create_heathaze_material()
