import base64
from cryptography.fernet import Fernet
import os

# Step 1: Ensure the layers directory exists
os.makedirs("layers", exist_ok=True)

# Step 2: Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Step 3: Create the flag and encode it
flag = "CTF{Sukuna-is-goat}"
encoded_flag = base64.b64encode(flag.encode()).decode()

# Save the base64 encoded flag as the first layer (layer1.txt)
with open("layers/layer1.txt", "w") as f:
    f.write(encoded_flag)

# Step 4: Encrypt the base64 encoded flag for layer2 (layer2.png)
encrypted_flag = cipher_suite.encrypt(encoded_flag.encode())

# Save the encrypted flag as layer2.png (Simulate an image file)
with open("layers/layer2.png", "wb") as f:
    f.write(encrypted_flag)

# Step 5: Create a final encrypted layer (layer3.enc)
final_encrypted_layer = cipher_suite.encrypt(flag.encode())

# Save the final encrypted layer
with open("layers/layer3.enc", "wb") as f:
    f.write(final_encrypted_layer)

# Step 6: Save the decryption key in a separate file (encoded_flag.txt)
with open("layers/encoded_flag.txt", "w") as f:
    f.write(key.decode())

print("Challenge layers generated successfully!")
