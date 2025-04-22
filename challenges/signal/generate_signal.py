# generate_signal.py
import base64
from cryptography.fernet import Fernet
import random
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
STATIC_FLAG = os.getenv("SIGNAL_FLAG", "HTB{default_signal}")  # Fallback if not set

PROGRESS_FILE = "progress.txt"

# Dependency check
try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Please install cryptography: pip install cryptography")
    exit(1)

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

def base64_encode(data):
    return base64.b64encode(data.encode()).decode()

def reverse_string(s):
    return s[::-1]

def update_progress():
    with open(PROGRESS_FILE, "a") as f:
        if "Signal challenge: Cleared" not in f.read():
            f.write("Signal challenge: Cleared\n")

def create_challenge():
    key = generate_key()
    encrypted_flag = encrypt_message(STATIC_FLAG, key)
    base64_flag = base64_encode(encrypted_flag)
    scrambled_flag = reverse_string(base64_flag)

    with open("signal.txt", "w") as f:
        f.write(scrambled_flag)

    with open("clue.txt", "w") as f:
        f.write(f"Decrypt the signal.\nKey (base64): {key.decode()}")

    update_progress()
    print("Signal challenge generated successfully!")

def run():
    print("[+] Generating signal challenge...")
    create_challenge()
    try:
        user_input = input("[?] Enter the flag you found: ").strip()
        if user_input == STATIC_FLAG:
            print("[✓] Flag is correct!")
            update_progress()  # Ensure progress is updated on correct input
        else:
            print("[✗] Incorrect flag. Try again.")
            print("[HINT] Reverse the string in signal.txt, decode base64, decrypt with the key from clue.txt using Fernet.")
    except KeyboardInterrupt:
        print("\n[-] Interrupted by user.")
        return

if __name__ == "__main__":
    run()
