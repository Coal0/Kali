import win32gui
import win32ui
import win32con
import win32api

hdesktop = win32gui.GetDesktopWindow()
width = win32api.GetSystemMetric(win32con.SM_CXVIRTUALSCREEN)
heigth = win32api.GetSystemMetric(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetric(win32con.SM_XVVIRTUALSCREEN)
top = win32api.GetSystemMetric(win32con.SM_YVVIRTUALSCREEN)
dektop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32gui.CreateDCFFromHandle(dektop_dc)
mem_dc = img_dc.CreateCompatibleDC()
screenshot = win32gui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, (left, top), win32con.SRCCOPY)
screenshot.SaveBitmapFile(mem_dc, 'C:\\WINDOWS\\Temp\\screenshot.bmp')
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())

