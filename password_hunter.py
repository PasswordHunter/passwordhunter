import tkinter as tk
from tkinter import messagebox
from edge import edge_browser
import chrome1
import firefox
from firefoxe1 import FirefoxBrowser
from brave import Brave
from windpass import WindowWifiPass
import subprocess

winpass = WindowWifiPass()
# firefox data
firefox1 = FirefoxBrowser()
# brave data
brave = Brave()
# chrome info variables
chrome = chrome1.Chrome()
password_data = chrome.passwords()
cookies = chrome.cookies()
search_terms, web_history = chrome.history()
autofill_data, credit_card_info = chrome.web_data()

# class LoginPage(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.master.title("Login Page")
#         # Create login label and entry fields
#         tk.Label(self, text="Username: ").grid(row=0, column=0, padx=10, pady=10)
#         self.username_entry = tk.Entry(self)
#         self.username_entry.grid(row=0, column=1, padx=10, pady=10)
#         tk.Label(self, text="Password: ").grid(row=1, column=0, padx=10, pady=10)
#         self.password_entry = tk.Entry(self, show="*")
#         self.password_entry.grid(row=1, column=1, padx=10, pady=10)

#         # Create login and quit buttons
#         tk.Button(self, text="Login", command=self.login).grid(row=5, column=0, padx=10, pady=10)
#         tk.Button(self, text="Quit", command=self.quit).grid(row=5, column=1, padx=10, pady=10)

#         self.pack()

#     def login(self):
#         username = self.username_entry.get()
#         password = self.password_entry.get()

#         # Check if username and password are valid
#         if username == "admin" and password == "password":

#             self.master.destroy()
#             root = tk.Tk()
#             menu = Main(root)
#             center_window(root, 800, 450)
#             root.mainloop()

#         else:
#             messagebox.showerror("Error", "Invalid username or password.")
#     def quit(self):
#         self.master.destroy()

# main pages


class Main:
    def __init__(self, master):
        self.master = master
        master.title("Password Hunter")
        master.iconbitmap("icon.ico")

        # create label widget
        self.label = tk.Label(master, text="Password Hunter", font=("Helvetica", 14,"bold"))
        self.label.pack()

        # create listbox widget
        self.listbox = tk.Listbox(master, font=("Helvetica", 12,"bold"), height=15, selectbackground="grey")
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listbox.delete(0, tk.END)
        with open("description.txt","r") as f:
            descrition = f.read()
            self.listbox.insert(tk.END, *descrition.split("\n"))

        self.password_label = tk.Label(root, font=("Helvetica", 12,"bold"),fg="white", text="")
        self.password_label.pack_forget()

        
        
        self.button = tk.Button(root, text="Scan for Network Profiles",
                                command=self.scan_wifi_profiles, justify='left', bg='red',font=("Helvetica", 12, "bold"),fg="white")
        self.button.pack_forget()
        
        self.button2 = tk.Button(
            root, text="Show Password",justify='left', bg='green',font=("Helvetica", 12, "bold"),fg="white", command=self.profile_show_password)
        self.button2.pack_forget()
        #button for password 
        self.password_button = tk.Button(root, text="Show Password",font=("Helvetica", 12, "bold"),bg="green",fg="white", command=self.show_password)
        self.password_button.pack_forget()
        self.hide_password_button = tk.Button(root, text="Hide Passwords",font=("Helvetica", 12, "bold"),bg="red",fg="white", command=self.hide_chrome_password_)
        self.hide_password_button.pack_forget()
        
        self.edge_password_button = tk.Button(root, text="Show Password",font=("Helvetica", 12, "bold"),bg="green",fg="white", command=self.show_edge_password)
        self.edge_password_button.pack_forget()
        self.edge_hide_password_button = tk.Button(root, text="Hide Passwords",font=("Helvetica", 12, "bold"),bg="red",fg="white", command=self.edge_hide_password)
        self.edge_hide_password_button.pack_forget()
        
        self.firefox_password_button = tk.Button(root, text="Show Password",font=("Helvetica", 12, "bold"),bg="green",fg="white", command=self.show_firefox_password)
        self.firefox_password_button.pack_forget()
        self.firefox_hide_password_button = tk.Button(root, text="Hide Passwords",font=("Helvetica", 12, "bold"),bg="red",fg="white", command=self.firefox_hide_password)
        self.firefox_hide_password_button.pack_forget()
        
        self.brave_password_button = tk.Button(root, text="Show Password",font=("Helvetica", 12, "bold"),bg="green",fg="white", command=self.brave_show_password)
        self.brave_password_button.pack_forget()
        self.brave_hide_password_button = tk.Button(root, text="Hide Passwords",font=("Helvetica", 12, "bold"),bg="red",fg="white", command=self.brave_hide_password)
        self.brave_hide_password_button.pack_forget()
        
      
        # create menu widget
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        # create chrome browser submenu
        self.chrome_menu = tk.Menu(self.menu, tearoff=False)
        self.chrome_menu.add_command(
            label="Credentials", command=self.chromecredentials)
        self.chrome_menu.add_command(
            label="History", command=self.chrome_history)
        self.chrome_menu.add_command(
            label="Cookies", command=self.chrome_cookies)
        self.chrome_menu.add_command(
            label="Autofill", command=self.chrome_autofill)
        self.chrome_menu.add_command(
            label="Credits card", command=self.chrome_credit)
        self.chrome_menu.add_command(
            label="Search Terms", command=self.chrome_seach)

        # create Edge browser submenu
        self.edge_menu = tk.Menu(self.menu, tearoff=False)
        self.edge_menu.add_command(
            label="Credentials", command=self.edge_credentials)
        self.edge_menu.add_command(label="History", command=self.edge_history)
        self.edge_menu.add_command(label="Cookies", command=self.edge_cookie)
        self.edge_menu.add_command(
            label="Downlaods", command=self.edge_downloaded)

        # create Firefox browser submenu
        self.firefox_menu = tk.Menu(self.menu, tearoff=False)
        self.firefox_menu.add_command(
            label="Credentials", command=self.firefox_credentials)
        self.firefox_menu.add_command(
            label="History", command=self.firefox_hsitories)
        self.firefox_menu.add_command(
            label="Cookies", command=self.firefox_cookie)
        # self.firefox_menu.add_command(label="Web data", command=self.opera)
        # create brave browser submenu
        self.brave_menu = tk.Menu(self.menu, tearoff=False)
        self.brave_menu.add_command(
            label="credentials", command=self.brave_credentials)
        self.brave_menu.add_command(label="Cookies", command=self.brave_cookie)
        self.brave_menu.add_command(
            label="History", command=self.brave_history)
        # self.brave_menu.add_command(label="Web data", command=self.opera)

        # create wifi submenu
        self.wifi_menu = tk.Menu(self.menu, tearoff=False)
        # self.wifi_menu.add_command(label="Credentials", command=self.connect)
        self.wifi_menu.add_command(
            label="Credentials", command=self.disconnect)

        self.main_menu = tk.Menu(self.menu, tearoff=False)
        # self.main_menu.add_command(label="Title", command=self.chrome())

        # add submenus to main menu
        self.menu.add_cascade(label="Chrome", menu=self.chrome_menu, font=("Helvetica", 14))
        self.menu.add_cascade(label="Edge", menu=self.edge_menu)
        self.menu.add_cascade(label="FireFox", menu=self.firefox_menu)
        self.menu.add_cascade(label="Brave", menu=self.brave_menu)
        self.menu.add_cascade(label="Wifi", menu=self.wifi_menu)

        self.edge_password_lines = [line for line in  edge_browser.get_edge_creds().split('\n') if not line.startswith("Password")]
        self.password_lines_hide = [line for line in  password_data.split('\n') if not line.startswith("Password")]
        self.firefox_password_lines = [line for line in  firefox.main().split("\n") if not line.startswith("Password")]
        self.brave_password_lines = [line for line in  brave.brave_passwords().split("\n") if not line.startswith("Password")]

    def unpack_data(self):
        try:
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.password_label.config(text="")
            self.password_button.pack_forget()
            self.hide_password_button.pack_forget()
            self.edge_password_button.pack_forget()
            self.edge_hide_password_button.pack_forget()
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
        except Exception as e:
            messagebox.showerror("Error",e)

    def pack_data(self):
        try:
            self.password_label.pack(pady=10)
            self.button2.pack(side=tk.RIGHT, pady=20, anchor=tk.CENTER, padx=10)
            self.button.pack(side=tk.RIGHT, pady=20, anchor=tk.CENTER, padx=10)
        except Exception as e:
            messagebox.showerror("Error",e)
    def show_password(self):
        self.listbox.delete(0, tk.END)
        try:
            for line in password_data.split("\n"):
                self.listbox.insert(tk.END, line)
                if line.startswith("Password"):
                    self.listbox.itemconfig(tk.END, fg="white", bg="green")
            # self.listbox.insert(tk.END, *self.password_lines_show)
            self.hide_password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
            self.password_button.pack_forget()
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.password_label.config(text="")
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
        except Exception as e:
            messagebox.showerror('Error', e)
            
    def hide_chrome_password_(self):
        try:
            self.chromecredentials()
            self.hide_password_button.pack_forget()
        except Exception as e:
            messagebox.showerror('Error', e)
        
    #Ege password displaying
    def show_edge_password(self):
        self.listbox.delete(0, tk.END)
        try:
            for line in edge_browser.get_edge_creds().split("\n"):
                self.listbox.insert(tk.END, line)
                if line.startswith("Password"):
                    self.listbox.itemconfig(tk.END, fg="white", bg="green")
            # self.listbox.insert(tk.END, *self.password_lines_show)
            self.edge_hide_password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
            self.password_button.pack_forget()
            self.edge_password_button.pack_forget()
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
            self.password_label.config(text="")
        except Exception as e:
            messagebox.showerror('Error', e)
            
    def edge_hide_password(self):
        try:
            self.edge_credentials()   
            self.edge_hide_password_button.pack_forget()
        except Exception as e:
            messagebox.showerror('Error', e)
            
    def show_firefox_password(self):
        self.listbox.delete(0, tk.END)
        try:
            for line in firefox.main().split("\n"):
                self.listbox.insert(tk.END, line)
                if line.startswith("Password"):
                    self.listbox.itemconfig(tk.END, fg="white", bg="green")
            # self.listbox.insert(tk.END, *self.password_lines_show)
            self.firefox_hide_password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
            self.password_button.pack_forget()
            self.edge_password_button.pack_forget()
            self.firefox_password_button.pack_forget()
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
            self.password_label.config(text="")
        except Exception as e:
            messagebox.showerror('Error', e) 
    def firefox_hide_password(self):
        try:
            self.firefox_credentials()   
            self.firefox_hide_password_button.pack_forget() 
        except Exception as e:
            messagebox.showerror('Error', e)
        
    def brave_show_password(self):
        self.listbox.delete(0, tk.END)
        try:
            for line in brave.brave_passwords().split("\n"):
                self.listbox.insert(tk.END, line)
                if line.startswith("Password"):
                    self.listbox.itemconfig(tk.END, fg="white", bg="green")
            # self.listbox.insert(tk.END, *self.password_lines_show)
            self.brave_hide_password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
            self.password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.edge_password_button.pack_forget()
            self.firefox_password_button.pack_forget()
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.password_label.config(text="")
        except Exception as e:
            messagebox.showerror('Error', e)
             
    def brave_hide_password(self):
        self.brave_credentials()
        self.brave_hide_password_button.pack_forget() 
        
           
    def chromecredentials(self):
        self.label.config(text="Chrome Credentials storages")
        try: 
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, *self.password_lines_hide)
            self.password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.edge_password_button.pack_forget()
            self.edge_hide_password_button.pack_forget()
            self.password_label.config(text="")
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
        except Exception as e:
            messagebox.showerror('Error', e)

    def chrome_cookies(self):
        self.label.config(text="Chrome Cookies selected")
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, *cookies.splitlines())
        self.unpack_data()
        self.password_button.pack_forget()

    def chrome_history(self):
        self.label.config(text="Chrome Cookies selected")
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, *web_history.splitlines())
        self.unpack_data()

    def chrome_seach(self):
        self.label.config(text="Chrome Search terms selected")
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, *search_terms)
        self.unpack_data()

    def chrome_autofill(self):
        self.label.config(text="Chrome autofill information")
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, *autofill_data.splitlines())
        self.unpack_data()

    def chrome_credit(self):
        self.label.config(text="Chrome credit cart information")
        self.unpack_data()
        try:
            if len(credit_card_info) != 0:
                self.listbox.delete(0, tk.END)
                self.listbox.insert(tk.END, *credit_card_info)
            else:
                self.listbox.delete(0, tk.END)
                messagebox.showinfo(
                    title="Info", message="No credit card information available")
        except Exception as e:
            messagebox.showerror("Error", f"[E] {str(e)}")

    def firefox_credentials(self):
        try:
            self.label.config(text="Firefox Credentials selected")
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.edge_password_button.pack_forget()
            self.edge_hide_password_button.pack_forget()
            self.password_label.config(text="")
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, *self.firefox_password_lines)
            self.firefox_password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
        except Exception as e:
            messagebox.showerror("Error", f"[E] {str(e)}")

    def firefox_cookie(self):
        self.unpack_data()
        self.label.config(text="Firefox Cookies selected")
        self.listbox.delete(0, tk.END)
        try:
            self.listbox.insert(
                tk.END, *firefox1.firefox_cookies().splitlines())
        except Exception as e:
            messagebox.showerror("Error", f"[E] {str(e)}")

    def firefox_hsitories(self):
        self.unpack_data()
        self.label.config(text="Firefox History selected")
        self.listbox.delete(0, tk.END)
        try:
            self.listbox.insert(
                tk.END, *firefox1.firefox_history().splitlines())
        except Exception as e:
            messagebox.showerror("Error", f"[E] {str(e)}")

    def edge_credentials(self):
        self.unpack_data()
        self.label.config(text="Edge credentials selected")
        try:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(
                tk.END, *self.edge_password_lines)
            self.edge_password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
            self.button2.pack_forget()
            self.button.pack_forget()
            self.password_label.pack_forget()
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
            self.password_label.config(text="")
        except Exception as e:
            self.listbox.delete(0, tk.END)
            messagebox.showerror("Error", f"[E] {str(e)}")

    def edge_cookie(self):
        self.label.config(text="Edge Cookies selected")
        self.unpack_data()
        try:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(
                tk.END, *edge_browser.edge_cookies().splitlines())
        except Exception as e:
            self.listbox.delete(0, tk.END)
            messagebox.showerror("Error", f"[E] {str(e)}")

    def edge_history(self):
        self.unpack_data()
        self.label.config(text="Edge History selected")
        try:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, *edge_browser.edge_history())
        except Exception as e:
            self.listbox.delete(0, tk.END)
            messagebox.showerror("Error", f"[E] {str(e)}")

    def edge_downloaded(self):
        self.unpack_data()
        self.label.config(text="Edge History selected")
        try:
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, *edge_browser.edge_downloads())
        except Exception as e:
            self.listbox.delete(0, tk.END)
            messagebox.showerror("Error", f"[E] {str(e)}")

    # brave credentials functionality
    def brave_credentials(self):
        self.unpack_data()
        self.brave_password_button.pack(side=tk.TOP, pady=20, anchor=tk.CENTER, padx=10)
        self.label.config(text="Brave credentials selected")
        try:
            self.listbox.delete(0, tk.END)
            if brave.get_installed_browsers():
                if brave.kill_program("brave.exe"):
                    messagebox.showinfo(
                        "Running", "Brave browser was running. It has been killed")
                else:
                    self.listbox.insert(
                        tk.END, *self.brave_password_lines)
            else:
                messagebox.showwarning(
                    "Warning", "Brave browser is not installed!")
        except Exception as e:
            messagebox.showerror("Error", f"[E] {str(e)}")

    def brave_history(self):
        self.unpack_data()
        self.label.config(text="Brave History selected")
        try:
            if brave.get_installed_browsers():
                if brave.kill_program("brave.exe"):
                    messagebox.showinfo(
                        "Running", "Brave browser was running. It has been killed")
                else:
                    self.listbox.delete(0, tk.END)
                    self.listbox.insert(
                        tk.END, *brave.get_brave_history().splitlines())
            else:
                self.listbox.delete(0, tk.END)
                messagebox.showwarning(
                    "Warning", "Brave browser is not installed! Please install it for forensic")
        except Exception as e:
            messagebox.showerror("Error", f"[E] {str(e)}")
            self.listbox.delete(0, tk.END)

    def brave_cookie(self):
        self.unpack_data()
       
        self.label.config(text="Brave Cookies selected")
        try:
            if brave.get_installed_browsers():
                if brave.kill_program("brave.exe"):
                    messagebox.showinfo(
                        "Running", "Brave browser was running. It has been killed")
                else:
                    self.listbox.delete(0, tk.END)
                    self.listbox.insert(
                        tk.END, *brave.brave_cookies().splitlines())
            else:
                self.listbox.delete(0, tk.END)
                messagebox.showwarning(
                    "Warning", "Brave browser is not installed! Please install it for forensic")
        except Exception as e:
            messagebox.showerror("Error", f"[E] {str(e)}")
            self.listbox.delete(0, tk.END)

# Wifi ---- info
    def disconnect(self):
        try:
            self.label.config(text="Wifi Profiles")
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, *winpass.get_devices_info().splitlines())
            self.button.pack(side=tk.LEFT, pady=20, anchor=tk.CENTER, padx=10)
            self.password_button.pack_forget()
            self.hide_password_button.pack_forget()
            self.edge_password_button.pack_forget()
            self.edge_hide_password_button.pack_forget()
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
        except Exception as e:
            messagebox.showerror('Error',str)

    def scan_wifi_profiles(self):
        try:
            self.password_button.pack_forget()
            self.hide_password_button.pack_forget()
            self.edge_password_button.pack_forget()
            self.edge_hide_password_button.pack_forget()
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
            self.password_label.pack(pady=10)
            self.button2.pack(side=tk.RIGHT, pady=20, anchor=tk.CENTER, padx=10)
            try:
                self.listbox.delete(0, tk.END)
                self.listbox.insert(tk.END, *winpass.get_wifi_profile())
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def profile_show_password(self):
        try: 
            self.password_button.pack_forget()
            self.hide_password_button.pack_forget()
            self.edge_password_button.pack_forget()
            self.edge_hide_password_button.pack_forget()
            self.firefox_password_button.pack_forget()
            self.firefox_hide_password_button.pack_forget()
            self.brave_password_button.pack_forget()
            self.brave_hide_password_button.pack_forget()
            selected_item = self.listbox.get(self.listbox.curselection())
            try:
                output = subprocess.check_output(
                    ["netsh", "wlan", "show", "profile", selected_item, "key=clear"], shell=True)
                output = output.decode("utf-8")
                password_line = [line.strip() for line in output.split(
                    "\n") if "Key Content" in line][0]
                password = password_line.split(":")[1].strip()
                self.password_label.config(
                    text=f"Password for: {selected_item} ==> {password}", background="black")
                tk.Button(self.password_label, text="Copy",
                        command=lambda: root.clipboard_append(password))
            except Exception as e:
                messagebox.showerror(title=selected_item, message=str(e))
        except Exception as e:
            messagebox.showwarning("Warning", "Please select Wi-Fi profile!!!")

def center_window(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')


if __name__ == "__main__":
    root = tk.Tk()
    menu = Main(root)
    center_window(root, 800, 500)
    root.mainloop()