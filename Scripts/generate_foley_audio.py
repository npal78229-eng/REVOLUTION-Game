"""
PROJECT REVOLUTION — PROCEDURAL FOLEY SYNTHESIZER
Synthesizes historically grounded 16-bit 44.1kHz PCM WAV audio for:
- Leather mojari footsteps on Lahori baked brick & aged teak wood
- Cotton kurta cloth rustle during 1.1m rooftop parapet vaulting
- Antique parchment vellum lore inspection card opening & stowing
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
        
        # Normalize and convert to 16-bit signed integers
        max_amp = max(max(abs(s) for s in samples), 0.0001)
        target_peak = 0.88  # Headroom
        scale = (32767.0 * target_peak) / max_amp
        
        raw_bytes = bytearray()
        for s in samples:
            val = int(s * scale)
            val = max(-32767, min(32767, val))
            raw_bytes.extend(struct.pack('<h', val))
        
        wav_file.writeframes(raw_bytes)
    print(f"[FOLEY] Generated: {filename} ({len(samples)/SAMPLE_RATE:.2f}s)")

def generate_brick_footstep(variation=1):
    random.seed(42 + variation * 13)
    duration = 0.22
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # 1. Low-frequency heel strike thud (leather sole on solid brick)
    thud_freq = 95.0 + variation * 12.0
    decay_rate = 38.0
    
    # 2. Masonry grit scatter (crushed sand / lime mortar friction)
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        # Impact transient
        thud = math.sin(2.0 * math.pi * thud_freq * t) * math.exp(-decay_rate * t)
        second_harm = 0.4 * math.sin(2.0 * math.pi * (thud_freq * 1.8) * t) * math.exp(-decay_rate * 1.4 * t)
        
        # Grit noise (bandpass feel using difference of randoms)
        noise = (random.random() * 2.0 - 1.0)
        grit_envelope = math.exp(-45.0 * t) if t < 0.08 else math.exp(-25.0 * t) * 0.2
        grit = noise * grit_envelope * 0.35
        
        # Sole slap secondary tap at 35ms
        tap = 0.0
        if t > 0.035:
            tap_t = t - 0.035
            tap = math.sin(2.0 * math.pi * 180.0 * tap_t) * math.exp(-60.0 * tap_t) * 0.45
            
        samples[i] = thud + second_harm + grit + tap
        
    return samples

def generate_wood_footstep(variation=1):
    random.seed(101 + variation * 17)
    duration = 0.26
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Teak wood cavity resonance (180 Hz, 340 Hz, 520 Hz)
    f1, f2, f3 = 175.0 + variation * 10, 350.0, 530.0
    decay_rate = 24.0
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        res1 = math.sin(2.0 * math.pi * f1 * t) * math.exp(-decay_rate * t)
        res2 = 0.55 * math.sin(2.0 * math.pi * f2 * t) * math.exp(-decay_rate * 1.3 * t)
        res3 = 0.25 * math.sin(2.0 * math.pi * f3 * t) * math.exp(-decay_rate * 1.8 * t)
        
        click = (random.random() * 2.0 - 1.0) * math.exp(-90.0 * t) * 0.35
        
        samples[i] = res1 + res2 + res3 + click
        
    return samples

def generate_vault_whoosh():
    random.seed(777)
    duration = 0.42
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Smooth bell envelope for whoosh
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = t / duration
        
        # Parabolic bell curve
        envelope = math.sin(math.pi * progress) ** 1.8
        
        # Cloth flutter (14 Hz modulation)
        flutter = 0.85 + 0.15 * math.sin(2.0 * math.pi * 14.0 * t)
        
        # Air displacement whoosh (swept noise)
        noise = (random.random() * 2.0 - 1.0)
        low_noise = math.sin(2.0 * math.pi * (220.0 + 380.0 * envelope) * t)
        
        samples[i] = (noise * 0.45 + low_noise * 0.55) * envelope * flutter
        
    return samples

def generate_parchment_sound(b_open=True):
    random.seed(333 if b_open else 444)
    duration = 0.36 if b_open else 0.28
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = t / duration
        
        # Envelope: quick rise, subtle friction crinkle, gentle taper
        if b_open:
            envelope = math.sin(math.pi * progress) ** 1.3
        else:
            envelope = math.exp(-7.0 * progress) * math.sin(math.pi * progress)
            
        noise = (random.random() * 2.0 - 1.0)
        
        # Paper crispness high-pass emphasis
        crinkle = math.sin(2.0 * math.pi * (1800.0 + 800.0 * random.random()) * t) * 0.25
        
        samples[i] = (noise * 0.75 + crinkle) * envelope
        
    return samples

def main():
    out_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    print("=== SYNTHESIZING REVOLUTION PERIOD FOLEY SFX ===")
    
    write_wav(os.path.join(out_dir, "SFX_Footstep_Brick_01.wav"), generate_brick_footstep(1))
    write_wav(os.path.join(out_dir, "SFX_Footstep_Brick_02.wav"), generate_brick_footstep(2))
    write_wav(os.path.join(out_dir, "SFX_Footstep_Wood_01.wav"), generate_wood_footstep(1))
    write_wav(os.path.join(out_dir, "SFX_Footstep_Wood_02.wav"), generate_wood_footstep(2))
    write_wav(os.path.join(out_dir, "SFX_Vault_Whoosh_Cloth.wav"), generate_vault_whoosh())
    write_wav(os.path.join(out_dir, "SFX_Parchment_Open.wav"), generate_parchment_sound(True))
    write_wav(os.path.join(out_dir, "SFX_Parchment_Close.wav"), generate_parchment_sound(False))
    
    print("=== ALL FOLEY ASSETS GENERATED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
