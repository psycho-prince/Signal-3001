import base64
from cryptography.fernet import Fernet
import random

FLAG = "HTB{t3ch5p34k_1n_5igN4l5}"

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

def base64_encode(data):
    return base64.b64encode(data.encode()).decode()

def reverse_string(s):
    return s[::-1]

def create_challenge():
    key = generate_key()
    encrypted_flag = encrypt_message(FLAG, key)
    base64_flag = base64_encode(encrypted_flag)
    scrambled_flag = reverse_string(base64_flag)

    with open("signal.txt", "w") as f:
        f.write(scrambled_flag)

    with open("clue.txt", "w") as f:
        f.write(f"Decrypt the signal.\nKey (base64): {key.decode()}")

    print("Signal challenge generated successfully!")

if __name__ == "__main__":
    create_challenge()
