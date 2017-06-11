import sys, os
os.system("apt-get update && apt-get upgrade && apt-get dist-upgrade")
if(str(input('Reboot [Y/N]:')) == in ['Y', 'y']): os.system("reboot")


