"""
PROJECT REVOLUTION — Task 13 Audio Synthesis
Synthesizes authentic period sound effects:
1. SFX_Telegraph_Chirp_Ticker.wav (Clicking brass telegraph sounder decoding imperial dispatches in Morse rhythm)
2. SFX_Locomotive_Steam_Hiss.wav (High-pressure steam relief valve hiss & boiler reverberation)
"""

import math
import struct
import wave
import os

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

# ---------------------------------------------------------------------------
# 1. Telegraph Sounder (Clicking brass relay in Morse pattern)
# ---------------------------------------------------------------------------
def generate_telegraph_sounder():
    duration = 4.2
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples

    # Sequence of clicks: down-click (high sharp click) and release click (lower hollow click)
    # Timing pattern imitating Morse "... .- - -.-- .- --. .-. .- .... .-" (SATYAGRAHA)
    morse_timings = [
        0.15, 0.28, 0.41,       # S (...)
        0.70, 0.88,             # A (.-)
        1.15,                   # T (-)
        1.45, 1.62, 1.85, 2.05, # Y (-.-- )
        2.35, 2.52,             # A (.-)
        2.80, 2.98, 3.15,       # G (--.)
        3.45, 3.65              # R (.-.)
    ]

    for t_start in morse_timings:
        start_idx = int(t_start * SAMPLE_RATE)
        # Down click (sharp brass strike ~2200Hz + metallic body ring ~850Hz)
        click_len = int(0.025 * SAMPLE_RATE)
        for i in range(click_len):
            idx = start_idx + i
            if idx < total_samples:
                t = i / SAMPLE_RATE
                env = math.exp(-t * 220.0)
                click = (
                    0.55 * math.sin(2.0 * math.pi * 2240.0 * t) +
                    0.30 * math.sin(2.0 * math.pi * 860.0 * t) +
                    0.15 * math.sin(2.0 * math.pi * 3800.0 * t)
                ) * env
                samples[idx] += click * 0.75

        # Release click (shorter, softer, ~1450Hz ~0.06s later)
        rel_start = start_idx + int(0.055 * SAMPLE_RATE)
        rel_len = int(0.020 * SAMPLE_RATE)
        for i in range(rel_len):
            idx = rel_start + i
            if idx < total_samples:
                t = i / SAMPLE_RATE
                env = math.exp(-t * 280.0)
                click = (
                    0.45 * math.sin(2.0 * math.pi * 1450.0 * t) +
                    0.20 * math.sin(2.0 * math.pi * 620.0 * t)
                ) * env
                samples[idx] += click * 0.45

    # Gentle room ambience / electronic wire hum (50Hz harmonic)
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        hum = 0.012 * math.sin(2.0 * math.pi * 100.0 * t)
        samples[i] += hum

    return samples

# ---------------------------------------------------------------------------
# 2. Locomotive Steam Relief Hiss (Pressurized boiler vent & metal heat)
# ---------------------------------------------------------------------------
def generate_locomotive_steam_hiss():
    duration = 4.8
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples

    # White noise filtered into high-pressure turbulent steam hiss
    # Envelope: sharp burst, sustained high pressure, gentle tapering
    import random
    random.seed(42)

    # Simple lowpass / bandpass state
    b0, b1, b2 = 0.0, 0.0, 0.0

    for i in range(total_samples):
        t = i / SAMPLE_RATE

        # Attack (0.0 to 0.35s), Sustain (0.35 to 3.2s), Release (3.2 to 4.8s)
        if t < 0.35:
            env = t / 0.35
            env = env * env
        elif t < 3.2:
            env = 1.0 + 0.12 * math.sin(2.0 * math.pi * 3.5 * t)
        else:
            rel = (4.8 - t) / 1.6
            env = rel * rel

        # High frequency turbulence
        noise = (random.random() * 2.0 - 1.0)
        
        # Simple 2-pole resonant filter (~2800Hz steam nozzle whistle)
        b0 = 0.85 * b0 + 0.15 * noise
        b1 = 0.70 * b1 + 0.30 * b0
        b2 = 0.60 * b2 + 0.40 * b1

        whistle = 0.18 * math.sin(2.0 * math.pi * 2750.0 * t + 0.5 * math.sin(2.0 * math.pi * 12.0 * t))
        boiler_rumble = 0.15 * math.sin(2.0 * math.pi * 65.0 * t) + 0.08 * math.sin(2.0 * math.pi * 130.0 * t)

        steam = (0.65 * (noise - b1) + whistle + boiler_rumble) * env * 0.72
        samples[i] = steam

    return samples

def main():
    dest_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Project/Content/Audio/SFX"
    os.makedirs(dest_dir, exist_ok=True)

    telegraph_samples = generate_telegraph_sounder()
    write_wav(os.path.join(dest_dir, "SFX_Telegraph_Chirp_Ticker.wav"), telegraph_samples)

    steam_samples = generate_locomotive_steam_hiss()
    write_wav(os.path.join(dest_dir, "SFX_Locomotive_Steam_Hiss.wav"), steam_samples)

    print("Task 13 Audio Synthesis completed successfully!")

if __name__ == "__main__":
    main()
