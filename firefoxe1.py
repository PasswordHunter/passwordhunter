import browser_cookie3
import os
import sqlite3
from datetime import  datetime

class FirefoxBrowser:
    def __init__(self):
        pass
    
    def firefox_date_and_time(self,timestamp):
        timestamp_s = timestamp / 1000000
        try:
            date_obj = datetime.fromtimestamp(timestamp_s)
        except TypeError:
            raise ValueError('Invalid Firefox timestamp')
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
            
        
    def get_path(self, file):
        try:
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
        except Exception as e:
            print(e)

    def firefox_history(self):
        history=""
        try:
            history_path = self.get_path("places.sqlite")
            if history_path:
                conn = sqlite3.connect(history_path)
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
                conn.close()
                return "*"*60+"\tFirefox history data\t"+"*"*60+"\n"+ history
        except Exception as e:
            print(e)

    def firefox_cookies(self):
        cookies_data = ""
        cookies = list(browser_cookie3.firefox())
        for cookie in cookies:
            data_cookies = f"Cookies Name: {cookie.name} \n"
            data_cookies += f"Cookies domain : {cookie.domain} \n"
            data_cookies += f"Cookies Values : {cookie.value} \n"
            data_cookies += f"Cookies expires : {cookie.expires} \n\n"
            cookies_data += data_cookies
        return "*"*60+"\t Firefox Cookies data\t "+"*"*60+"\n"+ cookies_data


# firfoxe = FirefoxBrowser()

# file = firfoxe.firefox_history()

# print(file)
# print(firfoxe.firefox_date_and_time(1680259862819000))
