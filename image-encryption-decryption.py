import os

from PIL import Image

from Crypto.Cipher import AES

from Crypto.Util.Padding import pad, unpad

from Crypto.Random import get_random_bytes



def generate_key():

    # Generate a strong random key

    return get_random_bytes(16)  # AES key size is 16 bytes (128 bits)



def encrypt_image(input_file, key):

    try:

        # Open and validate the input image

        with Image.open(input_file) as image:

            # Perform encryption using AES algorithm in CBC mode

            cipher = AES.new(key, AES.MODE_CBC)

            # Pad the image data before encryption

            padded_data = pad(image.tobytes(), AES.block_size)

            encrypted_data = cipher.iv + cipher.encrypt(padded_data)

        

        return encrypted_data, cipher

    except Exception as e:

        print("Error encrypting image:", str(e))

        return None, None



def decrypt_image(encrypted_data, key):

    try:

        # Perform decryption using AES algorithm in CBC mode

        iv = encrypted_data[:AES.block_size]

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)

        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)

        

        return decrypted_data

    except ValueError as ve:

        print("Error decrypting image:", str(ve))

        return None



def save_image(data, input_file):

    try:

        # Extract directory path and filename from input file

        directory, filename = os.path.split(input_file)

        

        # Remove "_encrypted" from filename to get output filename

        output_filename = os.path.splitext(filename)[0].replace("_encrypted", "_decrypted") + ".jpg"

        

        # Construct output file path

        output_file = os.path.join(directory, output_filename)

        

        # Convert decrypted data to image

        decrypted_image = Image.frombytes("RGB", (256, len(data) // 3), data)

        

        # Save the decrypted image

        decrypted_image.save(output_file)

        print("Decryption successful. Decrypted image saved to:", output_file)

    except Exception as e:

        print("Error saving decrypted image:", str(e))



def main():

    print("Welcome to Image Encryption and Decryption Tool")



    while True:

        action = input("Enter 'en' to encrypt or 'de' to decrypt (or 'exit' to quit): ").lower()



        if action == 'en':

            input_file = input("Enter the name of the image file to encrypt: ")

            output_file = os.path.splitext(input_file)[0] + "_encrypted.jpg"



            key = input("Enter the key (16 bytes) for encryption: ")

            key = key.encode() if isinstance(key, str) else key



            encrypted_data, _ = encrypt_image(input_file, key)

            if encrypted_data:

                with open(output_file, 'wb') as f:

                    f.write(encrypted_data)

                    print("Encryption successful. Encrypted image saved to:", output_file)



        elif action == 'de':

            input_file = input("Enter the name of the encrypted image file to decrypt: ")



            key = input("Enter the key (16 bytes) for decryption: ")

            key = key.encode() if isinstance(key, str) else key



            encrypted_data = None

            with open(input_file, 'rb') as f:

                encrypted_data = f.read()



            if encrypted_data:

                decrypted_data = decrypt_image(encrypted_data, key)

                if decrypted_data:

                    save_image(decrypted_data, input_file)



        elif action == 'exit':

            break



        else:

            print("Invalid input. Please enter 'en', 'de', or 'exit'.")



if __name__ == "__main__":

    main()

