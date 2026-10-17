"""
PROJECT REVOLUTION — Task 21 Audio Synthesis: Civilian Dialogue Voice Localization
Synthesizes 14 authentic period Punjabi vocal sound effects using acoustic formant synthesis:
1.  SFX_Voice_RamLubhaya_Bark.wav       (Father's concerned callout across veranda)
2.  SFX_Voice_RamLubhaya_Dialogue.wav   (Paternal advice on curfew & swadeshi cloth)
3.  SFX_Voice_Ghasita_Bark.wav          (Melodic traditional Bhishti water-carrier call)
4.  SFX_Voice_Ghasita_Dialogue.wav      (Humble reflection on mohalla well unity)
5.  SFX_Voice_HiraHalwai_Bark.wav       (Energetic bazaar tea stall vendor shout)
6.  SFX_Voice_HiraHalwai_Dialogue.wav   (Tea gossip regarding British troops & Hartal)
7.  SFX_Voice_LalaKaramChand_Bark.wav   (Mandi textile merchant market projection)
8.  SFX_Voice_LalaKaramChand_Dialogue.wav (Delivering khadi coat & boycott discussions)
9.  SFX_Voice_PanditKashiRam_Bark.wav   (Headmaster's courtyard morning bell call)
10. SFX_Voice_PanditKashiRam_Dialogue.wav (Scholarly discourse on knowledge and freedom)
11. SFX_Voice_KartarSingh_Bark.wav      (12-year-old schoolmate kite banter shout)
12. SFX_Voice_KartarSingh_Dialogue.wav  (Conspiratorial whispered excitement about leaflets)
13. SFX_Voice_ConstableGurdial_Curfew.wav (Imperial Police stern curfew command)
14. SFX_Voice_ConstableGurdial_Suspicion.wav (Suspicious patrol challenge query)
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

def synthesize_utterance(syllables, base_f0, character_type="adult_male", duration=2.2):
    """
    Synthesizes a multi-syllabic human vocal utterance using formant resonators and glottal pulse excitation.
    syllables: list of dicts with keys 'dur', 'f0_rel', 'formants' [F1, F2, F3], 'breath', 'vibrato'
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

        # Resonator state variables for 2-pole IIR filters (F1, F2, F3)
        y1_1, y1_2 = 0.0, 0.0
        y2_1, y2_2 = 0.0, 0.0
        y3_1, y3_2 = 0.0, 0.0

        # Precalculate bandwidths and filter coefficients
        # Q factors: Q1 ~ 6, Q2 ~ 8, Q3 ~ 10
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

        start_sample = int(current_time * SAMPLE_RATE)
        for i in range(syl_samples):
            idx = start_sample + i
            if idx >= total_samples:
                break
            
            t_syl = i / SAMPLE_RATE
            progress = i / max(1, syl_samples)
            
            # Syllable amplitude envelope (smooth trapezoid / Hann-like window)
            if progress < 0.15:
                env = 0.5 * (1.0 - math.cos(math.pi * progress / 0.15))
            elif progress > 0.80:
                decay_prog = (progress - 0.80) / 0.20
                env = 0.5 * (1.0 + math.cos(math.pi * decay_prog))
            else:
                env = 1.0

            # Pitch intonation contour with micro-vibrato (5.5 Hz)
            vib = vib_amp * math.sin(2.0 * math.pi * 5.5 * t_syl)
            inst_f0 = f0_target * (1.0 + vib)
            
            # Glottal pulse generator (Rosenberg polynomial / harmonic pulse)
            phase_glottal += inst_f0 / SAMPLE_RATE
            if phase_glottal >= 1.0:
                phase_glottal -= 1.0
                
            # Rosenberg glottal model approximation
            if phase_glottal < 0.40:
                glot = 3.0 * (phase_glottal / 0.40)**2 - 2.0 * (phase_glottal / 0.40)**3
            elif phase_glottal < 0.60:
                glot = 1.0 - ((phase_glottal - 0.40) / 0.20)**2
            else:
                glot = 0.0

            # Add subtle aspiration noise (white noise burst at consonant boundaries)
            noise = (math.sin(idx * 7919.13) * 43758.5453) % 1.0 - 0.5
            excitation = (glot * 0.90 + noise * breath_lvl) * env

            # Formant filtering (parallel resonators)
            # F1
            out1 = (1.0 - r1) * excitation + c1 * y1_1 + c1_2 * y1_2
            y1_2 = y1_1
            y1_1 = out1

            # F2
            out2 = (1.0 - r2) * excitation * 0.70 + c2 * y2_1 + c2_2 * y2_2
            y2_2 = y2_1
            y2_1 = out2

            # F3
            out3 = (1.0 - r3) * excitation * 0.45 + c3 * y3_1 + c3_2 * y3_2
            y3_2 = y3_1
            y3_1 = out3

            # Composite acoustic output
            sample_val = (out1 * 0.50 + out2 * 0.35 + out3 * 0.15) * gain
            samples[idx] += sample_val

        current_time += syl_dur + syl.get('pause', 0.04)

    # Master normalization
    max_peak = max(abs(s) for s in samples) if samples else 0.0
    if max_peak > 0.01:
        norm_factor = 0.88 / max_peak
        samples = [s * norm_factor for s in samples]

    return samples

# ---------------------------------------------------------------------------
# Specific Character Utterance Presets
# ---------------------------------------------------------------------------

def gen_ram_lubhaya_bark():
    # "Ka-bir put-tar! A-ndar a-ao!" (Warm paternal calling tone, ~114 Hz)
    syllables = [
        {'dur': 0.18, 'f0_rel': 1.02, 'formants': [650, 1200, 2400], 'gain': 0.85}, # Ka
        {'dur': 0.28, 'f0_rel': 1.12, 'formants': [400, 2100, 2700], 'gain': 0.95}, # bir
        {'dur': 0.08, 'pause': 0.06},
        {'dur': 0.16, 'f0_rel': 1.08, 'formants': [450, 1100, 2300], 'gain': 0.85}, # put
        {'dur': 0.32, 'f0_rel': 0.92, 'formants': [600, 1300, 2500], 'gain': 0.90}, # tar
        {'dur': 0.10, 'pause': 0.08},
        {'dur': 0.22, 'f0_rel': 1.05, 'formants': [680, 1350, 2450], 'gain': 0.90}, # An
        {'dur': 0.20, 'f0_rel': 0.96, 'formants': [500, 1150, 2350], 'gain': 0.85}, # dar
        {'dur': 0.35, 'f0_rel': 0.86, 'formants': [620, 1100, 2400], 'gain': 0.80}  # aao
    ]
    return synthesize_utterance(syllables, base_f0=114.0, duration=2.2)

def gen_ram_lubhaya_dialogue():
    # "Sun puttar, Lala Karam Chand kol coat de ke aavin..." (Measured paternal advice, ~108 Hz)
    syllables = [
        {'dur': 0.24, 'f0_rel': 1.04, 'formants': [420, 1050, 2300], 'gain': 0.85}, # Sun
        {'dur': 0.18, 'f0_rel': 1.08, 'formants': [450, 1100, 2350], 'gain': 0.85}, # put
        {'dur': 0.26, 'f0_rel': 0.96, 'formants': [600, 1250, 2450], 'gain': 0.80}, # tar
        {'dur': 0.12, 'pause': 0.06},
        {'dur': 0.22, 'f0_rel': 1.06, 'formants': [650, 1350, 2500], 'gain': 0.85}, # La
        {'dur': 0.22, 'f0_rel': 1.00, 'formants': [650, 1300, 2450], 'gain': 0.85}, # la
        {'dur': 0.20, 'f0_rel': 0.98, 'formants': [620, 1200, 2400], 'gain': 0.80}, # Ka
        {'dur': 0.32, 'f0_rel': 0.90, 'formants': [650, 1250, 2450], 'gain': 0.85}, # ram
        {'dur': 0.25, 'f0_rel': 1.02, 'formants': [480, 1150, 2350], 'gain': 0.85}, # coat
        {'dur': 0.35, 'f0_rel': 0.85, 'formants': [600, 1800, 2600], 'gain': 0.75}  # aavin
    ]
    return synthesize_utterance(syllables, base_f0=108.0, duration=2.6)

def gen_ghasita_bark():
    # "Bhishti aya! Thanda meetha pani!" (Melodic street cry with vibrato, ~132 Hz)
    syllables = [
        {'dur': 0.20, 'f0_rel': 1.02, 'formants': [400, 1950, 2600], 'gain': 0.85}, # Bhish
        {'dur': 0.35, 'f0_rel': 1.18, 'formants': [350, 2200, 2800], 'vibrato': 0.03, 'gain': 0.95}, # ti
        {'dur': 0.28, 'f0_rel': 1.10, 'formants': [680, 1350, 2500], 'gain': 0.90}, # a
        {'dur': 0.38, 'f0_rel': 0.94, 'formants': [620, 1150, 2400], 'gain': 0.85}, # ya!
        {'dur': 0.15, 'pause': 0.08},
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [640, 1300, 2450], 'gain': 0.90}, # Than
        {'dur': 0.28, 'f0_rel': 1.04, 'formants': [620, 1200, 2400], 'gain': 0.85}, # da
        {'dur': 0.25, 'f0_rel': 1.16, 'formants': [400, 2150, 2750], 'gain': 0.90}, # mee
        {'dur': 0.38, 'f0_rel': 0.88, 'formants': [600, 1250, 2450], 'vibrato': 0.025, 'gain': 0.80} # tha pa-ni
    ]
    return synthesize_utterance(syllables, base_f0=132.0, duration=2.8)

def gen_ghasita_dialogue():
    # "Salam chhotey Kabir, kuan da pani sab lai ikko jeya hai..." (Humble reflection, ~126 Hz)
    syllables = [
        {'dur': 0.22, 'f0_rel': 1.04, 'formants': [620, 1300, 2450], 'gain': 0.85}, # Sa
        {'dur': 0.30, 'f0_rel': 0.98, 'formants': [650, 1250, 2400], 'gain': 0.85}, # lam
        {'dur': 0.20, 'f0_rel': 1.08, 'formants': [480, 1100, 2350], 'gain': 0.85}, # chho
        {'dur': 0.25, 'f0_rel': 0.95, 'formants': [550, 1750, 2600], 'gain': 0.80}, # tey
        {'dur': 0.20, 'f0_rel': 1.04, 'formants': [650, 1250, 2450], 'gain': 0.85}, # Ka
        {'dur': 0.28, 'f0_rel': 0.92, 'formants': [420, 2050, 2700], 'gain': 0.80}, # bir
        {'dur': 0.12, 'pause': 0.05},
        {'dur': 0.25, 'f0_rel': 1.06, 'formants': [450, 1150, 2350], 'gain': 0.85}, # ku
        {'dur': 0.32, 'f0_rel': 0.90, 'formants': [680, 1300, 2500], 'gain': 0.80}  # an
    ]
    return synthesize_utterance(syllables, base_f0=126.0, duration=2.3)

def gen_hira_halwai_bark():
    # "Garam chai! Elaichi wali kadak kulhad chai!" (High energy bazaar shout, ~152 Hz)
    syllables = [
        {'dur': 0.16, 'f0_rel': 1.05, 'formants': [620, 1350, 2500], 'gain': 0.90}, # Ga
        {'dur': 0.24, 'f0_rel': 1.20, 'formants': [650, 1300, 2450], 'gain': 0.95}, # ram
        {'dur': 0.28, 'f0_rel': 1.28, 'formants': [680, 1850, 2700], 'gain': 1.00}, # chai!
        {'dur': 0.10, 'pause': 0.06},
        {'dur': 0.18, 'f0_rel': 1.15, 'formants': [550, 1800, 2650], 'gain': 0.90}, # E
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [650, 1300, 2450], 'gain': 0.90}, # lai
        {'dur': 0.24, 'f0_rel': 1.02, 'formants': [400, 2150, 2750], 'gain': 0.85}, # chi
        {'dur': 0.18, 'f0_rel': 1.18, 'formants': [640, 1250, 2400], 'gain': 0.95}, # ka
        {'dur': 0.28, 'f0_rel': 0.92, 'formants': [600, 1200, 2350], 'gain': 0.85}  # dak
    ]
    return synthesize_utterance(syllables, base_f0=152.0, duration=2.2)

def gen_hira_halwai_dialogue():
    # "Pee la kulhad chai Kabir, mandi vich sab Hartal di gal karde ne..." (~144 Hz)
    syllables = [
        {'dur': 0.22, 'f0_rel': 1.06, 'formants': [380, 2150, 2750], 'gain': 0.85}, # Pee
        {'dur': 0.18, 'f0_rel': 1.02, 'formants': [620, 1300, 2450], 'gain': 0.85}, # la
        {'dur': 0.20, 'f0_rel': 1.12, 'formants': [480, 1150, 2350], 'gain': 0.90}, # kul
        {'dur': 0.25, 'f0_rel': 0.95, 'formants': [600, 1200, 2400], 'gain': 0.85}, # had
        {'dur': 0.28, 'f0_rel': 1.18, 'formants': [680, 1800, 2650], 'gain': 0.95}, # chai
        {'dur': 0.12, 'pause': 0.05},
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [640, 1250, 2400], 'gain': 0.85}, # Har
        {'dur': 0.32, 'f0_rel': 0.88, 'formants': [650, 1300, 2450], 'gain': 0.80}  # tal
    ]
    return synthesize_utterance(syllables, base_f0=144.0, duration=2.1)

def gen_lala_karam_chand_bark():
    # "Swadeshi Khadi! Desi resham te kapaas! Aao dekho!" (Merchant market shout, ~122 Hz)
    syllables = [
        {'dur': 0.20, 'f0_rel': 1.04, 'formants': [580, 1200, 2400], 'gain': 0.85}, # Swa
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [520, 1750, 2600], 'gain': 0.90}, # de
        {'dur': 0.32, 'f0_rel': 0.96, 'formants': [400, 2150, 2750], 'gain': 0.85}, # shi
        {'dur': 0.10, 'pause': 0.05},
        {'dur': 0.24, 'f0_rel': 1.16, 'formants': [680, 1350, 2500], 'gain': 0.95}, # Kha
        {'dur': 0.30, 'f0_rel': 0.90, 'formants': [400, 2100, 2700], 'gain': 0.85}, # di!
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [650, 1300, 2450], 'gain': 0.85}, # Aa
        {'dur': 0.28, 'f0_rel': 0.86, 'formants': [480, 1100, 2350], 'gain': 0.80}  # o!
    ]
    return synthesize_utterance(syllables, base_f0=122.0, duration=2.1)

def gen_lala_karam_chand_dialogue():
    # "Aao puttar Kabir, coat di silai dekhiye... Swadeshi hi saadi taqat hai..." (~118 Hz)
    syllables = [
        {'dur': 0.24, 'f0_rel': 1.05, 'formants': [650, 1300, 2450], 'gain': 0.85}, # Aa
        {'dur': 0.26, 'f0_rel': 0.96, 'formants': [500, 1150, 2350], 'gain': 0.80}, # o
        {'dur': 0.18, 'f0_rel': 1.06, 'formants': [450, 1100, 2300], 'gain': 0.85}, # put
        {'dur': 0.26, 'f0_rel': 0.92, 'formants': [600, 1250, 2400], 'gain': 0.80}, # tar
        {'dur': 0.22, 'f0_rel': 1.08, 'formants': [650, 1350, 2500], 'gain': 0.85}, # si
        {'dur': 0.32, 'f0_rel': 0.94, 'formants': [620, 1800, 2650], 'gain': 0.85}, # lai
        {'dur': 0.30, 'f0_rel': 0.85, 'formants': [650, 1250, 2400], 'gain': 0.75}  # ta-qat
    ]
    return synthesize_utterance(syllables, base_f0=118.0, duration=2.1)

def gen_pandit_kashi_ram_bark():
    # "Vidyarthi bacho! Ghanta vajn wala hai! Class vich aao!" (~138 Hz)
    syllables = [
        {'dur': 0.18, 'f0_rel': 1.02, 'formants': [420, 2050, 2700], 'gain': 0.85}, # Vid
        {'dur': 0.22, 'f0_rel': 1.14, 'formants': [650, 1300, 2450], 'gain': 0.90}, # yar
        {'dur': 0.28, 'f0_rel': 0.98, 'formants': [400, 2150, 2750], 'gain': 0.85}, # thi
        {'dur': 0.10, 'pause': 0.05},
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [620, 1250, 2400], 'gain': 0.85}, # ba
        {'dur': 0.26, 'f0_rel': 0.92, 'formants': [480, 1150, 2350], 'gain': 0.80}, # cho!
        {'dur': 0.24, 'f0_rel': 1.18, 'formants': [640, 1300, 2450], 'gain': 0.95}, # ghan
        {'dur': 0.32, 'f0_rel': 0.88, 'formants': [600, 1200, 2400], 'gain': 0.85}  # ta
    ]
    return synthesize_utterance(syllables, base_f0=138.0, duration=2.1)

def gen_pandit_kashi_ram_dialogue():
    # "Namaste Kabir, gyan hi azaadi da rasta hai..." (~132 Hz)
    syllables = [
        {'dur': 0.22, 'f0_rel': 1.04, 'formants': [620, 1300, 2450], 'gain': 0.85}, # Na
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [600, 1750, 2600], 'gain': 0.85}, # mas
        {'dur': 0.28, 'f0_rel': 0.96, 'formants': [500, 1850, 2650], 'gain': 0.80}, # te
        {'dur': 0.12, 'pause': 0.06},
        {'dur': 0.26, 'f0_rel': 1.10, 'formants': [650, 1350, 2500], 'gain': 0.90}, # gyan
        {'dur': 0.25, 'f0_rel': 1.04, 'formants': [380, 2150, 2750], 'gain': 0.85}, # hi
        {'dur': 0.30, 'f0_rel': 1.08, 'formants': [680, 1300, 2450], 'gain': 0.85}, # a-za
        {'dur': 0.35, 'f0_rel': 0.86, 'formants': [400, 2100, 2700], 'gain': 0.75}  # di
    ]
    return synthesize_utterance(syllables, base_f0=132.0, duration=2.3)

def gen_kartar_singh_bark():
    # "Kabir! Patang dekho upar! Katra Jaimal Singh di patang hai!" (Youthful 12yo shout, ~228 Hz)
    syllables = [
        {'dur': 0.16, 'f0_rel': 1.06, 'formants': [680, 1450, 2800], 'gain': 0.90}, # Ka
        {'dur': 0.26, 'f0_rel': 1.25, 'formants': [420, 2300, 3100], 'gain': 1.00}, # bir!
        {'dur': 0.10, 'pause': 0.06},
        {'dur': 0.18, 'f0_rel': 1.15, 'formants': [650, 1400, 2750], 'gain': 0.90}, # Pa
        {'dur': 0.24, 'f0_rel': 1.20, 'formants': [620, 1350, 2700], 'gain': 0.95}, # tang
        {'dur': 0.18, 'f0_rel': 1.10, 'formants': [500, 1850, 2850], 'gain': 0.90}, # dek
        {'dur': 0.28, 'f0_rel': 0.94, 'formants': [480, 1250, 2600], 'gain': 0.85}  # ho!
    ]
    return synthesize_utterance(syllables, base_f0=228.0, duration=1.8)

def gen_kartar_singh_dialogue():
    # "Kabir, Peepal tree kol khufiya parcha mileya! Chheti kar school da ghanta vajaiye!" (~215 Hz)
    syllables = [
        {'dur': 0.18, 'f0_rel': 1.08, 'formants': [680, 1400, 2750], 'gain': 0.85}, # Ka
        {'dur': 0.25, 'f0_rel': 1.18, 'formants': [420, 2250, 3050], 'gain': 0.95}, # bir
        {'dur': 0.10, 'pause': 0.05},
        {'dur': 0.22, 'f0_rel': 1.12, 'formants': [520, 1900, 2900], 'gain': 0.90}, # par
        {'dur': 0.26, 'f0_rel': 1.00, 'formants': [650, 1350, 2700], 'gain': 0.85}, # cha
        {'dur': 0.20, 'f0_rel': 1.15, 'formants': [450, 1250, 2650], 'gain': 0.90}, # ghan
        {'dur': 0.32, 'f0_rel': 0.88, 'formants': [620, 1300, 2600], 'gain': 0.80}  # ta
    ]
    return synthesize_utterance(syllables, base_f0=215.0, duration=1.9)

def gen_constable_gurdial_curfew():
    # "Ruk oye! Section 144 laagu hai! Galiyan khali karo!" (Stern militaristic police command, ~102 Hz)
    syllables = [
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [420, 1050, 2300], 'gain': 0.95}, # Ruk
        {'dur': 0.30, 'f0_rel': 1.25, 'formants': [500, 1150, 2350], 'gain': 1.00}, # oye!
        {'dur': 0.12, 'pause': 0.08},
        {'dur': 0.22, 'f0_rel': 1.08, 'formants': [550, 1750, 2550], 'gain': 0.90}, # Sec
        {'dur': 0.25, 'f0_rel': 0.98, 'formants': [500, 1200, 2350], 'gain': 0.85}, # tion
        {'dur': 0.28, 'f0_rel': 1.16, 'formants': [650, 1300, 2450], 'gain': 0.95}, # laa
        {'dur': 0.32, 'f0_rel': 0.90, 'formants': [450, 1100, 2300], 'gain': 0.85}, # gu
        {'dur': 0.38, 'f0_rel': 0.82, 'formants': [480, 1150, 2350], 'gain': 0.80}  # ka-ro!
    ]
    return synthesize_utterance(syllables, base_f0=102.0, duration=2.4)

def gen_constable_gurdial_suspicion():
    # "Kaun hai othe? Parwana dikhao!" (Sharp suspicious challenge query, ~110 Hz)
    syllables = [
        {'dur': 0.25, 'f0_rel': 1.08, 'formants': [500, 1100, 2350], 'gain': 0.90}, # Kaun
        {'dur': 0.22, 'f0_rel': 1.18, 'formants': [620, 1800, 2600], 'gain': 0.95}, # hai
        {'dur': 0.28, 'f0_rel': 1.28, 'formants': [520, 1250, 2400], 'gain': 1.00}, # o-the?
        {'dur': 0.14, 'pause': 0.08},
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [650, 1300, 2450], 'gain': 0.90}, # Par
        {'dur': 0.28, 'f0_rel': 1.16, 'formants': [620, 1250, 2400], 'gain': 0.90}, # wa
        {'dur': 0.35, 'f0_rel': 0.86, 'formants': [480, 1150, 2350], 'gain': 0.80}  # na!
    ]
    return synthesize_utterance(syllables, base_f0=110.0, duration=2.2)

def main():
    print("================================================================================")
    print("  PROJECT REVOLUTION — TASK 21 CIVILIAN DIALOGUE VOICE SYNTHESIS")
    print("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dirs = [
        os.path.join(base_dir, "Art", "Audio", "Voice"),
        os.path.join(base_dir, "Art", "PROJECT", "Voice")
    ]

    generators = [
        ("SFX_Voice_RamLubhaya_Bark.wav", gen_ram_lubhaya_bark),
        ("SFX_Voice_RamLubhaya_Dialogue.wav", gen_ram_lubhaya_dialogue),
        ("SFX_Voice_Ghasita_Bark.wav", gen_ghasita_bark),
        ("SFX_Voice_Ghasita_Dialogue.wav", gen_ghasita_dialogue),
        ("SFX_Voice_HiraHalwai_Bark.wav", gen_hira_halwai_bark),
        ("SFX_Voice_HiraHalwai_Dialogue.wav", gen_hira_halwai_dialogue),
        ("SFX_Voice_LalaKaramChand_Bark.wav", gen_lala_karam_chand_bark),
        ("SFX_Voice_LalaKaramChand_Dialogue.wav", gen_lala_karam_chand_dialogue),
        ("SFX_Voice_PanditKashiRam_Bark.wav", gen_pandit_kashi_ram_bark),
        ("SFX_Voice_PanditKashiRam_Dialogue.wav", gen_pandit_kashi_ram_dialogue),
        ("SFX_Voice_KartarSingh_Bark.wav", gen_kartar_singh_bark),
        ("SFX_Voice_KartarSingh_Dialogue.wav", gen_kartar_singh_dialogue),
        ("SFX_Voice_ConstableGurdial_Curfew.wav", gen_constable_gurdial_curfew),
        ("SFX_Voice_ConstableGurdial_Suspicion.wav", gen_constable_gurdial_suspicion)
    ]

    for filename, gen_fn in generators:
        samples = gen_fn()
        for d in out_dirs:
            full_path = os.path.join(d, filename)
            write_wav(full_path, samples)

    print(f"\n[SUCCESS] All {len(generators)} authentic voice audio tracks synthesized across {len(out_dirs)} output directories.")

if __name__ == "__main__":
    main()
