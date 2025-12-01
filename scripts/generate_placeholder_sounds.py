import os
import wave
import math
import struct
import random

def generate_tone(filename, frequency=440, duration=0.5, volume=0.5, type='sine'):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = i / sample_rate
            if type == 'sine':
                value = math.sin(2 * math.pi * frequency * t)
            elif type == 'square':
                value = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            elif type == 'sawtooth':
                value = 2.0 * (t * frequency - math.floor(t * frequency + 0.5))
            elif type == 'noise':
                value = random.uniform(-1, 1)
            else:
                value = 0
            
            # Apply envelope (fade out)
            envelope = 1.0 - (i / n_samples)
            
            data = int(value * volume * envelope * 32767.0)
            wav_file.writeframes(struct.pack('<h', data))

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

BASE_DIR = "d:/EvalForge/apps/web/public/sounds"
ensure_dir(BASE_DIR)

# Cyberdeck Sounds (Mechanical/Retro)
generate_tone(f"{BASE_DIR}/click.mp3", 1000, 0.1, 0.5, 'square')
generate_tone(f"{BASE_DIR}/hover.mp3", 800, 0.05, 0.3, 'sine')
generate_tone(f"{BASE_DIR}/typewriter.mp3", 1200, 0.05, 0.4, 'noise')
generate_tone(f"{BASE_DIR}/success.mp3", 600, 0.5, 0.6, 'sine') # Arpeggio ideally
generate_tone(f"{BASE_DIR}/boss_alarm.mp3", 400, 1.0, 0.8, 'sawtooth')
generate_tone(f"{BASE_DIR}/access_denied.mp3", 150, 0.5, 0.8, 'sawtooth')

# Navigator Sounds (Sci-Fi/Soft)
generate_tone(f"{BASE_DIR}/nav_beep.mp3", 2000, 0.1, 0.4, 'sine')
generate_tone(f"{BASE_DIR}/nav_hum.mp3", 200, 0.2, 0.2, 'sine')
generate_tone(f"{BASE_DIR}/nav_chime.mp3", 1500, 0.6, 0.5, 'sine')
generate_tone(f"{BASE_DIR}/nav_alert.mp3", 800, 0.8, 0.7, 'sine')

# Workshop Sounds (Industrial/Tactile)
generate_tone(f"{BASE_DIR}/work_tock.mp3", 600, 0.05, 0.6, 'square') # Like a metronome
generate_tone(f"{BASE_DIR}/work_hover.mp3", 100, 0.05, 0.2, 'sawtooth') # Low buzz
generate_tone(f"{BASE_DIR}/work_bell.mp3", 880, 1.0, 0.5, 'sine')
generate_tone(f"{BASE_DIR}/work_whistle.mp3", 1200, 0.8, 0.6, 'sawtooth')

print(f"Generated placeholder sounds in {BASE_DIR}")
