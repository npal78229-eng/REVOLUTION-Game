"""
PROJECT REVOLUTION — HISTORICAL HAVELI DOOR & LATCH AUDIO SYNTHESIZER
Synthesizes period-authentic acoustic Foley for Kot Gurdarshan haveli doors and wrought-iron sliding bolts (kundi):
1. SFX_Iron_Latch_Slide.wav   - Heavy wrought-iron bolt scraping through iron brackets and locking into slot.
2. SFX_Teak_Door_Creak.wav    - Heavy dry teak timber groaning on forged iron pivot hinge (stick-slip friction).
3. SFX_Door_Slam_Wood.wav     - Resonant impact of heavy timber haveli door slamming shut into frame.
4. SFX_Door_Banging_Lathi.wav - 3 forceful strikes of brass-tipped bamboo lathi against locked wooden door planks.

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
        
        # Clamp and convert float to 16-bit signed integer
        raw_bytes = bytearray()
        for s in samples:
            s_clamped = max(-1.0, min(1.0, s))
            val = int(s_clamped * 32767.0)
            raw_bytes.extend(struct.pack("<h", val))
            
        wav_file.writeframes(raw_bytes)
    print(f"Generated {filename}: {len(samples)/SAMPLE_RATE:.2f}s ({len(raw_bytes)} bytes)")

def generate_iron_latch_slide():
    """Wrought-iron slide-bolt scraping through iron sleeve brackets with end lock click."""
    duration = 0.58
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    random.seed(42)
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        # Slide phase: 0.0s to 0.45s
        if t < 0.45:
            slide_progress = t / 0.45
            # Metal scrape friction noise modulated by frequency
            noise = (random.random() * 2.0 - 1.0) * 0.28
            # High resonant squeak / scrape frequencies of iron
            iron_res1 = math.sin(2.0 * math.pi * (780.0 + 350.0 * slide_progress) * t) * 0.15
            iron_res2 = math.sin(2.0 * math.pi * (1420.0 + 200.0 * math.sin(t * 30.0)) * t) * 0.10
            
            env = math.sin(slide_progress * math.pi) ** 0.8
            samples[i] = (noise + iron_res1 + iron_res2) * env * 0.75
            
        # Lock latch click phase: 0.45s to 0.58s
        else:
            click_t = t - 0.45
            click_decay = math.exp(-click_t * 55.0)
            
            # Sharp metallic strike (iron meeting iron catch)
            metal_strike = math.sin(2.0 * math.pi * 920.0 * click_t) * 0.45 + \
                           math.sin(2.0 * math.pi * 2150.0 * click_t) * 0.35 + \
                           math.sin(2.0 * math.pi * 3800.0 * click_t) * 0.20
            noise_burst = (random.random() * 2.0 - 1.0) * 0.3 * math.exp(-click_t * 120.0)
            
            samples[i] = (metal_strike + noise_burst) * click_decay * 0.95
            
    return samples

def generate_teak_door_creak():
    """Heavy seasoned teak door groaning on dry iron pivot hinge (stick-slip friction)."""
    duration = 1.15
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    random.seed(1919)
    
    phase_wood = 0.0
    phase_hinge = 0.0
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        # Envelope: slow ramp in, sustain with fluctuations, taper off
        if t < 0.2:
            env = (t / 0.2) ** 1.5
        elif t < 0.95:
            env = 1.0 + 0.25 * math.sin(t * 14.0)
        else:
            env = max(0.0, 1.0 - (t - 0.95) / 0.20)
            
        # Stick-slip frequency modulation (erratic pivot shudder)
        freq_slip = 110.0 + 45.0 * math.sin(t * 18.0) + 20.0 * (random.random() * 2.0 - 1.0)
        freq_body = 230.0 + 15.0 * math.sin(t * 8.0)
        
        phase_wood += 2.0 * math.pi * freq_body / SAMPLE_RATE
        phase_hinge += 2.0 * math.pi * freq_slip / SAMPLE_RATE
        
        # Distorted triangle / clipped wave for wood groaning texture
        wood_wave = math.sin(phase_wood)
        hinge_wave = math.sin(phase_hinge)
        if hinge_wave > 0.4:
            hinge_wave = 0.4 + (hinge_wave - 0.4) * 0.2
        elif hinge_wave < -0.4:
            hinge_wave = -0.4 + (hinge_wave + 0.4) * 0.2
            
        grain_noise = (random.random() * 2.0 - 1.0) * 0.08
        
        samples[i] = (wood_wave * 0.35 + hinge_wave * 0.55 + grain_noise) * env * 0.65
        
    return samples

def generate_door_slam_wood():
    """Heavy timber haveli door slamming shut with frame resonance and latch bounce."""
    duration = 0.48
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    random.seed(77)
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        decay_bass = math.exp(-t * 22.0)
        decay_thud = math.exp(-t * 45.0)
        decay_latch = math.exp(-max(0.0, t - 0.04) * 35.0)
        
        # Deep frame boom (60Hz to 85Hz)
        bass_boom = math.sin(2.0 * math.pi * (70.0 - 15.0 * min(1.0, t * 5.0)) * t) * 0.60
        # Thick timber crack
        timber_thud = math.sin(2.0 * math.pi * 180.0 * t) * 0.35 + (random.random() * 2.0 - 1.0) * 0.25 * decay_thud
        # Iron catch rattle
        iron_rattle = 0.0
        if t >= 0.04:
            iron_rattle = math.sin(2.0 * math.pi * 1150.0 * (t - 0.04)) * 0.25 * decay_latch
            
        samples[i] = (bass_boom * decay_bass + timber_thud * decay_thud + iron_rattle) * 0.90
        
    return samples

def generate_door_banging_lathi():
    """3 forceful strikes of brass-tipped bamboo lathi against locked wooden door planks."""
    duration = 1.35
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    strike_times = [0.02, 0.42, 0.84]
    strike_intensities = [0.85, 0.95, 1.0]
    
    random.seed(108)
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        sample_sum = 0.0
        
        for strike_idx, st in enumerate(strike_times):
            if t >= st:
                dt = t - st
                decay = math.exp(-dt * 32.0)
                decay_click = math.exp(-dt * 110.0)
                
                # Brass tip sharp impact
                brass_click = math.sin(2.0 * math.pi * 2400.0 * dt) * 0.40 * decay_click
                # Bamboo lathi body snap
                bamboo_snap = math.sin(2.0 * math.pi * 480.0 * dt) * 0.35 * decay
                # Heavy timber door plank vibration
                door_res = math.sin(2.0 * math.pi * 125.0 * dt) * 0.45 * decay
                impact_noise = (random.random() * 2.0 - 1.0) * 0.30 * decay_click
                
                intensity = strike_intensities[strike_idx]
                sample_sum += (brass_click + bamboo_snap + door_res + impact_noise) * intensity
                
        samples[i] = max(-1.0, min(1.0, sample_sum * 0.72))
        
    return samples

def main():
    print("Synthesizing Haveli Door & Iron Bolt Foley for Project REVOLUTION...")
    write_wav("SFX_Iron_Latch_Slide.wav", generate_iron_latch_slide())
    write_wav("SFX_Teak_Door_Creak.wav", generate_teak_door_creak())
    write_wav("SFX_Door_Slam_Wood.wav", generate_door_slam_wood())
    write_wav("SFX_Door_Banging_Lathi.wav", generate_door_banging_lathi())
    print("All door & latch audio assets generated successfully!")

if __name__ == "__main__":
    main()
