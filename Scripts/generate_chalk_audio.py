"""
PROJECT REVOLUTION — SCOUT CHALK & CINEMATIC AUDIO SYNTHESIZER
Synthesizes 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Chalk_Draw: Tailor's chalk (kharri mitti) scraping rhythmically on Lahori baked brick (0.48s)
2. SFX_Curfew_Bell_Toll: Heavy distant colonial clocktower curfew bell toll at midnight (3.5s)
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

def generate_chalk_draw():
    # Tailor's soapstone chalk drawing on rough brick: 3 deliberate strokes
    random.seed(909)
    duration = 0.48
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # 3 stroke strokes: (start, length, intensity)
    strokes = [
        (0.00, 0.14, 0.90),
        (0.16, 0.12, 0.75),
        (0.30, 0.15, 1.00)
    ]
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        val = 0.0
        
        for start_t, length, stroke_amp in strokes:
            if start_t <= t <= start_t + length:
                rel_t = (t - start_t) / length
                # Stroke attack/release envelope
                sin_val = max(0.0, math.sin(math.pi * rel_t))
                env = sin_val ** 1.4
                
                # Abrasive high-frequency granular noise
                friction_noise = (random.random() * 2.0 - 1.0)
                # Resonant chalk body tone (chalk stick vibrating as it catches on brick ridges)
                stick_res = math.sin(2.0 * math.pi * 1450.0 * t) * 0.35
                harm_res = math.sin(2.0 * math.pi * 2900.0 * t) * 0.20
                
                val += (friction_noise * 0.65 + stick_res + harm_res) * env * stroke_amp
                
        samples[i] = val
        
    return samples

def generate_curfew_bell_toll():
    # Deep midnight curfew bell toll (British colonial cantonment tower bell)
    random.seed(1010)
    duration = 3.6
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Fundamental 130 Hz with heavy iron clapper impact
    partials = [
        (130.0, 1.00, 0.85),
        (208.0, 0.70, 1.20),
        (260.0, 0.55, 1.60),
        (390.0, 0.40, 2.20),
        (520.0, 0.25, 2.90)
    ]
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        val = 0.0
        
        # Heavy clapper transient
        clapper = (random.random() * 2.0 - 1.0) * math.exp(-60.0 * t) * 0.45
        val += clapper
        
        for freq, amp, decay in partials:
            env = math.exp(-decay * t)
            beating = 1.0 + 0.06 * math.sin(2.0 * math.pi * 1.2 * t)
            tone = math.sin(2.0 * math.pi * freq * t)
            val += tone * env * amp * beating
            
        samples[i] = val
        
    return samples

def main():
    art_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"
    os.makedirs(art_dir, exist_ok=True)
    
    write_wav(os.path.join(art_dir, "SFX_Chalk_Draw.wav"), generate_chalk_draw())
    write_wav(os.path.join(art_dir, "SFX_Curfew_Bell_Toll.wav"), generate_curfew_bell_toll())
    
    print("[FOLEY] Scout Chalk & Curfew Bell synthesis complete.")

if __name__ == "__main__":
    main()
