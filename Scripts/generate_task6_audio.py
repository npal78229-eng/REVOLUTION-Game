"""
PROJECT REVOLUTION — Task 6: Jallianwala Bagh Audio Synthesizer
Generates 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Crowd_Rally_Speech: Distant orator addressing the assembly with crowd murmur affirmations (3.5s)
2. SFX_Military_Boot_March: Synchronized iron-heel military boots marching in cadence on gravel/earth (3.2s)
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

def generate_crowd_rally_speech():
    # Vocal formant peaks representing an orator calling out across the garden
    random.seed(1919)
    duration = 3.6
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Rhythmic vocal utterances representing speech cadences: "Inquilab! Satyagraha!"
    syllables = [
        (0.15, 220.0, 0.22, 0.7),
        (0.40, 240.0, 0.28, 0.9),
        (0.72, 195.0, 0.35, 0.8),
        (1.20, 260.0, 0.20, 0.75),
        (1.45, 280.0, 0.30, 0.95),
        (1.80, 210.0, 0.40, 0.85),
        (2.35, 250.0, 0.25, 0.8),
        (2.65, 310.0, 0.45, 1.0),
    ]

    for start_t, f0, length, amp in syllables:
        start_idx = int(start_t * SAMPLE_RATE)
        syl_len = int(length * SAMPLE_RATE)
        for i in range(syl_len):
            idx = start_idx + i
            if idx >= total_samples:
                break
            t = i / SAMPLE_RATE
            env = math.sin(math.pi * (i / syl_len))  # Smooth vowel envelope
            # Fundamental + Formant harmonics (1st, 2nd, 3rd)
            vocal = math.sin(2.0 * math.pi * f0 * t) * 0.5 \
                  + math.sin(2.0 * math.pi * f0 * 2.2 * t) * 0.3 \
                  + math.sin(2.0 * math.pi * f0 * 3.4 * t) * 0.15
            # Distant echo reflection
            echo_val = math.sin(2.0 * math.pi * f0 * 1.05 * t) * 0.1
            samples[idx] += (vocal + echo_val) * env * amp

    # Ambient garden crowd murmur bed underneath
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        noise = (random.random() * 2.0 - 1.0)
        # Low rumble & breathing swells
        crowd_bed = math.sin(2.0 * math.pi * 55.0 * t) * 0.08 \
                  + math.sin(2.0 * math.pi * 95.0 * t) * 0.06 \
                  + math.sin(2.0 * math.pi * 140.0 * t) * 0.04
        # Amplitude swell of the crowd reacting to speech
        swell = 0.5 + 0.3 * math.sin(2.0 * math.pi * 0.6 * t)
        samples[i] += (noise * 0.04 + crowd_bed) * swell

    return samples

def generate_military_boot_march():
    # Rhythmic cadence of 50 iron-hobnailed military boots stamping in unison
    random.seed(1304)
    duration = 3.2
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Cadence: 110 paces per minute (approx 0.545s per step)
    step_times = [0.15, 0.70, 1.25, 1.80, 2.35, 2.90]

    for step_t in step_times:
        step_idx = int(step_t * SAMPLE_RATE)
        # A single march step consists of multiple soldier footfalls clustered within 40ms
        for soldier in range(12):
            jitter = random.uniform(-0.018, 0.018)
            s_idx = step_idx + int(jitter * SAMPLE_RATE)
            if s_idx < 0 or s_idx >= total_samples:
                continue
            
            # Iron heel strike (metallic click + heavy earth thud)
            heel_len = int(0.12 * SAMPLE_RATE)
            for j in range(heel_len):
                idx = s_idx + j
                if idx >= total_samples:
                    break
                t = j / SAMPLE_RATE
                env = math.exp(-35.0 * t)
                # Low earth impact thud (65-80 Hz)
                thud = math.sin(2.0 * math.pi * 72.0 * t) * 0.7
                # Metallic hobnail crunch (high frequency noise burst)
                hobnail = (random.random() * 2.0 - 1.0) * math.exp(-60.0 * t) * 0.5
                samples[idx] += (thud + hobnail) * env * 0.35

    return samples

def main():
    print("================ TASK 6: JALLIANWALA BAGH AUDIO SYNTHESIZER ================")
    out_dir_art = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Audio"
    out_dir_proj = r"C:\Users\npal7\PROJECT\REVOLUTION\Project\Content\Audio\SFX"

    # 1. Crowd Rally Speech
    samples_speech = generate_crowd_rally_speech()
    wav_speech_art = os.path.join(out_dir_art, "SFX_Crowd_Rally_Speech.wav")
    wav_speech_proj = os.path.join(out_dir_proj, "SFX_Crowd_Rally_Speech.wav")
    write_wav(wav_speech_art, samples_speech)
    write_wav(wav_speech_proj, samples_speech)

    # 2. Military Boot March
    samples_march = generate_military_boot_march()
    wav_march_art = os.path.join(out_dir_art, "SFX_Military_Boot_March.wav")
    wav_march_proj = os.path.join(out_dir_proj, "SFX_Military_Boot_March.wav")
    write_wav(wav_march_art, samples_march)
    write_wav(wav_march_proj, samples_march)

    print("================ AUDIO SYNTHESIS COMPLETE ================")

if __name__ == "__main__":
    main()
