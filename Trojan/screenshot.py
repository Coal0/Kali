import win32gui
import win32ui
import win32con
import win32api

import os


def save_screenshot():
    # Get screen size
    w = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    h = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    l = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    t = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    # Create
    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    # Fill
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, w, h)
    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt((0,0),(w, h) , img_dc, (l,t), win32con.SRCCOPY)

    i = 0
    while os.path.exists("screenshot%s.bmp" % i):
        i += 1
    filename = os.join(os.getcwd() ,screenshot%s.bmp' % str(i))
    screenshot.SaveBitmapFile(mem_dc, filename)

    # Free Mem
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

if __name__=='__main__':
    save_screenshot()
