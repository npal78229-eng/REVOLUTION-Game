"""
PROJECT REVOLUTION — Master Continuous Integration (CI) Test Harness (Python)
Executes all 6 QA verification suites in sequence and prints a unified audit report.
"""

import os
import sys
import time
import subprocess

def main():
    print("================================================================================")
    print("  PROJECT REVOLUTION — MASTER CONTINUOUS INTEGRATION (CI) TEST HARNESS")
    print("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    project_path = os.path.join(base_dir, "Project", "REVOLUTION.uproject")
    scripts_dir = os.path.join(base_dir, "Scripts")

    ue_cmd = r"C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
    ue_python = r"C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\ThirdParty\Python3\Win64\python.exe"

    test_suites = [
        {
            "id": "TEST-01",
            "name": "Quality-of-Life, Satchel Modal & Historical Codex",
            "script": os.path.join(scripts_dir, "verify_qol_and_codex.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-02",
            "name": "Audio Mix, SoundClass Hierarchy & Dynamic Curfew Filter",
            "script": os.path.join(scripts_dir, "verify_audio_mix.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-03",
            "name": "Cinematic Camera Sequences & C++ Director Actor",
            "script": os.path.join(scripts_dir, "verify_cinematic_sequences.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-04",
            "name": "Act I Narrative Story Questline & Landmarks (206 Actors)",
            "script": os.path.join(scripts_dir, "verify_act1_questline.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-05",
            "name": "Master PIE & Story Simulation (27 Milestones across Acts I-V)",
            "script": os.path.join(scripts_dir, "verify_pie_master_walkthrough.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-06",
            "name": "Standalone Build Cook, IoStore Packaging & GTX 1650 Budget",
            "script": os.path.join(scripts_dir, "verify_standalone_package.py"),
            "type": "python"
        },
        {
            "id": "TEST-07",
            "name": "Civilian Dialogue Voice Localization & Ambient Proximity Audio",
            "script": os.path.join(scripts_dir, "verify_civilian_voice_localization.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-08",
            "name": "Pedestrian Reaction, Dynamic Stumble & Curiosity System",
            "script": os.path.join(scripts_dir, "verify_pedestrian_reactions.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-09",
            "name": "SteamOS & Handheld Proton Scalability Profile & Controller Mappings",
            "script": os.path.join(scripts_dir, "verify_steamos_handheld_profile.py"),
            "type": "commandlet"
        }
    ]

    results = []
    start_time = time.time()
    all_passed = True

    for test in test_suites:
        print("\n--------------------------------------------------------------------------------")
        print(f"[{test['id']}] Running: {test['name']}...")
        print(f"  Script: {test['script']}")

        t0 = time.time()
        if test["type"] == "commandlet":
            cmd = [
                ue_cmd,
                project_path,
                "-run=pythonscript",
                f"-script={test['script']}",
                "-stdout",
                "-unattended",
                "-NullRHI"
            ]
        else:
            cmd = [
                ue_python,
                test["script"]
            ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = round(time.time() - t0, 2)
        status = "PASS" if res.returncode == 0 else "FAIL"

        if res.returncode != 0:
            all_passed = False
            print(f"  -> Result: {status} (Exit Code: {res.returncode}) in {elapsed}s")
            # print last 10 lines of output for debugging
            lines = res.stdout.strip().split("\n")
            for line in lines[-10:]:
                print(f"     {line}")
        else:
            print(f"  -> Result: {status} (Exit Code: 0) in {elapsed}s")

        results.append({
            "id": test["id"],
            "name": test["name"],
            "status": status,
            "duration": f"{elapsed}s",
            "exit_code": res.returncode
        })

    total_elapsed_min = round((time.time() - start_time) / 60.0, 2)

    print("\n================================================================================")
    print("  PROJECT REVOLUTION — MASTER CI VERIFICATION SUMMARY REPORT")
    print("================================================================================")
    print(f"{'ID':<10} {'STATUS':<8} {'DURATION':<10} {'TEST SUITE NAME'}")
    print("-" * 80)
    for r in results:
        print(f"{r['id']:<10} {r['status']:<8} {r['duration']:<10} {r['name']}")
    print("-" * 80)

    if all_passed:
        pass_count = len([r for r in results if r['status'] == 'PASS'])
        print("================================================================================")
        print(f"  OVERALL RESULT: 100% PASS ({pass_count}/{len(test_suites)} SUITES PASSED) in {total_elapsed_min} minutes!")
        print("  PROJECT REVOLUTION IS CERTIFIED GOLD MASTER READY!")
        print("================================================================================")
        return 0
    else:
        print("================================================================================")
        print("  OVERALL RESULT: ONE OR MORE SUITES FAILED!")
        print("================================================================================")
        return 1

if __name__ == "__main__":
    sys.exit(main())
