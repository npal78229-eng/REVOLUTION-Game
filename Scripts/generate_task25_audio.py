"""
PROJECT REVOLUTION — Task 25 Audio Synthesis: Historical Narrative Epilogue
Synthesizes SFX_Epilogue_BaisakhiDawn.wav:
A reverent, warm morning tanpura drone, acoustic bansuri harmonic flute overtones,
and distant morning brass bell chime celebrating the dawn of April 14, 1919.
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

def synthesize_epilogue_dawn(duration=4.0):
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    # 1. Base Tanpura Drone in D (73.4 Hz + 146.8 Hz + 220.2 Hz)
    f0 = 73.416 # D2
    f_fifth = 110.0 # A2
    f_octave = 146.832 # D3
    
    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)
        # Envelope: Gentle swell in 0.8s, sustained warmly, gentle tail fade
        env = min(1.0, t / 0.8) * max(0.0, min(1.0, (duration - t) / 1.0))
        
        # Tanpura shimmer (slow beat frequency ~1.5 Hz)
        shimmer = 1.0 + 0.15 * math.sin(2.0 * math.pi * 1.5 * t)
        drone = (
            0.35 * math.sin(2.0 * math.pi * f0 * t) +
            0.25 * math.sin(2.0 * math.pi * f_fifth * t) +
            0.20 * math.sin(2.0 * math.pi * f_octave * t) +
            0.10 * math.sin(2.0 * math.pi * (f_octave * 1.5) * t)
        ) * shimmer
        
        # 2. Bansuri morning flute melody in Raag Bhairav / Bilawal
        # Notes: D4 (293.66), E4 (329.63), F#4 (369.99), A4 (440.0)
        flute_t = t - 0.5
        flute = 0.0
        if flute_t > 0:
            flute_env = min(1.0, flute_t / 0.6) * max(0.0, min(1.0, (duration - t) / 0.8))
            # Pentatonic melody progression
            if flute_t < 1.0:
                pitch = 293.66 # D4
            elif flute_t < 2.0:
                pitch = 369.99 # F#4
            elif flute_t < 3.0:
                pitch = 440.00 # A4
            else:
                pitch = 587.33 # D5 octave resolution
                
            vib = 1.0 + 0.015 * math.sin(2.0 * math.pi * 5.2 * t)
            harmonics = (
                0.35 * math.sin(2.0 * math.pi * pitch * vib * t) +
                0.15 * math.sin(2.0 * math.pi * (pitch * 2.0) * vib * t) +
                0.06 * math.sin(2.0 * math.pi * (pitch * 3.0) * vib * t)
            )
            # Breath noise
            noise = 0.02 * math.sin(2.0 * math.pi * 1840.0 * t) * math.cos(2.0 * math.pi * 420.0 * t)
            flute = (harmonics + noise) * flute_env
            
        # 3. Distant morning temple bell (struck at t=1.2s and t=2.5s)
        bell = 0.0
        for bell_strike in [1.2, 2.5]:
            dt = t - bell_strike
            if dt > 0:
                bell_decay = math.exp(-dt * 3.5)
                bell += 0.20 * (
                    0.6 * math.sin(2.0 * math.pi * 880.0 * dt) +
                    0.3 * math.sin(2.0 * math.pi * 1760.0 * dt) +
                    0.1 * math.sin(2.0 * math.pi * 2640.0 * dt)
                ) * bell_decay
                
        samples[i] = (drone + flute + bell) * env
        
    return samples

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(base_dir, "Art", "Audio")
    
    samples = synthesize_epilogue_dawn(4.2)
    wav_path = os.path.join(out_dir, "SFX_Epilogue_BaisakhiDawn.wav")
    write_wav(wav_path, samples)
    print("[TASK 25 AUDIO] Epilogue audio generation completed successfully.")

if __name__ == "__main__":
    main()
