# generate_waves.py
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.io.wavfile import write
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
STATIC_FLAG = os.getenv("WAVES_FLAG", "CTF{default_waves}")  # Fallback if not set

PROGRESS_FILE = "progress.txt"
FONT_SIZE = 40
IMG_SIZE = (800, 200)
DURATION = 5  # seconds
SAMPLE_RATE = 44100

# Dependency checks
try:
    import PIL
except ImportError:
    print("Please install Pillow: pip install Pillow")
    exit(1)
try:
    import numpy
except ImportError:
    print("Please install numpy: pip install numpy")
    exit(1)
try:
    from scipy.io.wavfile import write
except ImportError:
    print("Please install scipy: pip install scipy")
    exit(1)

def text_to_image(text):
    img = Image.new("L", IMG_SIZE, color=0)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", FONT_SIZE)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((IMG_SIZE[0]-w)/2, (IMG_SIZE[1]-h)/2), text, fill=255, font=font)
    return img

def image_to_wave(img):
    pixels = np.asarray(img) / 255.0
    flat = pixels.mean(axis=0)  # collapse rows -> get waveform-like structure
    waveform = np.interp(flat, (0, 1), (-1, 1))  # map 0-1 to -1 to 1
    signal = np.tile(waveform, int(SAMPLE_RATE * DURATION / len(waveform)))
    return np.int16(signal * 32767)

def update_progress():
    with open(PROGRESS_FILE, "a") as f:
        if "Waves challenge: Cleared" not in f.read():
            f.write("Waves challenge: Cleared\n")

def main():
    print("[?] Enter challenge name to generate :", end=" ")
    try:
        user_input = input().strip()
    except KeyboardInterrupt:
        print("\n[-] Interrupted by user.")
        return

    if user_input.lower() in ["waves", "sound", "truth"]:
        img = text_to_image(STATIC_FLAG)
        wave = image_to_wave(img)
        write("waves.wav", SAMPLE_RATE, wave)
        img.save("spectrogram_hint.png")  # Visual hint file
        update_progress()
        print("[✓] WAV file and image hint generated.")
        print("[+] Flag is correct!")
    else:
        print("[x] Invalid input. Try again.")
        print("[HINT] Analyze the spectrogram of waves.wav or the hint image to find the flag.")

if __name__ == "__main__":
    main()
