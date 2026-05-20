import win32gui
import win32con
import win32api

def make_overlay(title: str) -> None:
    """Applies always-on-top and transparent styles to the given window handle."""

    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        return

    ex_style = ( 
        win32con.WS_EX_LAYERED |
        win32con.WS_EX_TRANSPARENT |
        win32con.WS_EX_TOPMOST
    )

    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)