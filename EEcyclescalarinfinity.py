def patch_eboot(overclock_value):
    file_name = "eboot.bin"
    search_pattern = b'\x00\x00\x94\x11\x00\x01\x00\x00'

    try:
        # Convert the overclock value to a hexadecimal byte
        overclock_hex = int(overclock_value)
        overclock_byte = overclock_hex.to_bytes(1, 'big')

        # Read the file content
        with open(file_name, 'rb') as file:
            file_content = file.read()

        # Search for the pattern in the file content
        occurrences = [i for i in range(len(file_content)) if file_content.startswith(search_pattern, i)]

        if len(occurrences) != 1:
            print("EE clock speed not found! File either corrupt, altered, or unsupported.")
            return False

        # Replace the specific part of the pattern
        patched_content = bytearray(file_content)
        patched_content[occurrences[0] + 5] = overclock_byte[0]  # Correct index to replace '01' part

        # Write the modified content back to the file
        with open(file_name, 'wb') as file:
            file.write(patched_content)

        print("File successfully patched!")
        return True

    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    # Ask the user for the overclock value only once
    overclock_value = input("Overclock the EE by what value? (0-255): ").strip()

    # Check if the input is a valid byte value
    if not overclock_value.isdigit() or not (0 <= int(overclock_value) <= 255):
        print("Invalid input! Please enter a number between 0 and 255.")
        return

    # Continue running the script, but never ask for input again
    while True:
        success = patch_eboot(overclock_value)
        if success:
            print("You can now close the script or leave it running.")
        else:
            print("There was an issue with patching the file. Please check the error message above.")
        break  # After processing, break the loop

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript terminated by user.")