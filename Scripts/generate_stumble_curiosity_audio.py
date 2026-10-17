"""
PROJECT REVOLUTION — Task 22 Audio Synthesis: Dynamic Pedestrian Reactions & Stumble Voice System
Synthesizes 5 authentic period Punjabi vocal reactions using acoustic formant synthesis:
1. SFX_Voice_Civilian_Stumble_01.wav   (Adult male startled exclamation "Ohe! Sambhal ke!")
2. SFX_Voice_Civilian_Stumble_02.wav   (Bazaar vendor sharp exclamation "Arrey dhyan naal!")
3. SFX_Voice_Civilian_Stumble_03.wav   (Youth friend startled reaction "Oye Kabir, slow down!")
4. SFX_Voice_Civilian_Curiosity_01.wav (Puzzled adult murmur "Ki diggeya uthe? / What fell?")
5. SFX_Voice_Civilian_Curiosity_02.wav (Vendor curious whisper "Aawaz kithon aayi? / Where was that sound?")
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

def synthesize_utterance(syllables, base_f0, duration=1.8):
    """
    Synthesizes multi-syllabic human vocal utterance using formant resonators and glottal pulse excitation.
    """
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    current_time = 0.0
    phase_glottal = 0.0
    
    for syl in syllables:
        syl_dur = syl.get('dur', 0.25)
        syl_samples = int(syl_dur * SAMPLE_RATE)
        f0_target = base_f0 * syl.get('f0_rel', 1.0)
        f1, f2, f3 = syl.get('formants', [550.0, 1500.0, 2500.0])
        breath_lvl = syl.get('breath', 0.08)
        vib_amp = syl.get('vibrato', 0.015)
        gain = syl.get('gain', 0.85)

        bw1 = f1 / 6.0
        bw2 = f2 / 8.0
        bw3 = f3 / 10.0
        
        r1 = math.exp(-math.pi * bw1 / SAMPLE_RATE)
        c1 = 2.0 * r1 * math.cos(2.0 * math.pi * f1 / SAMPLE_RATE)
        c1_2 = -r1 * r1
        
        r2 = math.exp(-math.pi * bw2 / SAMPLE_RATE)
        c2 = 2.0 * r2 * math.cos(2.0 * math.pi * f2 / SAMPLE_RATE)
        c2_2 = -r2 * r2
        
        r3 = math.exp(-math.pi * bw3 / SAMPLE_RATE)
        c3 = 2.0 * r3 * math.cos(2.0 * math.pi * f3 / SAMPLE_RATE)
        c3_2 = -r3 * r3

        y1_1, y1_2 = 0.0, 0.0
        y2_1, y2_2 = 0.0, 0.0
        y3_1, y3_2 = 0.0, 0.0

        start_sample = int(current_time * SAMPLE_RATE)
        for i in range(syl_samples):
            idx = start_sample + i
            if idx >= total_samples:
                break
            
            progress = i / max(1, syl_samples)
            if progress < 0.15:
                env = 0.5 * (1.0 - math.cos(math.pi * progress / 0.15))
            elif progress > 0.80:
                decay_prog = (progress - 0.80) / 0.20
                env = 0.5 * (1.0 + math.cos(math.pi * decay_prog))
            else:
                env = 1.0

            vib = 1.0 + vib_amp * math.sin(2.0 * math.pi * 5.5 * (i / SAMPLE_RATE))
            f0 = f0_target * vib

            phase_glottal += f0 / SAMPLE_RATE
            if phase_glottal >= 1.0:
                phase_glottal -= 1.0

            # Rosenberg glottal pulse model
            tp = 0.40
            tn = 0.16
            if phase_glottal < tp:
                glottal = 0.5 * (1.0 - math.cos(math.pi * phase_glottal / tp))
            elif phase_glottal < (tp + tn):
                glottal = math.cos(math.pi * 0.5 * (phase_glottal - tp) / tn)
            else:
                glottal = 0.0

            glottal += 0.25 * math.sin(4.0 * math.pi * phase_glottal)
            # Add aspiration breath noise
            breath = ((math.sin(17.3 * i) + math.cos(43.7 * i)) * 0.5) * breath_lvl
            source = (glottal * (1.0 - breath_lvl) + breath) * env * gain

            # Resonators
            out1 = source + c1 * y1_1 + c1_2 * y1_2
            y1_2 = y1_1
            y1_1 = out1

            out2 = source + c2 * y2_1 + c2_2 * y2_2
            y2_2 = y2_1
            y2_1 = out2

            out3 = source + c3 * y3_1 + c3_2 * y3_2
            y3_2 = y3_1
            y3_1 = out3

            speech_val = (out1 * 0.55 + out2 * 0.32 + out3 * 0.13)
            samples[idx] += speech_val

        current_time += syl_dur + syl.get('pause', 0.04)

    # Normalize samples
    max_val = max(abs(s) for s in samples) if samples else 1.0
    if max_val > 0.001:
        norm_factor = 0.88 / max_val
        samples = [s * norm_factor for s in samples]

    return samples

def generate_all():
    dest_dirs = [
        os.path.join(os.path.dirname(__file__), "..", "Art", "Audio", "Voice"),
        os.path.join(os.path.dirname(__file__), "..", "Art", "PROJECT", "Voice")
    ]

    tracks = {}

    # 1. Adult Male Stumble ("Ohe! Sambhal ke!" - sudden startled pitch shift)
    tracks["SFX_Voice_Civilian_Stumble_01.wav"] = synthesize_utterance([
        {'dur': 0.22, 'f0_rel': 1.45, 'formants': [450, 1100, 2400], 'gain': 0.95, 'pause': 0.08}, # "Oh!"
        {'dur': 0.18, 'f0_rel': 1.30, 'formants': [350, 1800, 2600], 'gain': 0.90, 'pause': 0.02}, # "Sam-"
        {'dur': 0.26, 'f0_rel': 1.15, 'formants': [600, 1300, 2500], 'gain': 0.85, 'pause': 0.03}, # "-bhal"
        {'dur': 0.28, 'f0_rel': 0.95, 'formants': [450, 1900, 2700], 'gain': 0.78, 'pause': 0.05}, # "ke!"
    ], base_f0=120.0, duration=1.2)

    # 2. Bazaar Vendor Stumble ("Arrey dhyan naal!" - sharp vocal projection)
    tracks["SFX_Voice_Civilian_Stumble_02.wav"] = synthesize_utterance([
        {'dur': 0.16, 'f0_rel': 1.38, 'formants': [700, 1200, 2500], 'gain': 0.92, 'pause': 0.02}, # "A-"
        {'dur': 0.22, 'f0_rel': 1.48, 'formants': [450, 1900, 2600], 'gain': 0.95, 'pause': 0.06}, # "-rrey!"
        {'dur': 0.20, 'f0_rel': 1.25, 'formants': [350, 1800, 2500], 'gain': 0.88, 'pause': 0.02}, # "dhyan"
        {'dur': 0.26, 'f0_rel': 1.05, 'formants': [650, 1250, 2400], 'gain': 0.82, 'pause': 0.04}, # "naal!"
    ], base_f0=146.0, duration=1.1)

    # 3. Youth Friend Stumble ("Oye Kabir, slow down!" - youthful pitch)
    tracks["SFX_Voice_Civilian_Stumble_03.wav"] = synthesize_utterance([
        {'dur': 0.22, 'f0_rel': 1.40, 'formants': [450, 1200, 2800], 'gain': 0.95, 'pause': 0.05}, # "Oye!"
        {'dur': 0.18, 'f0_rel': 1.25, 'formants': [350, 2000, 2900], 'gain': 0.88, 'pause': 0.02}, # "Ka-"
        {'dur': 0.28, 'f0_rel': 1.10, 'formants': [300, 2200, 3100], 'gain': 0.85, 'pause': 0.04}, # "-bir!"
    ], base_f0=225.0, duration=1.0)

    # 4. Puzzled Adult Curiosity ("Ki diggeya uthe? / What fell?" - lower questioning cadence)
    tracks["SFX_Voice_Civilian_Curiosity_01.wav"] = synthesize_utterance([
        {'dur': 0.24, 'f0_rel': 1.05, 'formants': [320, 2200, 2800], 'gain': 0.80, 'pause': 0.04}, # "Ki"
        {'dur': 0.20, 'f0_rel': 1.12, 'formants': [360, 1900, 2600], 'gain': 0.82, 'pause': 0.02}, # "dig-"
        {'dur': 0.24, 'f0_rel': 1.08, 'formants': [550, 1400, 2500], 'gain': 0.78, 'pause': 0.03}, # "-geya"
        {'dur': 0.35, 'f0_rel': 1.28, 'formants': [450, 1100, 2400], 'gain': 0.85, 'pause': 0.05}, # "uthe?" (rising inflection)
    ], base_f0=114.0, duration=1.4)

    # 5. Vendor Curious Whisper ("Aawaz kithon aayi?" - inquisitive vendor whisper)
    tracks["SFX_Voice_Civilian_Curiosity_02.wav"] = synthesize_utterance([
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [700, 1200, 2500], 'gain': 0.75, 'breath': 0.18, 'pause': 0.03}, # "Aa-"
        {'dur': 0.26, 'f0_rel': 1.05, 'formants': [650, 1250, 2450], 'gain': 0.72, 'breath': 0.15, 'pause': 0.05}, # "-waz"
        {'dur': 0.20, 'f0_rel': 1.15, 'formants': [320, 2100, 2750], 'gain': 0.80, 'breath': 0.12, 'pause': 0.02}, # "ki-"
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [450, 1150, 2400], 'gain': 0.75, 'breath': 0.14, 'pause': 0.03}, # "-thon"
        {'dur': 0.32, 'f0_rel': 1.32, 'formants': [350, 2200, 2900], 'gain': 0.82, 'breath': 0.16, 'pause': 0.04}, # "aayi?" (questioning)
    ], base_f0=138.0, duration=1.5)

    for out_dir in dest_dirs:
        for fname, samples in tracks.items():
            out_path = os.path.join(out_dir, fname)
            write_wav(out_path, samples)

    print("\nSuccessfully synthesized 5 dynamic pedestrian stumble & curiosity voice tracks!")

if __name__ == "__main__":
    generate_all()
