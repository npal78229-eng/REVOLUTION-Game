"""
PROJECT REVOLUTION — Task 33 Audio Synthesis: Ladder Rung Creak & Dismount Foley
Generates authentic period foley audio for vertical ladder traversal:
1. SFX_Ladder_Rung_Creak.wav (Sal timber / bamboo rung creak under climbing footstep)
2. SFX_Ladder_Dismount.wav (Solid terrace brick/wood dismount step)
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

def generate_ladder_rung_creak(duration=1.4):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    
    # 3 distinct climbing footstep rung creaks
    steps = [0.15, 0.55, 0.95]
    for step_start in steps:
        step_idx = int(step_start * SAMPLE_RATE)
        step_len = int(0.28 * SAMPLE_RATE)
        for i in range(step_len):
            idx = step_idx + i
            if idx >= total:
                break
            t = i / SAMPLE_RATE
            env = math.sin(t / 0.28 * math.pi) * math.exp(-t * 8.0)
            # Low wood resonance (110 - 220 Hz) + high creak friction (800 - 1600 Hz)
            f_low = 140.0 + random.uniform(-15.0, 15.0)
            f_creak = 1100.0 + math.sin(t * 45.0) * 350.0
            
            wood = math.sin(2.0 * math.pi * f_low * t) * 0.45
            creak = math.sin(2.0 * math.pi * f_creak * t) * 0.25 * math.sin(t * 90.0)
            thump = (random.random() * 2.0 - 1.0) * 0.15 * math.exp(-t * 22.0)
            
            samples[idx] += (wood + creak + thump) * env * 0.85
            
    return samples

def generate_ladder_dismount(duration=0.8):
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total
    
    # Solid landing footstep on brick/timber terrace slab
    impact_len = int(0.45 * SAMPLE_RATE)
    for i in range(impact_len):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 14.0)
        # Heavy low thud (85 Hz) + masonry scrape
        thud = math.sin(2.0 * math.pi * 85.0 * t) * 0.65
        masonry = (random.random() * 2.0 - 1.0) * 0.30 * math.exp(-t * 25.0)
        scrape = math.sin(2.0 * math.pi * 520.0 * t) * 0.15 * math.exp(-t * 18.0)
        samples[i] = (thud + masonry + scrape) * env * 0.90
        
    return samples

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(base_dir, "Art", "Audio", "SFX")
    
    rung_path = os.path.join(out_dir, "SFX_Ladder_Rung_Creak.wav")
    dismount_path = os.path.join(out_dir, "SFX_Ladder_Dismount.wav")
    
    write_wav(rung_path, generate_ladder_rung_creak())
    write_wav(dismount_path, generate_ladder_dismount())
    print("Ladder audio synthesis complete.")

if __name__ == "__main__":
    main()
