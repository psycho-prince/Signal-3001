import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.io.wavfile import write

TEXT = "FLAG{sound_waves_reveal_truth}"
FONT_SIZE = 40
IMG_SIZE = (800, 200)
DURATION = 5  # seconds
SAMPLE_RATE = 44100

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

img = text_to_image(TEXT)
wave = image_to_wave(img)
write("waves.wav", SAMPLE_RATE, wave)
img.save("spectrogram_hint.png")  # Optional: Visual hint file

print("✅ WAV file and image hint generated.")
