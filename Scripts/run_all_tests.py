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
            "name": "Act I Narrative Story Questline & Landmarks (205 Actors)",
            "script": os.path.join(scripts_dir, "verify_act1_questline.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-05",
            "name": "Story Subsystem State Machine & 29-Stage Progression Suite",
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
        },
        {
            "id": "TEST-10",
            "name": "Advanced Photogrammetry Texturing & Material Architecture",
            "script": os.path.join(scripts_dir, "verify_photogrammetry_materials.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-11",
            "name": "Historical Narrative Epilogue, Codex 18th Record & Cinematic Director",
            "script": os.path.join(scripts_dir, "verify_task25_epilogue.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-12",
            "name": "Multi-Dialect Punjabi Voice Recording Expansion & Bazaar Walla System",
            "script": os.path.join(scripts_dir, "verify_task26_multidialect_walla.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-13",
            "name": "Dynamic Time-of-Day Weather States, Andhi Dust Storm & Volumetric Fog",
            "script": os.path.join(scripts_dir, "verify_task27_weather_states.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-14",
            "name": "Curfew Sentry AI Collision Resolution & 3-Waypoint Patrol Routine",
            "script": os.path.join(scripts_dir, "verify_curfew_patrol.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-15",
            "name": "Frontend Title Screen, Pause Menu System & Checkpoint Restart Loop",
            "script": os.path.join(scripts_dir, "verify_frontend_menus.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-16",
            "name": "Persistent Disk Save/Load System (USaveGame) & Continue Journey Loop",
            "script": os.path.join(scripts_dir, "verify_save_load_system.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-17",
            "name": "Procedural Skeletal Idle Animations, Occupational Routine Life & Heritage Attire",
            "script": os.path.join(scripts_dir, "verify_civilian_routines.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-18",
            "name": "Haveli Ground Floor Domestic Dressing & Village Exploration Boundaries",
            "script": os.path.join(scripts_dir, "verify_haveli_boundaries.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-19",
            "name": "Rooftop Traversal, Vertical Ladder Traversal & Mantling Feedback",
            "script": os.path.join(scripts_dir, "verify_rooftop_traversal.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-20",
            "name": "Seamless Act I In-World Objective Beacons & Mohalla Compass Waypoints",
            "script": os.path.join(scripts_dir, "verify_objective_beacons.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-21",
            "name": "Act I Finale to Act II Cinematic Handoff & Munadi Proclamation Sequence",
            "script": os.path.join(scripts_dir, "verify_act1_to_act2_handoff.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-22",
            "name": "Grand Bazaar Chowk Munadi Crowd Clatter & Dynamic Dialogue System",
            "script": os.path.join(scripts_dir, "verify_chowk_munadi_crowd.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-23",
            "name": "Act II Questline: 'The Rumors of Baisakhi' & Checkpost Eavesdropping",
            "script": os.path.join(scripts_dir, "verify_act2_questline.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-24",
            "name": "Baisakhi Fair Ground Atmosphere & Gathering Expansion",
            "script": os.path.join(scripts_dir, "verify_baisakhi_fairground.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-25",
            "name": "RDR2-Inspired Volumetric Smoke, Curl Noise Flow & Atmospheric Optics",
            "script": os.path.join(scripts_dir, "verify_rdr2_smoke_integration.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-26",
            "name": "Act II Climax: The Firing Line at Jallianwala Bagh & Escape Traversal",
            "script": os.path.join(scripts_dir, "verify_act2_climax_firing_line.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-27",
            "name": "Act III: The Desolate Night & Clandestine Medical Evacuation",
            "script": os.path.join(scripts_dir, "verify_act3_medical_evacuation.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-28",
            "name": "Act IV: The Rural Outskirts & Upper Bari Doab Canal Feeder Network",
            "script": os.path.join(scripts_dir, "verify_act4_canal_outskirts.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-29",
            "name": "Act IV Climax: Bhatta Brick Kiln Resistance Infiltration & Underground Press",
            "script": os.path.join(scripts_dir, "verify_act4_climax_brick_kiln.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-30",
            "name": "Act V: North Western Railway Cutting, Signal Gantry & Locomotive Climax",
            "script": os.path.join(scripts_dir, "verify_act5_railway_climax.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-31",
            "name": "Community-Trust System ('Izzat & Vishwas') & Localized Reputation",
            "script": os.path.join(scripts_dir, "verify_community_trust.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-32",
            "name": "End-to-End Interactive QA Playthrough Bot & 29-Stage Telemetry",
            "script": os.path.join(scripts_dir, "verify_e2e_interactive_playthrough.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-33",
            "name": "Extended Soak & Memory Stability Verification (300 Cycles)",
            "script": os.path.join(scripts_dir, "verify_extended_soak_test.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-34",
            "name": "Hardware Scalability & Multi-Tier GPU Compatibility Matrix",
            "script": os.path.join(scripts_dir, "verify_hardware_scalability_matrix.py"),
            "type": "commandlet"
        },
        {
            "id": "TEST-35",
            "name": "Win64 Shipping Distribution Security & Cryptographic Integrity",
            "script": os.path.join(scripts_dir, "verify_distribution_manifest.py"),
            "type": "python"
        },
        {
            "id": "TEST-36",
            "name": "Multi-Language Localization Coverage & UTF-8 Text Integrity Audit",
            "script": os.path.join(scripts_dir, "verify_localization_coverage.py"),
            "type": "python"
        }
    ]

    results = []
    start_time = time.time()
    all_passed = True

    summary_path = os.path.join(scripts_dir, "ci_master_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"PROJECT REVOLUTION CI RUN STARTED: {time.ctime()}\n\n")

    for test in test_suites:
        print("\n--------------------------------------------------------------------------------", flush=True)
        print(f"[{test['id']}] Running: {test['name']}...", flush=True)
        print(f"  Script: {test['script']}", flush=True)

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
        # Transient lock failure retry for headless editor commandlet
        if res.returncode != 0 and test["type"] == "commandlet":
            time.sleep(2.0)
            res = subprocess.run(cmd, capture_output=True, text=True)

        elapsed = round(time.time() - t0, 2)
        status = "PASS" if res.returncode == 0 else "FAIL"
        time.sleep(0.5)

        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(f"[{test['id']}] {test['name']} -> {status} (Exit {res.returncode}) in {elapsed}s\n")
            if res.returncode != 0:
                f.write("  --- STDOUT TAIL ---\n")
                for line in res.stdout.strip().split("\n")[-15:]:
                    f.write(f"    {line}\n")
                f.write("  --- STDERR TAIL ---\n")
                for line in res.stderr.strip().split("\n")[-15:]:
                    f.write(f"    {line}\n")
            f.flush()

        if res.returncode != 0:
            all_passed = False
            print(f"  -> Result: {status} (Exit Code: {res.returncode}) in {elapsed}s", flush=True)
            # print last 10 lines of output for debugging
            lines = res.stdout.strip().split("\n")
            for line in lines[-10:]:
                print(f"     {line}", flush=True)
        else:
            print(f"  -> Result: {status} (Exit Code: 0) in {elapsed}s", flush=True)

        results.append({
            "id": test["id"],
            "name": test["name"],
            "status": status,
            "duration": f"{elapsed}s",
            "exit_code": res.returncode
        })

    total_elapsed_min = round((time.time() - start_time) / 60.0, 2)

    print("\n================================================================================", flush=True)
    print("  PROJECT REVOLUTION — MASTER CI VERIFICATION SUMMARY REPORT", flush=True)
    print("================================================================================", flush=True)
    print(f"{'ID':<10} {'STATUS':<8} {'DURATION':<10} {'TEST SUITE NAME'}", flush=True)
    print("-" * 80, flush=True)
    for r in results:
        print(f"{r['id']:<10} {r['status']:<8} {r['duration']:<10} {r['name']}", flush=True)
    print("-" * 80, flush=True)

    with open(summary_path, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write("  PROJECT REVOLUTION — MASTER CI VERIFICATION SUMMARY REPORT\n")
        f.write("=" * 80 + "\n")
        for r in results:
            f.write(f"{r['id']:<10} {r['status']:<8} {r['duration']:<10} {r['name']}\n")
        f.write("-" * 80 + "\n")

    if all_passed:
        pass_count = len([r for r in results if r['status'] == 'PASS'])
        msg = f"  OVERALL RESULT: 100% PASS ({pass_count}/{len(test_suites)} SUITES PASSED) in {total_elapsed_min} minutes!\n  ALL {len(test_suites)} AUTOMATED CI VERIFICATION SUITES COMPLETED SUCCESSFULLY."
        print("================================================================================", flush=True)
        print(msg, flush=True)
        print("================================================================================", flush=True)
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n" + "=" * 80 + "\n")
        return 0
    else:
        fail_count = len([r for r in results if r['status'] == 'FAIL'])
        msg = f"  OVERALL RESULT: {fail_count} SUITE(S) FAILED out of {len(test_suites)}!"
        print("================================================================================", flush=True)
        print(msg, flush=True)
        print("================================================================================", flush=True)
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n" + "=" * 80 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
