"""
PROJECT REVOLUTION — MISSION & WATCHMAN FOLEY SYNTHESIZER
Synthesizes 16-bit 44.1kHz PCM WAV audio for:
- Colonial Police / Chaukidar Brass Whistle (Dual-tone 2400 Hz / 2640 Hz pea whistle)
- Watchman Curfew Challenge Callout (Deep vocalized warning resonance)
- Underground Pamphlet Bundle Retrieval (Rustle of cord and printed sheets)
- Dawn Temple Bronze Gong (Resonant 160 Hz historical morning bell)
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

def generate_police_whistle():
    # British colonial police pea whistle: 2400 Hz and 2640 Hz with trill modulation
    random.seed(505)
    duration = 0.65
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    f1 = 2380.0
    f2 = 2620.0
    trill_freq = 28.0 # Pea rotation trill in chamber
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = t / duration
        
        # Attack, sustain, quick release
        if progress < 0.1:
            env = progress / 0.1
        elif progress < 0.85:
            env = 1.0
        else:
            env = (1.0 - progress) / 0.15
            
        # Chamber trill amplitude & frequency modulation
        trill = 0.85 + 0.15 * math.sin(2.0 * math.pi * trill_freq * t)
        breath_noise = (random.random() * 2.0 - 1.0) * 0.12
        
        tone = (math.sin(2.0 * math.pi * f1 * t) + math.sin(2.0 * math.pi * f2 * t)) * 0.5
        samples[i] = (tone * trill + breath_noise) * env
        
    return samples

def generate_watchman_callout():
    # Deep vocalized curfew challenge burst: fundamental ~120 Hz with formant resonances
    random.seed(909)
    duration = 0.55
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    f0 = 125.0
    formant1 = 750.0  # Open vowel 'Ah/Oh'
    formant2 = 1250.0
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = t / duration
        
        # Bark envelope: quick rise at 40ms, sharp sustain, taper
        if progress < 0.12:
            env = progress / 0.12
        elif progress < 0.70:
            env = 1.0 - 0.2 * ((progress - 0.12) / 0.58)
        else:
            env = 0.8 * (1.0 - progress) / 0.30
            
        # Vocal buzz + formants
        glottal = math.sin(2.0 * math.pi * f0 * t) + 0.6 * math.sin(4.0 * math.pi * f0 * t)
        formants = 0.7 * math.sin(2.0 * math.pi * formant1 * t) + 0.4 * math.sin(2.0 * math.pi * formant2 * t)
        breath = (random.random() * 2.0 - 1.0) * 0.08
        
        samples[i] = (glottal * 0.4 + formants * 0.55 + breath) * env
        
    return samples

def generate_pamphlet_bundle():
    # Paper bundle retrieval: paper friction + cord snap
    random.seed(612)
    duration = 0.40
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = t / duration
        
        # Dual paper rustle wave
        env = math.sin(math.pi * progress) ** 1.5
        paper_noise = (random.random() * 2.0 - 1.0)
        high_paper = math.sin(2.0 * math.pi * (2400.0 + 1200.0 * random.random()) * t) * 0.3
        
        # Cord pop at 120ms
        cord_snap = 0.0
        if 0.10 < t < 0.14:
            dt = t - 0.10
            cord_snap = math.sin(2.0 * math.pi * 320.0 * dt) * math.exp(-80.0 * dt) * 0.6
            
        samples[i] = ((paper_noise * 0.6 + high_paper) * env) + cord_snap
        
    return samples

def generate_dawn_gong():
    # 160 Hz bronze bell with harmonic decay
    random.seed(321)
    duration = 1.8
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    f0 = 164.0
    f1 = 328.0
    f2 = 492.0
    f3 = 780.0
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        # Strike transient at t=0
        strike = math.exp(-60.0 * t) * (random.random() * 2.0 - 1.0) * 0.4
        
        # Resonant bell ring down
        ring0 = math.sin(2.0 * math.pi * f0 * t) * math.exp(-2.2 * t)
        ring1 = 0.55 * math.sin(2.0 * math.pi * f1 * t) * math.exp(-3.5 * t)
        ring2 = 0.35 * math.sin(2.0 * math.pi * f2 * t) * math.exp(-4.8 * t)
        ring3 = 0.20 * math.sin(2.0 * math.pi * f3 * t) * math.exp(-6.5 * t)
        
        samples[i] = strike + ring0 + ring1 + ring2 + ring3
        
    return samples

def main():
    out_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    print("=== SYNTHESIZING MISSION & WATCHMAN SFX ===")
    
    write_wav(os.path.join(out_dir, "SFX_Watchman_Whistle.wav"), generate_police_whistle())
    write_wav(os.path.join(out_dir, "SFX_Watchman_Callout.wav"), generate_watchman_callout())
    write_wav(os.path.join(out_dir, "SFX_Pamphlet_Retrieve.wav"), generate_pamphlet_bundle())
    write_wav(os.path.join(out_dir, "SFX_Dawn_Gong_Complete.wav"), generate_dawn_gong())
    
    print("=== MISSION AUDIO GENERATION FINISHED ===")

if __name__ == "__main__":
    main()
