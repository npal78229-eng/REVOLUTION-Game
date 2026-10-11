"""
PROJECT REVOLUTION — ENVIRONMENTAL SOUND MASKING & CONCEALMENT AUDIO SYNTHESIZER
Synthesizes 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Train_Distant_Rumble: North Western Railway steam locomotive rumble & distant whistle (4.2s)
2. SFX_Conceal_Cloth_Rustle: Soft rustle of burlap and khaddar cloth as Kabir slips into cover (0.38s)
"""

import math
import os
import random
import struct
import wave

SAMPLE_RATE = 44100

def write_wav(filename, samples):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        
        max_amp = max(max(abs(s) for s in samples), 0.0001)
        scale = (32767.0 * 0.88) / max_amp
        
        raw_bytes = bytearray()
        for s in samples:
            val = int(s * scale)
            val = max(-32767, min(32767, val))
            raw_bytes.extend(struct.pack('<h', val))
        
        wav_file.writeframes(raw_bytes)
    print(f"[FOLEY] Generated: {filename} ({len(samples)/SAMPLE_RATE:.2f}s)")

def generate_train_rumble():
    # Distant North Western Railway steam train: low mechanical chug (55 Hz) + distant steam whistle (680 Hz / 850 Hz)
    random.seed(1111)
    duration = 4.2
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Steam whistle envelope: active from 1.2s to 3.0s
    whistle_f1 = 680.0
    whistle_f2 = 850.0
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        # Overall train pass envelope (swell in, plateau, swell out)
        if t < 1.0:
            env = t / 1.0
        elif t > 3.2:
            env = max(0.0, (4.2 - t) / 1.0)
        else:
            env = 1.0
            
        # Low rhythmic chugging (4 beats per second)
        chug_pulse = (max(0.0, math.sin(2.0 * math.pi * 4.0 * t))) ** 2.0
        low_rumble = math.sin(2.0 * math.pi * 52.0 * t) * 0.45 + math.sin(2.0 * math.pi * 78.0 * t) * 0.25
        steam_hiss = (random.random() * 2.0 - 1.0) * 0.22
        
        train_mech = (low_rumble + steam_hiss) * (0.6 + 0.4 * chug_pulse)
        
        # Distant mournful steam whistle
        whistle = 0.0
        if 1.2 <= t <= 2.8:
            wh_rel = (t - 1.2) / 1.6
            wh_sin = max(0.0, math.sin(math.pi * wh_rel))
            wh_env = wh_sin ** 1.3
            tone1 = math.sin(2.0 * math.pi * whistle_f1 * t)
            tone2 = math.sin(2.0 * math.pi * whistle_f2 * t)
            whistle_noise = (random.random() * 2.0 - 1.0) * 0.15
            whistle = (tone1 * 0.5 + tone2 * 0.4 + whistle_noise) * wh_env * 0.48
            
        samples[i] = (train_mech * 0.75 + whistle) * env
        
    return samples

def generate_cloth_rustle():
    # Soft burlap/khaddar rustle when squeezing into hiding cover
    random.seed(1212)
    duration = 0.38
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = t / duration
        
        # Two quick rustles
        sin_prog = max(0.0, math.sin(math.pi * progress))
        env = (sin_prog ** 1.5) * (0.8 + 0.2 * math.sin(2.0 * math.pi * 9.0 * t))
        
        # Texture noise with soft friction resonance
        noise = (random.random() * 2.0 - 1.0)
        low_body = math.sin(2.0 * math.pi * 240.0 * t) * 0.35
        
        samples[i] = (noise * 0.70 + low_body) * env
        
    return samples

def main():
    art_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    os.makedirs(art_dir, exist_ok=True)
    
    write_wav(os.path.join(art_dir, "SFX_Train_Distant_Rumble.wav"), generate_train_rumble())
    write_wav(os.path.join(art_dir, "SFX_Conceal_Cloth_Rustle.wav"), generate_cloth_rustle())
    
    print("[FOLEY] Environmental & Concealment Foley synthesis complete.")

if __name__ == "__main__":
    main()
