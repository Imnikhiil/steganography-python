from PIL import Image
import os

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def encode_image(img_path, secret_text, output_path):
    if not os.path.exists(img_path):
        print(f"❌ Error: '{img_path}' not found!")
        return

    img = Image.open(img_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    binary_secret = text_to_bin(secret_text + "###")
    data_index = 0
    pixels = list(img.getdata())
    new_pixels = []

    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(3):
            if data_index < len(binary_secret):
                new_pixel[i] = new_pixel[i] & ~1 | int(binary_secret[data_index])
                data_index += 1
        new_pixels.append(tuple(new_pixel))

    if data_index < len(binary_secret):
        print("❌ Error: Message is too long for the image.")
        return

    img.putdata(new_pixels)
    img.save(output_path)
    print(f"✅ Secret message successfully encoded in '{output_path}'.")

def decode_image(img_path):
    if not os.path.exists(img_path):
        print(f"❌ Error: '{img_path}' not found!")
        return

    img = Image.open(img_path)
    pixels = list(img.getdata())
    binary_data = ''

    for pixel in pixels:
        for i in range(3):
            binary_data += str(pixel[i] & 1)

    text = bin_to_text(binary_data)
    if "###" in text:
        return text.split("###")[0]
    else:
        return "❌ No hidden message found."

# ---- Change message and image names below
input_image = "input.png"
output_image = "output.png"
secret_message = "RC Explore Cybersecurity Internship Project!"

encode_image(input_image, secret_message, output_image)
decoded = decode_image(output_image)
print(f"🔓 Decoded message: {decoded}")
