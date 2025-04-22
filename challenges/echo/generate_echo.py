from PIL import Image
import numpy as np

flag = "FLAG{lsb_success}"
flag_bin = ''.join(format(ord(c), '08b') for c in flag)

img = Image.new("RGB", (100, 100), color="black")
pixels = np.array(img)

flat_pixels = pixels.reshape(-1, 3)

for i, bit in enumerate(flag_bin):
    blue = flat_pixels[i][2]
    blue = (blue & 0b11111110) | int(bit)  # Clear LSB and set it to the bit
    flat_pixels[i][2] = blue

pixels = flat_pixels.reshape((100, 100, 3))
encoded_img = Image.fromarray(pixels.astype('uint8'), 'RGB')
encoded_img.save("echo.png")
