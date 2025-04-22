# generate_echo.py
from PIL import Image
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
STATIC_FLAG = os.getenv("ECHO_FLAG", "CTF{default_echo}")  # Fallback if not set

IMAGE_NAME = "echo.png"
PROGRESS_FILE = "progress.txt"

# Dependency check
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

def encode_static_flag():
    flag_bin = ''.join(format(ord(c), '08b') for c in STATIC_FLAG)

    img = Image.new("RGB", (100, 100), color="black")
    pixels = np.array(img)
    flat_pixels = pixels.reshape(-1, 3)

    if len(flag_bin) > len(flat_pixels) * 3:  # Ensure flag fits in pixels
        raise ValueError("Flag too long for this image.")

    for i, bit in enumerate(flag_bin):
        if i >= len(flat_pixels) * 3:
            break
        pixel_idx = i // 3
        channel_idx = i % 3
        current_pixel = flat_pixels[pixel_idx][channel_idx]
        new_pixel = (current_pixel & 0b11111110) | int(bit)  # LSB encode
        flat_pixels[pixel_idx][channel_idx] = new_pixel

    pixels = flat_pixels.reshape((100, 100, 3))
    encoded_img = Image.fromarray(pixels.astype('uint8'), 'RGB')
    encoded_img.save(IMAGE_NAME)
    print(f"[+] Static flag encoded into {IMAGE_NAME}")

def validate_flag(user_input):
    return user_input.strip() == STATIC_FLAG

def update_progress():
    with open(PROGRESS_FILE, "a") as f:
        if "Echo challenge: Cleared" not in f.read():
            f.write("Echo challenge: Cleared\n")

def run():
    encode_static_flag()
    try:
        user_flag = input("[?] Enter the flag you found: ").strip()
    except KeyboardInterrupt:
        print("\n[-] Interrupted by user.")
        return

    if validate_flag(user_flag):
        print("[✓] Flag is correct!")
        update_progress()
    else:
        print("[✗] Incorrect flag. Try again.")
        print("[HINT] Check the LSB of the blue channel in the first pixels of echo.png.")

# Optional CLI execution
if __name__ == "__main__":
    run()
