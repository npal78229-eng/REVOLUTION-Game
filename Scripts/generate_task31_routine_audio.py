"""
PROJECT REVOLUTION — Task 31 Audio Synthesis: Civilian NPC Occupational Routine Foley Loops
Generates 6 authentic period foley loops corresponding to the daily life routines of Kot Gurdarshan's residents:
1. SFX_Routine_SewingMachine_Loop.wav (Ram Lubhaya - cast iron Singer 1910s sewing machine cadence)
2. SFX_Routine_ChaiStir_Loop.wav (Hira Halwai - copper karahi simmering and brass spoon stirring)
3. SFX_Routine_MashkWater_Loop.wav (Ghasita Bhishti - goatskin mashk slosh, well rope creak, water drops)
4. SFX_Routine_ClothMerchant_Loop.wav (Lala Karam Chand - khadi weave handling, wooden yardstick tap)
5. SFX_Routine_Schoolmaster_Loop.wav (Pandit Kashi Ram - slate pencil chalkboard scratch, ledger turn)
6. SFX_Routine_KartarKite_Loop.wav (Kartar Singh - fighter kite manja twine hum, wooden spool spin)
"""

import math
import struct
import wave
import os
import random

SAMPLE_RATE = 44100

def write_wav(filename, samples):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        
        packed_samples = bytearray()
        for sample in samples:
            clamped = max(-1.0, min(1.0, sample))
            val = int(clamped * 32767.0)
            packed_samples.extend(struct.pack('<h', val))
        wav_file.writeframes(packed_samples)
    print(f"Synthesized: {filename} ({len(samples)} samples, {len(samples)/SAMPLE_RATE:.2f}s)")

def generate_sewing_machine_loop(duration=3.0):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    # Treadle & needle frequency: ~5.5 Hz
    needle_freq = 5.5
    for i in range(total):
        t = i / SAMPLE_RATE
        # Low frequency wheel whir
        wheel = math.sin(2 * math.pi * 32.0 * t) * 0.12 + math.sin(2 * math.pi * 64.0 * t) * 0.08
        # Needle strike impulse
        phase = (t * needle_freq) % 1.0
        needle = 0.0
        if phase < 0.08:
            strike_t = phase / 0.08
            needle = math.sin(strike_t * math.pi * 18.0) * math.exp(-strike_t * 6.0) * 0.45
            needle += (random.random() * 2.0 - 1.0) * 0.15 * math.exp(-strike_t * 8.0)
        # Shuttle click
        shuttle_phase = ((t * needle_freq) + 0.5) % 1.0
        shuttle = 0.0
        if shuttle_phase < 0.06:
            st = shuttle_phase / 0.06
            shuttle = math.sin(st * math.pi * 12.0) * math.exp(-st * 8.0) * 0.25
        samples[i] = wheel + needle + shuttle
    return samples

def generate_chai_stir_loop(duration=3.0):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    for i in range(total):
        t = i / SAMPLE_RATE
        # Simmering liquid bed (low-pass filtered white noise)
        simmer = (random.random() * 2.0 - 1.0) * 0.08
        # Gentle bubble pops
        bubble = 0.0
        if random.random() < 0.008:
            pop_freq = 240.0 + random.random() * 180.0
            bubble = math.sin(2 * math.pi * pop_freq * t) * 0.22
        # Metallic spoon scraping along copper karahi (circular ~0.8 Hz)
        stir_phase = math.sin(2 * math.pi * 0.8 * t)
        metal_scrape = 0.0
        if stir_phase > 0.2:
            metal_scrape = (math.sin(2 * math.pi * 1850.0 * t) * 0.06 + math.sin(2 * math.pi * 3200.0 * t) * 0.04) * (stir_phase - 0.2)
        samples[i] = simmer + bubble + metal_scrape
    return samples

def generate_mashk_water_loop(duration=3.0):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    for i in range(total):
        t = i / SAMPLE_RATE
        # Heavy sloshing liquid in leather
        slosh = math.sin(2 * math.pi * 1.2 * t) * math.sin(2 * math.pi * 120.0 * t) * 0.18
        # Leather creak (dry friction)
        creak_env = max(0.0, math.sin(2 * math.pi * 0.6 * t))
        creak = math.sin(2 * math.pi * 480.0 * t) * (random.random() * 0.10) * creak_env
        # Occasional droplet
        drop = 0.0
        if random.random() < 0.003:
            drop_f = 650.0 + random.random() * 400.0
            drop = math.sin(2 * math.pi * drop_f * t) * 0.35
        samples[i] = slosh + creak + drop
    return samples

def generate_cloth_merchant_loop(duration=3.0):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    for i in range(total):
        t = i / SAMPLE_RATE
        # Soft textile khadi rustling
        rustle_env = max(0.0, math.sin(2 * math.pi * 0.75 * t))
        rustle = (random.random() * 2.0 - 1.0) * 0.12 * rustle_env
        # Wooden yardstick tap against table every 1.5s
        tap_phase = (t / 1.5) % 1.0
        tap = 0.0
        if tap_phase < 0.04:
            tt = tap_phase / 0.04
            tap = math.sin(tt * math.pi * 8.0) * math.exp(-tt * 7.0) * 0.38
        samples[i] = rustle + tap
    return samples

def generate_schoolmaster_loop(duration=3.0):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    for i in range(total):
        t = i / SAMPLE_RATE
        # Slate pencil scratch on chalkboard
        scratch_env = max(0.0, math.sin(2 * math.pi * 1.1 * t))
        scratch = (math.sin(2 * math.pi * 2400.0 * t) * 0.09 + math.sin(2 * math.pi * 4100.0 * t) * 0.05) * scratch_env
        # Paper page turn flutter
        page_phase = (t / 2.8) % 1.0
        page = 0.0
        if page_phase < 0.08:
            pt = page_phase / 0.08
            page = (random.random() * 2.0 - 1.0) * 0.18 * math.sin(pt * math.pi)
        samples[i] = scratch + page
    return samples

def generate_kartar_kite_loop(duration=3.0):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    for i in range(total):
        t = i / SAMPLE_RATE
        # High-pitched manja twine singing in wind
        twine = math.sin(2 * math.pi * 880.0 * t) * 0.08 + math.sin(2 * math.pi * 1760.0 * t) * 0.04
        twine *= (0.7 + 0.3 * math.sin(2 * math.pi * 2.5 * t))
        # Wooden charkhi spool whir / rattle
        spool_phase = (t * 4.0) % 1.0
        spool = 0.0
        if spool_phase < 0.12:
            st = spool_phase / 0.12
            spool = math.sin(st * math.pi * 10.0) * 0.14
        samples[i] = twine + spool
    return samples

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(base_dir, "Art", "Audio", "SFX", "Routines")
    os.makedirs(out_dir, exist_ok=True)

    tracks = [
        ("SFX_Routine_SewingMachine_Loop.wav", generate_sewing_machine_loop()),
        ("SFX_Routine_ChaiStir_Loop.wav", generate_chai_stir_loop()),
        ("SFX_Routine_MashkWater_Loop.wav", generate_mashk_water_loop()),
        ("SFX_Routine_ClothMerchant_Loop.wav", generate_cloth_merchant_loop()),
        ("SFX_Routine_Schoolmaster_Loop.wav", generate_schoolmaster_loop()),
        ("SFX_Routine_KartarKite_Loop.wav", generate_kartar_kite_loop())
    ]

    for fname, smps in tracks:
        write_wav(os.path.join(out_dir, fname), smps)

    print("Task 31 Routine Foley loops synthesis 100% COMPLETE.")

if __name__ == "__main__":
    main()
