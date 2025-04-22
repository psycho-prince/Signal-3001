# generate_layers.py
import base64
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STATIC_FLAG = os.getenv("LAYERS_FLAG", "CTF{default_layers}")  # Fallback if not set

# Constants
LAYER_DIR = "layers"
ENCODED_FLAG_FILE = f"{LAYER_DIR}/encoded_flag.txt"
LAYER1_FILE = f"{LAYER_DIR}/layer1.txt"
LAYER2_FILE = f"{LAYER_DIR}/layer2.png"
LAYER3_FILE = f"{LAYER_DIR}/layer3.enc"
PROGRESS_FILE = "progress.txt"

# Dependency check
try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Please install cryptography: pip install cryptography")
    exit(1)

def generate_layers():
    # Ensure layers directory exists
    os.makedirs(LAYER_DIR, exist_ok=True)

    # Generate encryption key and cipher suite
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # Step 1: Base64 encode the flag and save to layer1.txt
    encoded_flag = base64.b64encode(STATIC_FLAG.encode()).decode()
    with open(LAYER1_FILE, "w") as f:
        f.write(encoded_flag)

    # Step 2: Encrypt the base64 encoded flag and save to layer2.png
    encrypted_flag = cipher_suite.encrypt(encoded_flag.encode())
    with open(LAYER2_FILE, "wb") as f:
        f.write(encrypted_flag)

    # Step 3: Encrypt the flag itself and save to layer3.enc
    final_encrypted_layer = cipher_suite.encrypt(STATIC_FLAG.encode())
    with open(LAYER3_FILE, "wb") as f:
        f.write(final_encrypted_layer)

    # Step 4: Save the decryption key in a separate file
    with open(ENCODED_FLAG_FILE, "w") as f:
        f.write(key.decode())

    print("Challenge layers generated successfully!")

def update_progress():
    with open(PROGRESS_FILE, "a") as f:
        if "Layers challenge: Cleared" not in f.read():
            f.write("Layers challenge: Cleared\n")

def run():
    print("[+] Generating challenge layers...")
    generate_layers()
    try:
        user_input = input("[?] Enter the flag you found: ").strip()
        if user_input == STATIC_FLAG:
            print("[✓] Flag is correct!")
            update_progress()
        else:
            print("[✗] Incorrect flag. Try again.")
            print("[HINT] Decrypt layer3.enc using the key from encoded_flag.txt, then reverse the base64 encoding.")
    except KeyboardInterrupt:
        print("\n[-] Interrupted by user.")
        return

if __name__ == "__main__":
    run()
