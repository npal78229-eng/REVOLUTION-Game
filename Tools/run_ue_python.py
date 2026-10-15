import sys
import time
import os

sys.path.append("C:/Program Files/Epic Games/UE_5.5/Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python")
import remote_execution

def main():
    if len(sys.argv) < 2:
        print("Usage: run_ue_python.py <script_path_or_command>")
        sys.exit(1)

    cfg = remote_execution.RemoteExecutionConfig()
    cfg.multicast_bind_address = "0.0.0.0"
    client = remote_execution.RemoteExecution(cfg)
    client.start()
    time.sleep(2.0)

    if not client.remote_nodes:
        print("[ERROR] No running Unreal Editor nodes found on multicast 239.0.0.1:6766!")
        client.stop()
        sys.exit(1)

    node = client.remote_nodes[0]
    node_id = node["node_id"]
    client.open_command_connection(node_id)
    time.sleep(0.5)

    if not client.has_command_connection():
        print(f"[ERROR] Failed to connect to Unreal node {node_id}")
        client.stop()
        sys.exit(1)

    if os.path.exists(target):
        print(f"[INFO] Executing script file: {target}")
        with open(target, "r", encoding="utf-8") as f:
            code = f.read()
        res = client.run_command(code, exec_mode=remote_execution.MODE_EXEC_FILE)
    else:
        print(f"[INFO] Executing statement: {target}")
        res = client.run_command(target, exec_mode=remote_execution.MODE_EXEC_STATEMENT)

    print("[RESULT]", res)
    client.close_command_connection()
    client.stop()

if __name__ == "__main__":
    main()
