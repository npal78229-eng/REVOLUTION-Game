"""
PROJECT REVOLUTION — STEALTH DISTRACTION & ATMOSPHERE AUDIO SYNTHESIZER
Synthesizes 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Pebble_Throw: Subtle cloth swish / boyish hand fling (0.22s)
2. SFX_Pebble_Impact: Sharp stone-on-brick transient with realistic ceramic ricochets (0.42s)
3. SFX_Dawn_Temple_Bell: Resonant 1919 Punjabi bronze temple bell with rich overtones (3.2s)
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

def generate_pebble_throw():
    # Boyish cloth flick and gentle air whoosh
    random.seed(601)
    duration = 0.22
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = t / duration
        
        # Smooth bell envelope peaking around 35%
        env = math.sin(math.pi * progress) ** 2.2
        
        # Low frequency cloth whoosh + subtle white noise
        whoosh_freq = 280.0 + 160.0 * math.sin(math.pi * progress)
        tone = math.sin(2.0 * math.pi * whoosh_freq * t)
        noise = (random.random() * 2.0 - 1.0) * 0.45
        
        samples[i] = (tone * 0.55 + noise * 0.45) * env
        
    return samples

def generate_pebble_impact():
    # Sharp stone-on-brick initial click + 2 small ricochet bounces
    random.seed(702)
    duration = 0.42
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Impact events: (start_time, amplitude, resonance_freq, decay_rate)
    impacts = [
        (0.000, 1.00, 1850.0, 48.0),   # Main sharp hard brick crack
        (0.075, 0.42, 2100.0, 65.0),   # Secondary ricochet
        (0.145, 0.18, 2350.0, 80.0)    # Soft settling rattle
    ]
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        val = 0.0
        
        for imp_t, amp, freq, decay in impacts:
            if t >= imp_t:
                dt = t - imp_t
                env = math.exp(-decay * dt)
                # Ceramic resonant ping with high transient noise
                carrier = math.sin(2.0 * math.pi * freq * dt)
                harmonic = 0.4 * math.sin(2.0 * math.pi * (freq * 1.62) * dt)
                noise_burst = (random.random() * 2.0 - 1.0) * math.exp(-120.0 * dt) * 0.6
                val += (carrier + harmonic + noise_burst) * env * amp
                
        samples[i] = val
        
    return samples

def generate_dawn_temple_bell():
    # Punjabi temple / gurdwara bronze bell with deep harmonic overtones
    random.seed(803)
    duration = 3.2
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Bell partial frequencies and decay rates:
    # Bronze bells have non-harmonic partials: prime, tierce, quint, octave, nominal
    partials = [
        (220.0, 1.00, 1.1),    # Prime (fundamental 220 Hz)
        (262.0, 0.65, 1.6),    # Minor third (tierce)
        (330.0, 0.50, 2.0),    # Fifth (quint)
        (440.0, 0.40, 2.6),    # Octave (nominal)
        (587.0, 0.25, 3.4),    # Upper partial
        (880.0, 0.15, 4.5)     # Shimmer
    ]
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        val = 0.0
        
        # Initial mallet strike transient
        strike_noise = (random.random() * 2.0 - 1.0) * math.exp(-80.0 * t) * 0.35
        val += strike_noise
        
        for freq, amp, decay in partials:
            env = math.exp(-decay * t)
            # Subtle beating between dual modes
            beating = 1.0 + 0.08 * math.sin(2.0 * math.pi * 1.8 * t)
            tone = math.sin(2.0 * math.pi * freq * t)
            val += tone * env * amp * beating
            
        samples[i] = val
        
    return samples

def main():
    art_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    os.makedirs(art_dir, exist_ok=True)
    
    write_wav(os.path.join(art_dir, "SFX_Pebble_Throw.wav"), generate_pebble_throw())
    write_wav(os.path.join(art_dir, "SFX_Pebble_Impact.wav"), generate_pebble_impact())
    write_wav(os.path.join(art_dir, "SFX_Dawn_Temple_Bell.wav"), generate_dawn_temple_bell())
    
    print("[FOLEY] Stealth & Atmosphere Foley synthesis complete.")

if __name__ == "__main__":
    main()
