import win32gui
import win32con
import win32console
import os

def hide_console_window():
    """
    Hides the console window of the program.
    """
    console_window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(console_window, 0)

def hide_program_window():
    """
    Hides the program's window from the taskbar and Alt-Tab menu.
    """
    # Find the main program window by class name or process ID
    def enum_windows_callback(hwnd, windows):
        if windows["class_name"] and windows["class_name"] in win32gui.GetClassName(hwnd):
            windows["handle"] = hwnd
            return False
        if windows["process_id"] and windows["process_id"] == win32gui.GetWindowThreadProcessId(hwnd)[1]:
            windows["handle"] = hwnd
            return False
        return True

    windows = {"handle": None, "class_name": None, "process_id": None}

    # Modify the values below to match your program's window class name or process ID
    windows["class_name"] = "your_class_name"
    # windows["process_id"] = your_process_id

    win32gui.EnumWindows(enum_windows_callback, windows)
    program_window = windows["handle"]

    # Hide the program window
    if program_window:
        win32gui.ShowWindow(program_window, 0)
        ex_style = win32gui.GetWindowLong(program_window, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(program_window, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_TOOLWINDOW)
    else:
        raise Exception("Program window not found")

def stealth_mode():
    """
    Enables stealth mode by hiding the console window and the program's window from the taskbar and Alt-Tab menu.
    """
    try:
        hide_console_window()
        hide_program_window()
    except Exception as e:
        print(f"Error in stealth mode: {e}")
