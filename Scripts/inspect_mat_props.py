import unreal

mat_path = "/Game/Environment/Mohalla/Materials/M_ClothIndigo_PBR"
mat = unreal.EditorAssetLibrary.load_asset(mat_path)
unreal.log_warning(f"Loaded {mat.get_name()}, class={mat.get_class().get_name()}")

for p in dir(mat):
    if "mesh" in p.lower() or "skeletal" in p.lower() or "usage" in p.lower() or "used" in p.lower():
        unreal.log_warning(f"Prop: {p}")
