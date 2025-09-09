import os
import sys
import time
import marshal
import subprocess
import shutil
from pathlib import Path

# --- Color Codes ---
black = "\033[1;90m"
white = "\033[1;97m"
red = "\033[1;91m"
green = "\033[1;92m"
yellow = "\033[1;93m"
blue = "\033[1;94m"
purple = "\033[1;95m"
cyan = "\033[1;96m"
rst = "\033[0m"

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def animetion(text):
    """Prints text with a character-by-character animation effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)

def display_header():
    """Defines and displays the main header and menu for the tool."""
    header_art = f"""
{purple}
    __  ___              _____              __
  /  |/  /__ _________/ ___/_____ _____  / /____ ____
 / /|_/ / _ `/ __/___/ /__/ __/ // / _ \/ __/ -_) __/
/_/  /_/\_,_/\__/     \___/_/  \_, / .__/\__/\__/_/
                             /___/_/                  {rst}
{green} Protect your code and copyright using this Tool
"""
    details = f"""{green} Author   : Macgaiver
 Github   : https://github.com/macgaiver11996
 Telegram : t.me/macgaiver_official{rst}
"""
    symbol = f"{green}\n***********************************************************{rst}"

    menu = f"""

{rst}
    {cyan}1- Encrypt Bash Script
    2- Decrypt Bash Script
    3- Encrypt Python Script (Marshal)
    4- About This Tool
    0- Exit{rst}
    """

    animetion(header_art)
    animetion(details)
    animetion(symbol)
    print(menu)

def show_about_info():
    """Displays detailed information about the tool."""
    about_text = f"""
    {green}Tool coded by: Macgaiver
    Github         : https://github.com/macgaiver11996
    Telegram       : https://t.me/macgaiver_official{rst}

    This script is written in Python. You can use it to
    encrypt and decrypt your bash scripts.
    Additionally, you can encrypt Python code using marshal.
    """
    print(about_text)

def obfuscate_bash_script():
    """Encrypts a bash script using the 'bash-obfuscate' tool."""
    # --- SECURE DEPENDENCY CHECK ---
    # Check if 'bash-obfuscate' is installed and available in the system's PATH.
    if not shutil.which("bash-obfuscate"):
        print(f"\n{red}Error: The 'bash-obfuscate' tool is not installed.{rst}")
        print(f"{yellow}This feature requires an external tool to work.{rst}")
        print("\nPlease install it by running these commands in your terminal:")
        print(f"  1. {cyan}git clone https://github.com/bash-obfuscator/bash-obfuscator.git{rst}")
        print(f"  2. {cyan}cd bash-obfuscator{rst}")
        print(f"  3. {cyan}sudo ./install.sh{rst}\n")
        return # Exit the function safely without trying to run the command.

    try:
        source_file_str = input("Enter the input filename: ")
        if not source_file_str:
            print(f"{red}Error: No input file provided.{rst}")
            return

        source_file = Path(source_file_str)
        if not source_file.is_file():
            print(f"{red}Error: File '{source_file}' not found.{rst}")
            return

        destination_file_str = input("Enter the output filename (leave blank for default): ")
        if not destination_file_str:
            destination_file = source_file.with_name(f"{source_file.stem}_encrypted.sh")
        else:
            destination_file = Path(destination_file_str)

        process = subprocess.run(
            ["bash-obfuscate", str(source_file), "-o", str(destination_file)],
            capture_output=True, text=True
        )

        if process.returncode != 0:
            print(f"{red}Error during obfuscation:{rst}")
            print(process.stderr)
            return

        print(f"{green}Success: '{source_file}' was encrypted and saved as '{destination_file}'.{rst}")

    except Exception as e:
        print(f"{red}An unexpected error occurred: {e}{rst}")

def deobfuscate_bash_script():
    """Attempts to decrypt a script obfuscated by this tool."""
    try:
        source_file_str = input("Enter the encrypted filename: ")
        if not source_file_str:
            print(f"{red}Error: No input file provided.{rst}")
            return
            
        source_file = Path(source_file_str)
        if not source_file.is_file():
            print(f"{red}Error: File not found.{rst}")
            return

        content = source_file.read_text()
        if "eval" not in content:
            print(f"{red}Error: This file does not appear to be a decryptable script.{rst}")
            return

        modified_content = content.replace("eval", "echo", 1)

        process = subprocess.run(
            ["bash", "-c", modified_content],
            capture_output=True, text=True, check=True
        )
        decrypted_content = process.stdout

        destination_file_str = input("Enter the output filename (leave blank for default): ")
        if not destination_file_str:
             destination_file = source_file.with_name(f"{source_file.stem}_decrypted.sh")
        else:
            destination_file = Path(destination_file_str)
            
        header_comment = f"# Decrypted by Macgaiver\n\n"
        destination_file.write_text(header_comment + decrypted_content)

        print(f"{green}Success: '{source_file}' was decrypted and saved as '{destination_file}'.{rst}")

    except subprocess.CalledProcessError as e:
        print(f"{red}Error running script to decrypt: {e}{rst}")
    except Exception as e:
        print(f"{red}An unexpected error occurred: {e}{rst}")

def compile_python_script():
    """Encrypts a Python script using marshal."""
    try:
        file_path_str = input("Enter the Python filename (.py): ")
        if not file_path_str:
            print(f"{red}Error: No input file provided.{rst}")
            return

        source_file = Path(file_path_str)
        if not source_file.is_file():
            print(f"{red}Error: File '{source_file}' not found.{rst}")
            return

        source_code = source_file.read_text()

        try:
            compiled_code = compile(source_code, source_file.name, 'exec')
            marshalled_data = marshal.dumps(compiled_code)
        except (TypeError, ValueError) as e:
            print(f"{red}Error compiling the Python script: {e}{rst}")
            print(f"{yellow}The file may be invalid or already encrypted.{rst}")
            return

        output_filename = source_file.with_name(f"{source_file.stem}_encrypted.py")

        output_content = (
            f"# Encrypted by Macgaiver\n"
            "import marshal\n\n"
            f"exec(marshal.loads({repr(marshalled_data)}))\n"
        )

        output_filename.write_text(output_content)
        print(f"{green}Success: The new encrypted file is named '{output_filename}'{rst}")

    except KeyboardInterrupt:
        print("\nProcess cancelled by user.")
    except Exception as e:
        print(f"{red}An unexpected error occurred: {e}{rst}")

def main_loop():
    """The main function loop for the program."""
    actions = {
        '1': obfuscate_bash_script,
        '2': deobfuscate_bash_script,
        '3': compile_python_script,
        '4': show_about_info,
    }

    while True:
        clear_screen()
        display_header()
        choice = input(f"Select an option: ")

        if choice == '0':
            print(f"{green}Thank you for using this tool!{rst}")
            time.sleep(1)
            break

        action = actions.get(choice)

        if action:
            action()
        else:
            print(f"{red}Invalid input. Please try again.{rst}")

        print(f"\nPress Enter to return to the menu...")
        input()

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print(f"\n{yellow}Program terminated by user.{rst}")
        sys.exit(0)
