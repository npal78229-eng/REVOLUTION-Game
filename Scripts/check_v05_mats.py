import unreal

skm_v05 = unreal.load_asset("/Game/Characters/Kabir_v05/SKM_Kabir_v05")
mats_v05 = skm_v05.get_editor_property("materials")
for i, m in enumerate(mats_v05):
    unreal.log_warning(f"v05 Slot [{i}] {m.material_slot_name}: {m.material_interface.get_name() if m.material_interface else 'None'}")
