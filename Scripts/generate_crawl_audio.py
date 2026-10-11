"""
PROJECT REVOLUTION — HISTORICAL HAVELI DRAIN CRAWLWAY AUDIO SYNTHESIZER
Synthesizes period-authentic acoustic Foley for Kot Gurdarshan haveli drain crawlways (mori / parnala):
1. SFX_Crawl_Brick_Scrape.wav - Gritty shuffling of palms, knees, and coarse khadi cotton cloth dragging across baked Lahori brickwork with dislodged mortar grit.
2. SFX_Drain_Emerge_Gasp.wav   - Quiet exertion breath of 12-year-old scout Kabir planting hands on courtyard flagstones and emerging from the low conduit.

Output: 16-bit 44.1kHz mono PCM WAV files in Art/Audio/
"""

import math
import os
import random
import struct
import wave

SAMPLE_RATE = 44100
OUT_DIR = "C:/Users/npal7/PROJECT/REVOLUTION/Art/Audio"

def write_wav(filename, samples):
    os.makedirs(OUT_DIR, exist_ok=True)
    filepath = os.path.join(OUT_DIR, filename)
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        
        raw_bytes = bytearray()
        for s in samples:
            s_clamped = max(-1.0, min(1.0, s))
            val = int(s_clamped * 32767.0)
            raw_bytes.extend(struct.pack("<h", val))
            
        wav_file.writeframes(raw_bytes)
    print(f"Generated {filename}: {len(samples)/SAMPLE_RATE:.2f}s ({len(raw_bytes)} bytes)")

def generate_crawl_brick_scrape():
    """Rhythmic, gritty scraping of knees and palms on rough brick inside narrow haveli conduit."""
    duration = 1.60
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    random.seed(404)
    
    # 4 crawl shuffle strokes at t = 0.05, 0.42, 0.82, 1.20
    strokes = [0.05, 0.42, 0.82, 1.20]
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        val = 0.0
        
        for st in strokes:
            if t >= st:
                dt = t - st
                if dt < 0.28:
                    env = math.sin((dt / 0.28) * math.pi) ** 1.3
                    
                    # Brick friction scrape (band-filtered friction noise around 600-1400Hz)
                    scrape_noise = (random.random() * 2.0 - 1.0) * 0.45
                    # Low knee contact thump on brick (110-180Hz)
                    knee_thump = math.sin(2.0 * math.pi * 140.0 * dt) * 0.35 * math.exp(-dt * 22.0)
                    # Cloth sliding across rough masonry surface
                    cloth_slide = math.sin(2.0 * math.pi * 750.0 * dt) * 0.15 * math.sin(dt * 30.0)
                    
                    val += (scrape_noise + knee_thump + cloth_slide) * env
                    
        # Low conduit acoustic resonance (hollow enclosed drain feeling around 160Hz)
        conduit_resonance = math.sin(2.0 * math.pi * 160.0 * t) * 0.04 * math.exp(-t * 1.5)
        
        # Dislodged mortar sand grit particles
        grit = (random.random() * 2.0 - 1.0) * 0.06 * (0.5 + 0.5 * math.sin(t * 12.0))
        
        total = (val * 0.85 + conduit_resonance + grit) * 0.95
        samples[i] = max(-1.0, min(1.0, total))
        
    return samples

def generate_drain_emerge_gasp():
    """Subtle child exertion breath and firm hand plant on courtyard paving stones."""
    duration = 0.85
    total_samples = int(duration * SAMPLE_RATE)
    samples = [0.0] * total_samples
    
    random.seed(707)
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        
        # Hand plant impact at t = 0.08s
        hand_plant = 0.0
        if t >= 0.08:
            dt = t - 0.08
            decay = math.exp(-dt * 45.0)
            stone_thud = math.sin(2.0 * math.pi * 210.0 * dt) * 0.35 * decay
            palm_slap = (random.random() * 2.0 - 1.0) * 0.25 * math.exp(-dt * 90.0)
            hand_plant = stone_thud + palm_slap
            
        # Subtle breath intake/gasp from 0.12s to 0.65s
        breath = 0.0
        if 0.12 <= t <= 0.65:
            bt = t - 0.12
            env_breath = math.sin((bt / 0.53) * math.pi) ** 2.0
            # Filtered whisper noise for air intake
            noise = (random.random() * 2.0 - 1.0) * 0.18
            vocal_formant = math.sin(2.0 * math.pi * 420.0 * bt) * 0.08
            breath = (noise + vocal_formant) * env_breath
            
        # Cloth settling rustle
        cloth = 0.0
        if t >= 0.35:
            ct = t - 0.35
            cloth = (random.random() * 2.0 - 1.0) * 0.12 * math.exp(-ct * 12.0)
            
        samples[i] = max(-1.0, min(1.0, (hand_plant * 0.7 + breath * 0.85 + cloth * 0.5)))
        
    return samples

def main():
    print("Synthesizing Haveli Drain Crawlway Foley for Project REVOLUTION...")
    write_wav("SFX_Crawl_Brick_Scrape.wav", generate_crawl_brick_scrape())
    write_wav("SFX_Drain_Emerge_Gasp.wav", generate_drain_emerge_gasp())
    print("All drain crawlway audio assets generated successfully!")

if __name__ == "__main__":
    main()
