import unreal

def log(msg):
    unreal.log_warning(f"[INSPECT_GRAPHS] {msg}")

for bp_path in ["/Game/Blueprints/BP_Mohalla_Daytime_GameMode", "/Game/Characters/Kabir/BP_Kabir"]:
    asset = unreal.EditorAssetLibrary.load_asset(bp_path)
    if not asset:
        log(f"Could not load {bp_path}")
        continue
    log(f"Inspecting Blueprint: {bp_path}")
    # Inspect graphs
    uber_graph_pages = asset.get_editor_property("uber_graph_pages")
    log(f"  UberGraph pages count: {len(uber_graph_pages)}")
    for ug in uber_graph_pages:
        nodes = ug.get_editor_property("nodes")
        log(f"  Page '{ug.get_name()}' has {len(nodes)} nodes")
        for n in nodes:
            log(f"    - Node: {n.get_name()} ({n.get_class().get_name()}) title='{n.get_node_title(0)}'")

    func_graphs = asset.get_editor_property("function_graphs")
    log(f"  Function graphs count: {len(func_graphs)}")
    for fg in func_graphs:
        log(f"    - Function: {fg.get_name()}")
