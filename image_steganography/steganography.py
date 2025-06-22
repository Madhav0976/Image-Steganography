from PIL import Image

# Function to convert text to binary
def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary + '1111111011111110'  # End flag

# Function to convert binary to text
def binary_to_text(binary):
    end_flag = '1111111011111110'
    end_index = binary.find(end_flag)
    if end_index != -1:
        binary = binary[:end_index]
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''.join([chr(int(char, 2)) for char in chars])
    return message

# Function to encode a message in an image
def encode_image(input_image, output_image, secret_message):
    image = Image.open(input_image).convert("RGB")
    binary_message = text_to_binary(secret_message)
    data = list(image.getdata())
    encoded_pixels = []

    binary_index = 0
    for pixel in data:
        r, g, b = pixel
        if binary_index < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_index])
            binary_index += 1
        encoded_pixels.append((r, g, b))

    image.putdata(encoded_pixels)
    image.save(output_image)
    print(f"✅ Secret message encoded and saved as {output_image}")

# Function to decode message from image
def decode_image(stego_image):
    image = Image.open(stego_image).convert("RGB")
    data = list(image.getdata())
    binary_data = ""

    for pixel in data:
        for value in pixel:
            binary_data += str(value & 1)

    message = binary_to_text(binary_data)
    print("📥 Hidden Message Decoded:")
    print("🔓", message)


# -------------------------
# Example Usage
# -------------------------
if __name__ == "__main__":
    choice = input("Choose operation: 1. Encode  2. Decode\nEnter 1 or 2: ")

    if choice == '1':
        input_image = input("Enter path of input image (e.g. input.png): ")
        output_image = input("Enter name for output image (e.g. stego.png): ")
        message = input("Enter the secret message to hide: ")
        encode_image(input_image, output_image, message)

    elif choice == '2':
        stego_image = input("Enter path of stego image: ")
        decode_image(stego_image)

    else:
        print("❌ Invalid option.")
