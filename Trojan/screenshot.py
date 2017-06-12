import win32gui
import win32ui
import win32con
import win32api

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
screenshot.SaveBitmapFile(mem_dc, 'C:\\Users\\Educontract\\Desktop\\Kali_Networking_Python2.7\\Trojan\\screenshot.bmp')

# Free Mem
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())

