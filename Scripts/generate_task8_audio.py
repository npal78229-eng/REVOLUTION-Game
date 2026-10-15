"""
PROJECT REVOLUTION — Task 8: Act III — The Fateful Dusk & The Amritsar Curfew
Audio Synthesizer: Night Ambience & Curfew Police Whistle
Generates 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Night_Cricket_Ambience.wav: Nocturnal Punjab ambience with crickets, alley wind, and distant mourning (4.5s)
2. SFX_Police_Whistle_Curfew.wav: Sharp British colonial police curfew whistle signalling 8:00 PM martial curfew (3.5s)
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

def generate_night_cricket_ambience():
    """
    Synthesizes nocturnal Punjab alley atmosphere:
    High-frequency crickets (4.5 kHz & 5.2 kHz chirps),
    low hollow wind drafts through brick haveli canyons (80-140 Hz),
    and a distant haunting minor key resonance.
    """
    random.seed(1919041308)
    duration = 4.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # 1. Rhythmic cricket chirping clusters
    # Crickets chirp in bursts of 3-4 pulses at ~4800 Hz
    t = 0.0
    while t < duration:
        burst_len = random.uniform(0.12, 0.22)
        chirp_freq = random.uniform(4600.0, 5200.0)
        num_pulses = random.randint(3, 5)
        pulse_len = burst_len / num_pulses

        for p in range(num_pulses):
            p_start = t + p * pulse_len
            p_idx = int(p_start * SAMPLE_RATE)
            p_samps = int(pulse_len * 0.75 * SAMPLE_RATE)
            amp = random.uniform(0.18, 0.35)

            for i in range(p_samps):
                idx = p_idx + i
                if idx >= total_samples:
                    break
                st = i / SAMPLE_RATE
                env = math.sin(math.pi * (i / p_samps))
                pulse = math.sin(2.0 * math.pi * chirp_freq * st) * env * amp
                samples[idx] += pulse

        # Pause between cricket bursts
        t += burst_len + random.uniform(0.18, 0.45)

    # 2. Hollow wind drafts whistling through narrow 3-story haveli canyons
    for i in range(total_samples):
        st = i / SAMPLE_RATE
        # Low frequency gusts
        gust = 0.5 + 0.5 * math.sin(2.0 * math.pi * 0.25 * st)
        noise = (random.random() * 2.0 - 1.0) * 0.04
        wind = (math.sin(2.0 * math.pi * 85.0 * st) * 0.08
              + math.sin(2.0 * math.pi * 135.0 * st) * 0.06
              + noise) * gust
        samples[i] += wind

    # 3. Distant sombre reverberation (haunting minor drone of a traumatized city)
    for i in range(total_samples):
        st = i / SAMPLE_RATE
        drone = (math.sin(2.0 * math.pi * 110.0 * st) * 0.05
               + math.sin(2.0 * math.pi * 164.81 * st) * 0.04  # E3
               + math.sin(2.0 * math.pi * 220.0 * st) * 0.02)
        samples[i] += drone

    return samples

def generate_police_whistle_curfew():
    """
    Synthesizes a sharp, piercing British colonial Acme/Metropolitan police whistle.
    Dual resonant pea-whistle frequencies creating a harsh beating trill:
    f1 ~ 2400 Hz, f2 ~ 2650 Hz with 18 Hz trill modulation.
    """
    random.seed(800)
    duration = 3.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Two sharp whistle blasts (e.g., standard police curfew call)
    blasts = [
        (0.20, 1.10, 0.95),  # First blast: 1.1s
        (1.55, 1.35, 1.00),  # Second blast: 1.35s
    ]

    for start_t, blast_len, amp in blasts:
        start_idx = int(start_t * SAMPLE_RATE)
        num_samps = int(blast_len * SAMPLE_RATE)

        for i in range(num_samps):
            idx = start_idx + i
            if idx >= total_samples:
                break
            st = i / SAMPLE_RATE

            # Whistle envelope: explosive puff attack, sustained pressure, sharp release
            attack = 0.04
            release = 0.06
            if st < attack:
                env = (st / attack) ** 0.8
            elif st > (blast_len - release):
                env = ((blast_len - st) / release) ** 1.2
            else:
                env = 1.0

            # Pea rattle modulation (cork pea spinning inside cylinder chamber at ~22 Hz)
            trill = 1.0 + 0.12 * math.sin(2.0 * math.pi * 22.0 * st)

            # Dual acoustic chambers of Acme whistle (2400 Hz and 2640 Hz beat frequency)
            f1 = 2380.0 * trill
            f2 = 2620.0 * trill
            whistle_tone = math.sin(2.0 * math.pi * f1 * st) * 0.50 \
                         + math.sin(2.0 * math.pi * f2 * st) * 0.45 \
                         + math.sin(2.0 * math.pi * (f1 * 2.0) * st) * 0.12 \
                         + (random.random() * 2.0 - 1.0) * 0.08  # Air turbulence hiss

            samples[idx] += whistle_tone * env * amp

    # Alley acoustic slapback echo off high haveli brickwork
    echo_delay = int(0.12 * SAMPLE_RATE)
    for i in range(echo_delay, total_samples):
        samples[i] += samples[i - echo_delay] * 0.22

    return samples

def main():
    audio_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Audio"
    os.makedirs(audio_dir, exist_ok=True)

    print("================ TASK 8 AUDIO SYNTHESIS ================")

    # 1. Night Cricket Ambience
    night_samples = generate_night_cricket_ambience()
    night_path = os.path.join(audio_dir, "SFX_Night_Cricket_Ambience.wav")
    write_wav(night_path, night_samples)

    # 2. Police Curfew Whistle
    whistle_samples = generate_police_whistle_curfew()
    whistle_path = os.path.join(audio_dir, "SFX_Police_Whistle_Curfew.wav")
    write_wav(whistle_path, whistle_samples)

    print("================ TASK 8 AUDIO COMPLETED ================")

if __name__ == "__main__":
    main()
