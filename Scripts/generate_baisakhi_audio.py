"""
PROJECT REVOLUTION — Baisakhi Festival & Proclamation Audio Synthesizer
Generates 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Munadi_Drum: Traditional municipal crier proclamation drum roll & heavy resonant strikes (2.4s)
2. SFX_Baisakhi_Crowd_Murmur: Atmospheric gathering murmur with distant festival overtones (4.0s)
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
        scale = (32767.0 * 0.90) / max_amp
        
        raw_bytes = bytearray()
        for s in samples:
            val = int(s * scale)
            val = max(-32767, min(32767, val))
            raw_bytes.extend(struct.pack('<h', val))
        
        wav_file.writeframes(raw_bytes)
    print(f"[AUDIO_SYNTH] Generated: {filename} ({len(samples)/SAMPLE_RATE:.2f}s)")

def generate_munadi_drum():
    # Munadi drum: Quick warning roll (rattling drumhead) followed by 3 heavy proclamation strikes
    random.seed(1919)
    duration = 2.6
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Strikes timeline: (time, freq, decay, intensity)
    strikes = [
        # Rapid drum roll
        (0.00, 180.0, 0.08, 0.40),
        (0.06, 175.0, 0.08, 0.45),
        (0.12, 190.0, 0.08, 0.50),
        (0.18, 180.0, 0.08, 0.55),
        (0.24, 185.0, 0.08, 0.60),
        (0.30, 170.0, 0.08, 0.65),
        # 3 Heavy resonant proclamation thuds
        (0.48, 85.0, 0.65, 1.00),
        (1.15, 82.0, 0.70, 1.00),
        (1.85, 78.0, 0.90, 1.05)
    ]

    for start_t, freq, decay, amp in strikes:
        start_idx = int(start_t * SAMPLE_RATE)
        hit_len = int(decay * 1.5 * SAMPLE_RATE)
        for i in range(hit_len):
            idx = start_idx + i
            if idx >= total_samples:
                break
            t = i / SAMPLE_RATE
            env = math.exp(-t / (decay * 0.35))
            # Resonant drum shell modal sum
            fundamental = math.sin(2.0 * math.pi * freq * t)
            sub_octave = 0.5 * math.sin(2.0 * math.pi * (freq * 0.52) * t)
            rim_overtone = 0.3 * math.sin(2.0 * math.pi * (freq * 2.3) * t) * math.exp(-t / 0.08)
            noise = (random.random() * 2.0 - 1.0) * math.exp(-t / 0.03) * 0.25
            
            samples[idx] += amp * env * (fundamental + sub_octave + rim_overtone + noise)

    return samples

def generate_baisakhi_crowd():
    # Atmospheric murmur with low-frequency murmuring chatter and subtle resonant harmonics
    random.seed(413)
    duration = 4.0
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Pink noise base
    b0 = b1 = b2 = b3 = b4 = b5 = b6 = 0.0
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        white = random.random() * 2.0 - 1.0
        b0 = 0.99886 * b0 + white * 0.0555179
        b1 = 0.99332 * b1 + white * 0.0750759
        b2 = 0.96900 * b2 + white * 0.1538520
        b3 = 0.86650 * b3 + white * 0.3104856
        b4 = 0.55000 * b4 + white * 0.5329522
        b5 = -0.7616 * b5 - white * 0.0168980
        pink = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362
        b6 = white * 0.115926
        
        # Slow swells simulating moving festive crowds
        swell = 0.6 + 0.4 * (0.5 * math.sin(2 * math.pi * 0.35 * t) + 0.5 * math.cos(2 * math.pi * 0.72 * t))
        
        # Vocal formant simulation (frequencies at 220Hz, 440Hz, 880Hz with slow vibrato)
        formant1 = 0.25 * math.sin(2 * math.pi * (220 + 8 * math.sin(2 * math.pi * 1.5 * t)) * t)
        formant2 = 0.15 * math.sin(2 * math.pi * (440 + 12 * math.cos(2 * math.pi * 1.8 * t)) * t)
        
        samples[i] = swell * (pink * 0.18 + formant1 + formant2)

    return samples

if __name__ == "__main__":
    audio_dir = "C:/Users/npal7/PROJECT/REVOLUTION/Project/Content/Audio/SFX"
    write_wav(os.path.join(audio_dir, "SFX_Munadi_Drum.wav"), generate_munadi_drum())
    write_wav(os.path.join(audio_dir, "SFX_Baisakhi_Crowd_Murmur.wav"), generate_baisakhi_crowd())
