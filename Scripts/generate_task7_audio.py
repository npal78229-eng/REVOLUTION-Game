"""
PROJECT REVOLUTION — Task 7: The Fateful Afternoon of April 13, 1919
Audio Synthesizer: Bugle Call & Crowd Panic
Generates 16-bit 44.1kHz PCM WAV audio for:
1. SFX_Bugle_Call_Charge.wav: Period British military bugle call signalling the firing order (4.2s)
2. SFX_Crowd_Panic_Scream.wav: Sudden stampede, shouting voices and chaotic reverberations (4.5s)
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

def generate_bugle_call_charge():
    """
    Synthesizes a period British military bugle call ("The Charge / Fire").
    Bugles only play natural notes of the harmonic series:
    Low G (196 Hz), C4 (261.6 Hz), E4 (329.6 Hz), G4 (392.0 Hz), C5 (523.2 Hz).
    """
    duration = 4.2
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # Bugle melody sequence: (start_time, frequency, note_duration, amplitude)
    # Fanfare: G3, C4, E4, G4, C5, high flourish
    notes = [
        (0.10, 261.63, 0.22, 0.85), # C4
        (0.35, 329.63, 0.22, 0.85), # E4
        (0.60, 392.00, 0.28, 0.90), # G4
        (0.95, 261.63, 0.20, 0.80), # C4
        (1.20, 329.63, 0.20, 0.85), # E4
        (1.45, 392.00, 0.35, 0.95), # G4
        (1.90, 523.25, 0.45, 1.00), # C5 (high sustained peak)
        (2.45, 392.00, 0.22, 0.90), # G4
        (2.70, 523.25, 0.70, 0.98), # C5 (final resonant charge note)
    ]

    for start_t, f0, note_len, amp in notes:
        start_idx = int(start_t * SAMPLE_RATE)
        num_samps = int(note_len * SAMPLE_RATE)

        for i in range(num_samps):
            idx = start_idx + i
            if idx >= total_samples:
                break
            t = i / SAMPLE_RATE

            # Brass attack and decay envelope
            attack_time = 0.025
            if t < attack_time:
                env = (t / attack_time) ** 1.5
            else:
                decay_progress = (t - attack_time) / (note_len - attack_time)
                env = math.exp(-1.8 * decay_progress)

            # Rich brass harmonic spectrum (even & odd harmonics)
            # Characteristic bright trumpet/bugle overtones
            brass = math.sin(2.0 * math.pi * f0 * t) * 0.45 \
                  + math.sin(2.0 * math.pi * f0 * 2.0 * t) * 0.25 \
                  + math.sin(2.0 * math.pi * f0 * 3.0 * t) * 0.18 \
                  + math.sin(2.0 * math.pi * f0 * 4.0 * t) * 0.12 \
                  + math.sin(2.0 * math.pi * f0 * 5.0 * t) * 0.08 \
                  + math.sin(2.0 * math.pi * f0 * 6.0 * t) * 0.04

            # Slight initial brass "spit" / attack noise
            if t < 0.03:
                brass += (random.random() * 2.0 - 1.0) * 0.08 * (1.0 - t/0.03)

            samples[idx] += brass * env * amp

    # Reverb and garden wall acoustic reflections
    reverb_delays = [0.08, 0.16, 0.24, 0.35]
    reverb_gains = [0.22, 0.15, 0.10, 0.06]
    for delay, gain in zip(reverb_delays, reverb_gains):
        d_samples = int(delay * SAMPLE_RATE)
        for i in range(d_samples, total_samples):
            samples[i] += samples[i - d_samples] * gain

    return samples

def generate_crowd_panic_scream():
    """
    Synthesizes sudden crowd panic: stampede footsteps, shouting voices,
    reverberating clamor, and chaotic surging echoes off 5-meter brick walls.
    """
    random.seed(19190413)
    duration = 4.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples

    # 1. Distant and near vocal cries ("Bhaago!", shrill screams, shouting)
    shout_events = [
        (0.15, 340.0, 0.40, 0.8),
        (0.30, 480.0, 0.60, 0.9),
        (0.55, 290.0, 0.45, 0.85),
        (0.80, 520.0, 0.70, 0.95),
        (1.10, 310.0, 0.50, 0.8),
        (1.40, 440.0, 0.65, 0.9),
        (1.75, 380.0, 0.55, 0.85),
        (2.10, 560.0, 0.75, 1.0),
        (2.50, 330.0, 0.60, 0.85),
        (2.90, 460.0, 0.80, 0.95),
        (3.30, 390.0, 0.70, 0.9),
        (3.80, 510.0, 0.65, 0.85)
    ]

    for start_t, f0, length, amp in shout_events:
        start_idx = int(start_t * SAMPLE_RATE)
        s_len = int(length * SAMPLE_RATE)
        for i in range(s_len):
            idx = start_idx + i
            if idx >= total_samples:
                break
            t = i / SAMPLE_RATE
            # Human cry envelope: rapid attack, trembling sustain, trailing off
            env = math.sin(math.pi * (i / s_len)) ** 0.8
            # Pitch vibrato and panic flutter
            flutter = 1.0 + 0.05 * math.sin(2.0 * math.pi * 9.0 * t)
            cur_f = f0 * flutter
            vocal = math.sin(2.0 * math.pi * cur_f * t) * 0.4 \
                  + math.sin(2.0 * math.pi * cur_f * 2.1 * t) * 0.3 \
                  + math.sin(2.0 * math.pi * cur_f * 3.2 * t) * 0.15 \
                  + (random.random() * 2.0 - 1.0) * 0.15
            samples[idx] += vocal * env * amp

    # 2. Dense frantic stampede footfalls (thousands of feet scuffling and pounding)
    for _ in range(120):
        t_foot = random.uniform(0.1, 4.2)
        f_idx = int(t_foot * SAMPLE_RATE)
        foot_len = int(SAMPLE_RATE * random.uniform(0.04, 0.09))
        foot_f0 = random.uniform(70.0, 160.0)
        foot_amp = random.uniform(0.15, 0.45)
        for i in range(foot_len):
            idx = f_idx + i
            if idx >= total_samples:
                break
            t = i / SAMPLE_RATE
            env = math.exp(-35.0 * t)
            foot = (math.sin(2.0 * math.pi * foot_f0 * t) + (random.random() * 2.0 - 1.0) * 0.6) * env * foot_amp
            samples[idx] += foot

    # 3. Overall surging roar of 20,000 people trapped in an enclosure
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # Progressive roar building up from t=0.2 to t=4.0
        build = min(1.0, max(0.0, (t - 0.2) / 1.5))
        rumble = (math.sin(2.0 * math.pi * 45.0 * t) * 0.12
                + math.sin(2.0 * math.pi * 85.0 * t) * 0.10
                + math.sin(2.0 * math.pi * 125.0 * t) * 0.08
                + (random.random() * 2.0 - 1.0) * 0.09) * build
        samples[i] += rumble

    return samples

def main():
    audio_dir = r"C:\Users\npal7\PROJECT\REVOLUTION\Art\Audio"
    os.makedirs(audio_dir, exist_ok=True)

    print("================ TASK 7 AUDIO SYNTHESIS ================")
    
    # 1. Bugle Call
    bugle_samples = generate_bugle_call_charge()
    bugle_path = os.path.join(audio_dir, "SFX_Bugle_Call_Charge.wav")
    write_wav(bugle_path, bugle_samples)

    # 2. Crowd Panic Scream
    panic_samples = generate_crowd_panic_scream()
    panic_path = os.path.join(audio_dir, "SFX_Crowd_Panic_Scream.wav")
    write_wav(panic_path, panic_samples)

    print("================ TASK 7 AUDIO COMPLETED ================")

if __name__ == "__main__":
    main()
