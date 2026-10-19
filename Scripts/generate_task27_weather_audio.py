"""
PROJECT REVOLUTION — Task 27 Audio Synthesis: Dynamic Weather Loops
Synthesizes 2 authentic period atmospheric weather loops using procedural resonant noise filtering:
1. SFX_Weather_DustStorm_Wind_Loop.wav (Gusting North Indian Andhi dust storm with low canyon roar)
2. SFX_Weather_GoldenHaze_Breeze.wav    (Soft morning Punjabi dawn breeze with gentle airflow)
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

def pseudo_noise(seed):
    """Deterministic pseudo-random noise generator [-1.0, 1.0]"""
    return ((math.sin(seed * 12.9898) * 43758.5453) % 1.0) * 2.0 - 1.0

def gen_dust_storm_wind(duration=4.5):
    """
    Synthesizes pre-monsoonal Andhi dust storm:
    Low-frequency resonant wind rumble, mid-frequency haveli whistle gusts, and turbulent airflow.
    """
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples

    # 2-pole resonant bandpass filter states
    # Layer 1: Deep canyon roar (~120 Hz)
    y1_1, y1_2 = 0.0, 0.0
    # Layer 2: Haveli archway whistle (~520 Hz)
    y2_1, y2_2 = 0.0, 0.0
    # Layer 3: High swirling dust hiss (~1450 Hz)
    y3_1, y3_2 = 0.0, 0.0

    for i in range(total_samples):
        t = i / SAMPLE_RATE

        # Multi-frequency gust modulation envelopes (convective turbulence)
        gust1 = 0.5 + 0.5 * math.sin(2.0 * math.pi * 0.28 * t)
        gust2 = 0.5 + 0.5 * math.sin(2.0 * math.pi * 0.45 * t + 1.2)
        whistle_mod = 0.5 + 0.5 * math.sin(2.0 * math.pi * 0.65 * t + 2.5)
        total_gust = (gust1 * 0.60 + gust2 * 0.40)

        # Dynamic center frequency shifts
        f1 = 110.0 + 35.0 * total_gust
        f2 = 480.0 + 120.0 * whistle_mod
        f3 = 1350.0 + 300.0 * total_gust

        bw1 = 45.0
        bw2 = 65.0
        bw3 = 180.0

        r1 = math.exp(-math.pi * bw1 / SAMPLE_RATE)
        c1 = 2.0 * r1 * math.cos(2.0 * math.pi * f1 / SAMPLE_RATE)
        c1_2 = -r1 * r1

        r2 = math.exp(-math.pi * bw2 / SAMPLE_RATE)
        c2 = 2.0 * r2 * math.cos(2.0 * math.pi * f2 / SAMPLE_RATE)
        c2_2 = -r2 * r2

        r3 = math.exp(-math.pi * bw3 / SAMPLE_RATE)
        c3 = 2.0 * r3 * math.cos(2.0 * math.pi * f3 / SAMPLE_RATE)
        c3_2 = -r3 * r3

        raw_n = pseudo_noise(i * 1.037)

        # Filter band 1 (Deep Roar)
        out1 = (1.0 - r1) * raw_n * (0.75 + 0.25 * total_gust) + c1 * y1_1 + c1_2 * y1_2
        y1_2 = y1_1
        y1_1 = out1

        # Filter band 2 (Haveli Whistle)
        out2 = (1.0 - r2) * raw_n * (whistle_mod * 0.85) + c2 * y2_1 + c2_2 * y2_2
        y2_2 = y2_1
        y2_1 = out2

        # Filter band 3 (Swirling Sand Hiss)
        out3 = (1.0 - r3) * raw_n * (total_gust * 0.40) + c3 * y3_1 + c3_2 * y3_2
        y3_2 = y3_1
        y3_1 = out3

        # Seamless loop crossfade envelope at boundaries (Hann window for first and last 0.2s)
        fade = 1.0
        edge_dur = 0.25
        if t < edge_dur:
            fade = 0.5 * (1.0 - math.cos(math.pi * t / edge_dur))
        elif t > (duration - edge_dur):
            rem = (duration - t) / edge_dur
            fade = 0.5 * (1.0 - math.cos(math.pi * rem))

        samples[i] = (out1 * 0.55 + out2 * 0.30 + out3 * 0.15) * fade

    # Normalize
    peak = max(abs(s) for s in samples) if samples else 1.0
    if peak > 0.01:
        samples = [s * (0.88 / peak) for s in samples]

    return samples

def gen_golden_haze_breeze(duration=4.5):
    """
    Synthesizes tranquil morning golden hour breeze:
    Gentle high-pass air filtration, soft atmospheric breath, and peaceful dawn stillness.
    """
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples

    y1_1, y1_2 = 0.0, 0.0
    y2_1, y2_2 = 0.0, 0.0

    for i in range(total_samples):
        t = i / SAMPLE_RATE

        # Gentle slow modulation (0.15 Hz breathing)
        swell = 0.65 + 0.35 * math.sin(2.0 * math.pi * 0.15 * t)

        f1 = 280.0 + 40.0 * swell
        f2 = 850.0 + 100.0 * swell

        bw1 = 120.0
        bw2 = 240.0

        r1 = math.exp(-math.pi * bw1 / SAMPLE_RATE)
        c1 = 2.0 * r1 * math.cos(2.0 * math.pi * f1 / SAMPLE_RATE)
        c1_2 = -r1 * r1

        r2 = math.exp(-math.pi * bw2 / SAMPLE_RATE)
        c2 = 2.0 * r2 * math.cos(2.0 * math.pi * f2 / SAMPLE_RATE)
        c2_2 = -r2 * r2

        raw_n = pseudo_noise(i * 0.817)

        out1 = (1.0 - r1) * raw_n * swell + c1 * y1_1 + c1_2 * y1_2
        y1_2 = y1_1
        y1_1 = out1

        out2 = (1.0 - r2) * raw_n * swell * 0.45 + c2 * y2_1 + c2_2 * y2_2
        y2_2 = y2_1
        y2_1 = out2

        fade = 1.0
        edge_dur = 0.25
        if t < edge_dur:
            fade = 0.5 * (1.0 - math.cos(math.pi * t / edge_dur))
        elif t > (duration - edge_dur):
            rem = (duration - t) / edge_dur
            fade = 0.5 * (1.0 - math.cos(math.pi * rem))

        samples[i] = (out1 * 0.65 + out2 * 0.35) * fade

    peak = max(abs(s) for s in samples) if samples else 1.0
    if peak > 0.01:
        samples = [s * (0.80 / peak) for s in samples]

    return samples

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(base_dir, "Art", "Audio", "Weather")
    os.makedirs(out_dir, exist_ok=True)

    tracks = [
        ("SFX_Weather_DustStorm_Wind_Loop.wav", gen_dust_storm_wind()),
        ("SFX_Weather_GoldenHaze_Breeze.wav", gen_golden_haze_breeze())
    ]

    for filename, samples in tracks:
        out_path = os.path.join(out_dir, filename)
        write_wav(out_path, samples)

    print(f"\n[SUCCESS] Synthesized all {len(tracks)} weather loops to: {out_dir}")

if __name__ == "__main__":
    main()
