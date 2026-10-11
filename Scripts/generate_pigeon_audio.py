"""
PROJECT REVOLUTION — HISTORICAL HAVELI ROOFTOP PIGEON AUDIO SYNTHESIZER
Synthesizes period-authentic acoustic Foley for Kot Gurdarshan haveli rooftop pigeons (kabootar):
1. SFX_Pigeon_Flock_Scatter.wav - Sudden explosive flurry of panicked wing-beats, feather fluttering, and alarmed guttural coos echoing off brick parapets.
2. SFX_Pigeon_Coo_Calm.wav      - Gentle, calm nocturnal throat cooing of roosting haveli pigeons on parapet ledges.

Output: 16-bit 44.1kHz mono PCM WAV files in Art/Audio/
"""

import math
import os
import random
import struct
import wave

SAMPLE_RATE = 44100
OUT_DIR = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"

def write_wav(filename, samples):
    os.makedirs(OUT_DIR, exist_ok=True)
    filepath = os.path.join(OUT_DIR, filename)
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        
        raw_bytes = bytearray()
        for s in samples:
            s_clamped = max(-1.0, min(1.0, s))
            val = int(s_clamped * 32767.0)
            raw_bytes.extend(struct.pack("<h", val))
            
        wav_file.writeframes(raw_bytes)
    print(f"Generated {filename}: {len(samples)/SAMPLE_RATE:.2f}s ({len(raw_bytes)} bytes)")

def generate_pigeon_scatter():
    """Panicked explosion of pigeon flock wing-flapping, air turbulence, and alarmed flutter."""
    duration = 1.85
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    random.seed(303)
    
    # 28 overlapping wing flaps across the flock
    flaps = []
    t_cursor = 0.02
    for _ in range(32):
        flaps.append(t_cursor)
        t_cursor += random.uniform(0.03, 0.08)
        
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        sample_val = 0.0
        
        # Wing flap impulses
        for flap_t in flaps:
            if t >= flap_t:
                dt = t - flap_t
                if dt < 0.09:
                    # Low aerodynamic thump (80-140Hz)
                    flap_thump = math.sin(2.0 * math.pi * (110.0 - 30.0 * dt) * dt) * 0.35 * math.exp(-dt * 40.0)
                    # High feather rustle / air turbulence (noise burst)
                    feather_noise = (random.random() * 2.0 - 1.0) * 0.40 * math.exp(-dt * 55.0)
                    sample_val += flap_thump + feather_noise
                    
        # Overall flock envelope: sudden sharp peak at start, gradual decay as they fly away
        env_overall = math.exp(-t * 2.2) * (1.0 - math.exp(-t * 35.0))
        
        # Alarmed cooing tones rising in pitch
        alarm_coo = 0.0
        if 0.15 <= t <= 0.8:
            coo_t = t - 0.15
            coo_freq = 320.0 + 80.0 * math.sin(coo_t * 25.0)
            alarm_coo = math.sin(2.0 * math.pi * coo_freq * coo_t) * 0.15 * math.sin((t - 0.15) / 0.65 * math.pi)
            
        # Continuous air whoosh as flock ascends
        air_whoosh = (random.random() * 2.0 - 1.0) * 0.12 * math.exp(-t * 1.8)
        
        total = (sample_val * 0.75 + alarm_coo + air_whoosh) * env_overall * 1.4
        samples[i] = max(-1.0, min(1.0, total))
        
    return samples

def generate_pigeon_coo_calm():
    """Gentle, nocturnal throaty coo of sleeping haveli rooftop pigeons."""
    duration = 1.25
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    random.seed(505)
    
    # 2 calm cooing syllables (e.g. "coo-ROOO-coo")
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        coo = 0.0
        # Syllable 1: 0.1s to 0.45s
        if 0.10 <= t <= 0.45:
            dt = t - 0.10
            env = math.sin((dt / 0.35) * math.pi) ** 1.8
            freq = 240.0 + 35.0 * math.sin(dt * 15.0)
            coo += (math.sin(2.0 * math.pi * freq * dt) * 0.4 + \
                    math.sin(2.0 * math.pi * freq * 2.0 * dt) * 0.15) * env
                    
        # Syllable 2: 0.55s to 1.05s
        if 0.55 <= t <= 1.05:
            dt = t - 0.55
            env = math.sin((dt / 0.50) * math.pi) ** 1.5
            freq = 210.0 + 25.0 * math.sin(dt * 12.0)
            coo += (math.sin(2.0 * math.pi * freq * dt) * 0.45 + \
                    math.sin(2.0 * math.pi * freq * 2.0 * dt) * 0.12) * env
                    
        # Soft body breath noise
        breath = (random.random() * 2.0 - 1.0) * 0.025
        samples[i] = (coo + breath) * 0.75
        
    return samples

def main():
    print("Synthesizing Haveli Rooftop Pigeon Foley for Project REVOLUTION...")
    write_wav("SFX_Pigeon_Flock_Scatter.wav", generate_pigeon_scatter())
    write_wav("SFX_Pigeon_Coo_Calm.wav", generate_pigeon_coo_calm())
    print("All pigeon audio assets generated successfully!")

if __name__ == "__main__":
    main()
