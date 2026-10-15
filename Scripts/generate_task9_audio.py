"""
PROJECT REVOLUTION — Task 9: Outskirts & The Upper Bari Doab Canal
Audio Synthesizer: Canal Water Flow & Persian Wheel (Rahat) Creak
Generates 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Canal_Water_Flow_Gentle.wav: Continuous flowing water currents, sluice ripples and channel turbulence (4.5s)
2. SFX_Persian_Wheel_Rahat_Creak.wav: Heavy timber cogwheel groaning, rhythmic wooden friction creaks and splashing buckets (4.5s)
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
        scale = (32767.0 * 0.92) / max_amp
        
        raw_bytes = bytearray()
        for s in samples:
            val = int(s * scale)
            val = max(-32767, min(32767, val))
            raw_bytes.extend(struct.pack('<h', val))
        
        wav_file.writeframes(raw_bytes)
    print(f"[AUDIO_SYNTH] Generated: {filename} ({len(samples)/SAMPLE_RATE:.2f}s)")

def generate_canal_water_flow():
    """
    Synthesizes gentle canal water flow:
    - Low-frequency hydraulic rumble (120-220 Hz)
    - Mid-frequency fluid turbulence & swirling vortex currents (300-800 Hz)
    - High-frequency surface ripples & bubbling foam (1400-3200 Hz)
    """
    random.seed(1919041309)
    duration = 4.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # 1. Base flowing current (filtered white noise & low sine modulation)
    prev_low = 0.0
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        noise = random.uniform(-1.0, 1.0)
        # Low-pass filter for rumble
        prev_low = prev_low * 0.96 + noise * 0.04
        rumble = prev_low * 0.45 * (1.0 + 0.2 * math.sin(2.0 * math.pi * 0.8 * t))
        samples[i] += rumble

    # 2. Swirling vortex currents & mid-frequency stream eddies
    for comp in [(240.0, 0.25), (380.0, 0.22), (520.0, 0.18), (680.0, 0.15)]:
        freq, amp = comp
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            mod = 1.0 + 0.3 * math.sin(2.0 * math.pi * 1.4 * t + freq * 0.01)
            samples[i] += amp * mod * math.sin(2.0 * math.pi * freq * t + random.uniform(-0.1, 0.1))

    # 3. Surface ripple & bubble droplets
    num_bubbles = 180
    for _ in range(num_bubbles):
        b_time = random.uniform(0.05, duration - 0.1)
        b_idx = int(b_time * SAMPLE_RATE)
        b_len = int(random.uniform(0.02, 0.06) * SAMPLE_RATE)
        b_freq = random.uniform(1200.0, 2800.0)
        b_amp = random.uniform(0.12, 0.28)
        
        for k in range(b_len):
            idx = b_idx + k
            if idx < total_samples:
                tau = k / b_len
                env = math.sin(math.pi * tau) * math.exp(-2.5 * tau)
                # frequency chirp up slightly like real fluid bubbles
                f_inst = b_freq * (1.0 + 0.3 * tau)
                samples[idx] += b_amp * env * math.sin(2.0 * math.pi * f_inst * (k / SAMPLE_RATE))

    # 4. Fade in and out
    fade_len = int(0.2 * SAMPLE_RATE)
    for i in range(fade_len):
        f = i / fade_len
        samples[i] *= f
        samples[total_samples - 1 - i] *= f

    return samples

def generate_persian_wheel_rahat_creak():
    """
    Synthesizes rhythmic Persian Wheel (Rahat) rotation:
    - Periodic wooden tooth friction & groaning stresses (0.8s rotation cycle)
    - Timber stress squeaks (220-480 Hz with rich wooden overtones)
    - Iron pivot axle squeak
    - Rhythmic cascade of water tipping from earthenware buckets into canal trough
    """
    random.seed(1919041310)
    duration = 4.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    cycle_period = 0.85  # Seconds per gear tooth mesh cycle
    num_cycles = int(duration / cycle_period) + 1

    for c in range(num_cycles):
        cycle_start = c * cycle_period
        
        # A. Heavy timber gear tooth creak (0.25s)
        creak_len = 0.26
        creak_samps = int(creak_len * SAMPLE_RATE)
        c_idx = int(cycle_start * SAMPLE_RATE)
        base_pitch = random.uniform(190.0, 240.0)

        for k in range(creak_samps):
            idx = c_idx + k
            if idx < total_samples:
                t_k = k / SAMPLE_RATE
                tau = k / creak_samps
                env = math.sin(math.pi * tau) * (1.0 + 0.4 * math.sin(2.0 * math.pi * 32.0 * t_k))
                
                # Timber harmonics: fundamental + 2nd + 3rd + friction grit
                sig = 0.45 * math.sin(2.0 * math.pi * base_pitch * t_k)
                sig += 0.30 * math.sin(2.0 * math.pi * (base_pitch * 2.03) * t_k)
                sig += 0.20 * math.sin(2.0 * math.pi * (base_pitch * 3.12) * t_k)
                sig += 0.15 * math.sin(2.0 * math.pi * (base_pitch * 4.85) * t_k)
                sig += 0.18 * random.uniform(-1.0, 1.0) * math.sin(math.pi * tau)  # rough wood friction
                
                samples[idx] += sig * env * 0.75

        # B. High iron spindle squeak chirp (0.08s)
        squeak_start = cycle_start + random.uniform(0.08, 0.15)
        squeak_idx = int(squeak_start * SAMPLE_RATE)
        squeak_samps = int(0.09 * SAMPLE_RATE)
        sq_pitch = random.uniform(1350.0, 1650.0)
        for k in range(squeak_samps):
            idx = squeak_idx + k
            if idx < total_samples:
                t_k = k / SAMPLE_RATE
                tau = k / squeak_samps
                env = math.sin(math.pi * tau) ** 2
                sig = math.sin(2.0 * math.pi * sq_pitch * t_k)
                samples[idx] += sig * env * 0.22

        # C. Water bucket tipping and splashing into wooden trough (0.35s)
        splash_start = cycle_start + 0.18
        splash_idx = int(splash_start * SAMPLE_RATE)
        splash_samps = int(0.38 * SAMPLE_RATE)
        for k in range(splash_samps):
            idx = splash_idx + k
            if idx < total_samples:
                tau = k / splash_samps
                env = math.sin(math.pi * tau) * math.exp(-1.8 * tau)
                noise = random.uniform(-1.0, 1.0)
                # Filtered splashing texture
                samples[idx] += noise * env * 0.35

    # Low continuous axle rotational drone
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        drone = 0.12 * math.sin(2.0 * math.pi * 95.0 * t) + 0.08 * math.sin(2.0 * math.pi * 190.0 * t)
        samples[i] += drone

    # Fade in / fade out
    fade_len = int(0.2 * SAMPLE_RATE)
    for i in range(fade_len):
        f = i / fade_len
        samples[i] *= f
        samples[total_samples - 1 - i] *= f

    return samples

if __name__ == "__main__":
    out_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Audio"
    os.makedirs(out_dir, exist_ok=True)
    
    water_flow_path = os.path.join(out_dir, "SFX_Canal_Water_Flow_Gentle.wav")
    samples_water = generate_canal_water_flow()
    write_wav(water_flow_path, samples_water)
    
    rahat_creak_path = os.path.join(out_dir, "SFX_Persian_Wheel_Rahat_Creak.wav")
    samples_rahat = generate_persian_wheel_rahat_creak()
    write_wav(rahat_creak_path, samples_rahat)
    
    print("[TASK9_AUDIO] Successfully generated all Task 9 audio assets!")
