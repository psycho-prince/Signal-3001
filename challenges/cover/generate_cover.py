from PIL import Image
import numpy as np

# Set the flag that you want to encode
FLAG = "FLAG{hidden_data}"

# Function to encode the flag in the image
def encode_flag_in_image(image_path, flag):
    img = Image.open(image_path)
    img = img.convert("RGB")  # Make sure the image is in RGB format
    pixels = np.array(img)
    
    # Flatten the pixel array
    flat_pixels = pixels.flatten()

    # Convert the flag into a binary string
    binary_flag = ''.join(format(ord(c), '08b') for c in flag)
    
    # Ensure the flag is long enough to encode
    if len(binary_flag) > len(flat_pixels):
        raise ValueError("Flag is too long to encode in this image.")

    # Loop through the binary flag and modify the LSB of each pixel
    for i, bit in enumerate(binary_flag):
        # Get the current pixel value (range 0-255)
        pixel_value = flat_pixels[i]

        # Debugging: Print the pixel values before modifying them
        if pixel_value < 0 or pixel_value > 255:
            print(f"Invalid pixel value before modification: {pixel_value}")
        
        # Ensure the pixel value is within valid bounds (0-255)
        pixel_value = max(0, min(255, pixel_value))

        # Set the LSB (Least Significant Bit) of the pixel value
        new_pixel_value = (pixel_value & ~1) | int(bit)

        # Debugging: Print the new pixel value
        if new_pixel_value < 0 or new_pixel_value > 255:
            print(f"New pixel value out of bounds: {new_pixel_value}")
        
        # Ensure new_pixel_value stays within the uint8 bounds
        flat_pixels[i] = max(0, min(255, new_pixel_value))
    
    # Reshape the flat pixels back to the original image shape
    new_pixels = flat_pixels.reshape(pixels.shape)

    # Save the new image with the flag encoded
    new_image = Image.fromarray(new_pixels.astype(np.uint8))
    new_image.save("encoded_cover_image.png")
    print("Flag encoded successfully into the image!")

# Call the function to encode the flag
encode_flag_in_image("cover_image.png", FLAG)
