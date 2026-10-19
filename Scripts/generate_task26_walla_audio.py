"""
PROJECT REVOLUTION — Task 26 Audio Synthesis: Multi-Dialect Punjabi Voice Recording Expansion
Synthesizes 8 authentic period Punjabi vocal vendor cries and crowd walla across Majhi and Doabi vernacular:

Majhi Dialect (Amritsar / Lahore Urban Bazaar):
1. SFX_Voice_Majhi_SabziWalla_Bark.wav    ("Taaza saag te gobi lai lo ji! Majhe da taaza saal!")
2. SFX_Voice_Majhi_PatrikaHawker_Bark.wav ("Waqt di aawaz! Akhbar padho! Rowlatt Act di khabar!")
3. SFX_Voice_Majhi_ChanaVendor_Bark.wav   ("Chana jor garam masaledaar! Mazedaar garma-garam!")
4. SFX_Voice_Majhi_ElderMatron_Bark.wav   ("Ve bachiyo dhyan naal khelo, galli vich police ghumdi e!")

Doabi Dialect (Jalandhar / Hoshiarpur Agrarian Pilgrims & Traders):
5. SFX_Voice_Doabi_KulfiWalla_Bark.wav    ("Thandi kulfi pista-badam! Aao bai kulfi khao!")
6. SFX_Voice_Doabi_KumharPotter_Bark.wav  ("Pakke kooje te surahiyan! Thanda jheel warga paani!")
7. SFX_Voice_Doabi_MandiArhtiya_Bark.wav  ("Navi kanak da daana! Khari toli khara wapar!")
8. SFX_Voice_Doabi_MazdoorPorter_Bark.wav ("Bacha ke ji bacha ke! Bhari gathri hai, raah chaddo!")
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

def synthesize_utterance(syllables, base_f0, duration=2.4):
    """
    Synthesizes multi-syllabic human vocal utterances with parallel 3-formant resonators and glottal pulse excitation.
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
        vib_amp = syl.get('vibrato', 0.018)
        gain = syl.get('gain', 0.88)

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
            
            t_syl = i / SAMPLE_RATE
            progress = i / max(1, syl_samples)
            
            if progress < 0.15:
                env = 0.5 * (1.0 - math.cos(math.pi * progress / 0.15))
            elif progress > 0.80:
                decay_prog = (progress - 0.80) / 0.20
                env = 0.5 * (1.0 + math.cos(math.pi * decay_prog))
            else:
                env = 1.0

            vib = vib_amp * math.sin(2.0 * math.pi * 5.5 * t_syl)
            inst_f0 = f0_target * (1.0 + vib)
            
            phase_glottal += inst_f0 / SAMPLE_RATE
            if phase_glottal >= 1.0:
                phase_glottal -= 1.0
                
            if phase_glottal < 0.40:
                glot = 3.0 * (phase_glottal / 0.40)**2 - 2.0 * (phase_glottal / 0.40)**3
            elif phase_glottal < 0.60:
                glot = 1.0 - ((phase_glottal - 0.40) / 0.20)**2
            else:
                glot = 0.0

            noise = (math.sin(idx * 7919.13) * 43758.5453) % 1.0 - 0.5
            excitation = (glot * 0.90 + noise * breath_lvl) * env

            out1 = (1.0 - r1) * excitation + c1 * y1_1 + c1_2 * y1_2
            y1_2 = y1_1
            y1_1 = out1

            out2 = (1.0 - r2) * excitation * 0.70 + c2 * y2_1 + c2_2 * y2_2
            y2_2 = y2_1
            y2_1 = out2

            out3 = (1.0 - r3) * excitation * 0.45 + c3 * y3_1 + c3_2 * y3_2
            y3_2 = y3_1
            y3_1 = out3

            sample_val = (out1 * 0.50 + out2 * 0.35 + out3 * 0.15) * gain
            samples[idx] += sample_val

        current_time += syl_dur + syl.get('pause', 0.04)

    max_peak = max(abs(s) for s in samples) if samples else 0.0
    if max_peak > 0.01:
        norm_factor = 0.88 / max_peak
        samples = [s * norm_factor for s in samples]

    return samples

# ---------------------------------------------------------------------------
# Majhi Dialect Walla Utterances
# ---------------------------------------------------------------------------

def gen_majhi_sabzi():
    # "Taa-za saag te go-bi lai lo ji!" (Majhi energetic market cry, ~148 Hz)
    syllables = [
        {'dur': 0.20, 'f0_rel': 1.05, 'formants': [650, 1300, 2450], 'gain': 0.90}, # Taa
        {'dur': 0.22, 'f0_rel': 1.15, 'formants': [620, 1250, 2400], 'gain': 0.92}, # za
        {'dur': 0.28, 'f0_rel': 1.18, 'formants': [680, 1380, 2520], 'gain': 0.95}, # saag
        {'dur': 0.10, 'pause': 0.05},
        {'dur': 0.18, 'f0_rel': 1.02, 'formants': [500, 1800, 2600], 'gain': 0.88}, # te
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [480, 1150, 2350], 'gain': 0.90}, # go
        {'dur': 0.24, 'f0_rel': 1.04, 'formants': [380, 2150, 2750], 'gain': 0.92}, # bi
        {'dur': 0.10, 'pause': 0.06},
        {'dur': 0.26, 'f0_rel': 1.12, 'formants': [650, 1300, 2450], 'gain': 0.92}, # lai
        {'dur': 0.22, 'f0_rel': 0.96, 'formants': [480, 1100, 2300], 'gain': 0.88}, # lo
        {'dur': 0.35, 'f0_rel': 0.88, 'formants': [350, 2250, 2800], 'vibrato': 0.025, 'gain': 0.82} # ji
    ]
    return synthesize_utterance(syllables, base_f0=148.0, duration=2.5)

def gen_majhi_patrika():
    # "Waqt di aa-waaz! Akh-bar padh-o ji!" (Majhi newspaper hawker, ~165 Hz)
    syllables = [
        {'dur': 0.22, 'f0_rel': 1.08, 'formants': [580, 1200, 2400], 'gain': 0.92}, # Waqt
        {'dur': 0.18, 'f0_rel': 1.14, 'formants': [380, 2150, 2750], 'gain': 0.90}, # di
        {'dur': 0.10, 'pause': 0.04},
        {'dur': 0.26, 'f0_rel': 1.22, 'formants': [680, 1350, 2500], 'gain': 0.95}, # aa
        {'dur': 0.30, 'f0_rel': 1.08, 'formants': [620, 1200, 2400], 'gain': 0.92}, # waaz
        {'dur': 0.12, 'pause': 0.06},
        {'dur': 0.20, 'f0_rel': 1.10, 'formants': [650, 1300, 2450], 'gain': 0.90}, # Akh
        {'dur': 0.24, 'f0_rel': 1.16, 'formants': [680, 1350, 2500], 'gain': 0.92}, # bar
        {'dur': 0.22, 'f0_rel': 1.02, 'formants': [500, 1150, 2350], 'gain': 0.88}, # padh
        {'dur': 0.32, 'f0_rel': 0.88, 'formants': [460, 1080, 2300], 'vibrato': 0.022, 'gain': 0.82} # o
    ]
    return synthesize_utterance(syllables, base_f0=165.0, duration=2.4)

def gen_majhi_chana():
    # "Cha-na jor ga-ram ma-sa-le-daar!" (Majhi street-food vendor, ~156 Hz)
    syllables = [
        {'dur': 0.18, 'f0_rel': 1.04, 'formants': [620, 1250, 2400], 'gain': 0.88}, # Cha
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [660, 1320, 2480], 'gain': 0.92}, # na
        {'dur': 0.26, 'f0_rel': 1.18, 'formants': [480, 1100, 2320], 'gain': 0.94}, # jor
        {'dur': 0.20, 'f0_rel': 1.06, 'formants': [620, 1250, 2420], 'gain': 0.90}, # ga
        {'dur': 0.28, 'f0_rel': 1.14, 'formants': [660, 1300, 2460], 'gain': 0.92}, # ram
        {'dur': 0.10, 'pause': 0.05},
        {'dur': 0.16, 'f0_rel': 1.02, 'formants': [600, 1220, 2380], 'gain': 0.88}, # ma
        {'dur': 0.18, 'f0_rel': 1.10, 'formants': [650, 1300, 2450], 'gain': 0.90}, # sa
        {'dur': 0.22, 'f0_rel': 1.16, 'formants': [520, 1850, 2650], 'gain': 0.92}, # le
        {'dur': 0.36, 'f0_rel': 0.90, 'formants': [680, 1350, 2500], 'vibrato': 0.026, 'gain': 0.85} # daar
    ]
    return synthesize_utterance(syllables, base_f0=156.0, duration=2.4)

def gen_majhi_matron():
    # "Ve ba-chiyo dhyan naal khelo!" (Majhi elder matron from haveli, ~210 Hz)
    syllables = [
        {'dur': 0.25, 'f0_rel': 1.12, 'formants': [520, 1950, 2750], 'gain': 0.92}, # Ve
        {'dur': 0.18, 'f0_rel': 1.05, 'formants': [620, 1250, 2450], 'gain': 0.88}, # ba
        {'dur': 0.22, 'f0_rel': 1.18, 'formants': [400, 2200, 2800], 'gain': 0.92}, # chi
        {'dur': 0.26, 'f0_rel': 1.08, 'formants': [480, 1150, 2350], 'gain': 0.90}, # yo
        {'dur': 0.10, 'pause': 0.06},
        {'dur': 0.24, 'f0_rel': 1.14, 'formants': [650, 1300, 2450], 'gain': 0.92}, # dhyan
        {'dur': 0.20, 'f0_rel': 1.06, 'formants': [680, 1350, 2500], 'gain': 0.90}, # naal
        {'dur': 0.22, 'f0_rel': 1.12, 'formants': [520, 1850, 2650], 'gain': 0.90}, # khe
        {'dur': 0.35, 'f0_rel': 0.88, 'formants': [480, 1100, 2300], 'vibrato': 0.028, 'gain': 0.82} # lo
    ]
    return synthesize_utterance(syllables, base_f0=210.0, duration=2.3)

# ---------------------------------------------------------------------------
# Doabi Dialect Walla Utterances
# ---------------------------------------------------------------------------

def gen_doabi_kulfi():
    # "Than-di kul-fi pis-ta ba-dam! Aao bai khao!" (Doabi sweet vendor cry, ~140 Hz)
    syllables = [
        {'dur': 0.22, 'f0_rel': 1.08, 'formants': [640, 1280, 2420], 'gain': 0.90}, # Than
        {'dur': 0.20, 'f0_rel': 1.02, 'formants': [380, 2150, 2750], 'gain': 0.88}, # di
        {'dur': 0.24, 'f0_rel': 1.16, 'formants': [450, 1120, 2320], 'gain': 0.92}, # kul
        {'dur': 0.26, 'f0_rel': 1.10, 'formants': [380, 2200, 2780], 'gain': 0.90}, # fi
        {'dur': 0.10, 'pause': 0.06},
        {'dur': 0.18, 'f0_rel': 1.05, 'formants': [390, 2180, 2760], 'gain': 0.88}, # pis
        {'dur': 0.22, 'f0_rel': 1.12, 'formants': [650, 1300, 2450], 'gain': 0.92}, # ta
        {'dur': 0.20, 'f0_rel': 1.04, 'formants': [620, 1250, 2420], 'gain': 0.90}, # ba
        {'dur': 0.32, 'f0_rel': 0.92, 'formants': [660, 1320, 2480], 'vibrato': 0.024, 'gain': 0.88}, # dam
        {'dur': 0.12, 'pause': 0.08},
        {'dur': 0.24, 'f0_rel': 1.14, 'formants': [680, 1350, 2500], 'gain': 0.92}, # Aao
        {'dur': 0.22, 'f0_rel': 1.06, 'formants': [650, 1300, 2450], 'gain': 0.90}, # bai
        {'dur': 0.35, 'f0_rel': 0.88, 'formants': [680, 1350, 2500], 'vibrato': 0.026, 'gain': 0.82} # khao
    ]
    return synthesize_utterance(syllables, base_f0=140.0, duration=3.0)

def gen_doabi_kumhar():
    # "Pak-ke koo-je te su-ra-hiyan! Than-da paa-ni!" (Doabi potter, ~126 Hz)
    syllables = [
        {'dur': 0.18, 'f0_rel': 1.05, 'formants': [620, 1250, 2420], 'gain': 0.88}, # Pak
        {'dur': 0.22, 'f0_rel': 1.12, 'formants': [520, 1850, 2650], 'gain': 0.92}, # ke
        {'dur': 0.26, 'f0_rel': 1.18, 'formants': [450, 1100, 2300], 'gain': 0.92}, # koo
        {'dur': 0.22, 'f0_rel': 1.04, 'formants': [520, 1850, 2650], 'gain': 0.90}, # je
        {'dur': 0.10, 'pause': 0.05},
        {'dur': 0.18, 'f0_rel': 1.02, 'formants': [450, 1100, 2320], 'gain': 0.88}, # su
        {'dur': 0.24, 'f0_rel': 1.14, 'formants': [680, 1350, 2500], 'gain': 0.92}, # ra
        {'dur': 0.30, 'f0_rel': 0.96, 'formants': [650, 1300, 2450], 'gain': 0.88}, # hiyan
        {'dur': 0.12, 'pause': 0.06},
        {'dur': 0.22, 'f0_rel': 1.10, 'formants': [640, 1280, 2420], 'gain': 0.90}, # Than
        {'dur': 0.20, 'f0_rel': 1.02, 'formants': [620, 1250, 2400], 'gain': 0.88}, # da
        {'dur': 0.38, 'f0_rel': 0.88, 'formants': [680, 1350, 2500], 'vibrato': 0.024, 'gain': 0.82} # paani
    ]
    return synthesize_utterance(syllables, base_f0=126.0, duration=2.8)

def gen_doabi_arhtiya():
    # "Na-vi ka-nak da daa-na! Kha-ra wa-par!" (Doabi grain trader, ~118 Hz)
    syllables = [
        {'dur': 0.20, 'f0_rel': 1.04, 'formants': [620, 1250, 2400], 'gain': 0.88}, # Na
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [380, 2150, 2750], 'gain': 0.92}, # vi
        {'dur': 0.22, 'f0_rel': 1.06, 'formants': [650, 1300, 2450], 'gain': 0.90}, # ka
        {'dur': 0.28, 'f0_rel': 1.16, 'formants': [620, 1250, 2420], 'gain': 0.94}, # nak
        {'dur': 0.18, 'f0_rel': 1.02, 'formants': [650, 1300, 2450], 'gain': 0.88}, # da
        {'dur': 0.26, 'f0_rel': 1.14, 'formants': [680, 1350, 2500], 'gain': 0.92}, # daa
        {'dur': 0.28, 'f0_rel': 1.00, 'formants': [650, 1300, 2450], 'gain': 0.88}, # na
        {'dur': 0.10, 'pause': 0.06},
        {'dur': 0.22, 'f0_rel': 1.08, 'formants': [650, 1300, 2450], 'gain': 0.90}, # Kha
        {'dur': 0.24, 'f0_rel': 1.14, 'formants': [680, 1350, 2500], 'gain': 0.92}, # ra
        {'dur': 0.22, 'f0_rel': 1.02, 'formants': [620, 1250, 2400], 'gain': 0.88}, # wa
        {'dur': 0.35, 'f0_rel': 0.88, 'formants': [680, 1350, 2500], 'vibrato': 0.022, 'gain': 0.82} # par
    ]
    return synthesize_utterance(syllables, base_f0=118.0, duration=2.9)

def gen_doabi_mazdoor():
    # "Ba-cha ke ji ba-cha ke! Raah chad-do!" (Doabi porter laden with cargo, ~134 Hz)
    syllables = [
        {'dur': 0.18, 'f0_rel': 1.06, 'formants': [620, 1250, 2400], 'gain': 0.90}, # Ba
        {'dur': 0.22, 'f0_rel': 1.16, 'formants': [680, 1350, 2500], 'gain': 0.94}, # cha
        {'dur': 0.18, 'f0_rel': 1.04, 'formants': [520, 1850, 2650], 'gain': 0.88}, # ke
        {'dur': 0.22, 'f0_rel': 1.00, 'formants': [380, 2150, 2750], 'gain': 0.86}, # ji
        {'dur': 0.10, 'pause': 0.05},
        {'dur': 0.18, 'f0_rel': 1.08, 'formants': [620, 1250, 2400], 'gain': 0.90}, # ba
        {'dur': 0.22, 'f0_rel': 1.18, 'formants': [680, 1350, 2500], 'gain': 0.95}, # cha
        {'dur': 0.20, 'f0_rel': 1.02, 'formants': [520, 1850, 2650], 'gain': 0.88}, # ke!
        {'dur': 0.12, 'pause': 0.06},
        {'dur': 0.24, 'f0_rel': 1.12, 'formants': [680, 1350, 2500], 'gain': 0.92}, # Raah
        {'dur': 0.22, 'f0_rel': 1.08, 'formants': [620, 1250, 2400], 'gain': 0.90}, # chad
        {'dur': 0.35, 'f0_rel': 0.88, 'formants': [480, 1100, 2300], 'vibrato': 0.024, 'gain': 0.82} # do
    ]
    return synthesize_utterance(syllables, base_f0=134.0, duration=2.5)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(base_dir, "Art", "Audio", "Voice", "Walla")
    os.makedirs(out_dir, exist_ok=True)

    tracks = [
        ("SFX_Voice_Majhi_SabziWalla_Bark.wav", gen_majhi_sabzi()),
        ("SFX_Voice_Majhi_PatrikaHawker_Bark.wav", gen_majhi_patrika()),
        ("SFX_Voice_Majhi_ChanaVendor_Bark.wav", gen_majhi_chana()),
        ("SFX_Voice_Majhi_ElderMatron_Bark.wav", gen_majhi_matron()),
        ("SFX_Voice_Doabi_KulfiWalla_Bark.wav", gen_doabi_kulfi()),
        ("SFX_Voice_Doabi_KumharPotter_Bark.wav", gen_doabi_kumhar()),
        ("SFX_Voice_Doabi_MandiArhtiya_Bark.wav", gen_doabi_arhtiya()),
        ("SFX_Voice_Doabi_MazdoorPorter_Bark.wav", gen_doabi_mazdoor())
    ]

    for filename, samples in tracks:
        out_path = os.path.join(out_dir, filename)
        write_wav(out_path, samples)

    print(f"\n[SUCCESS] Synthesized all {len(tracks)} multi-dialect Punjabi voice tracks to: {out_dir}")

if __name__ == "__main__":
    main()
