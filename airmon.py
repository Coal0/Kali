import os,sys

# probe TCP SYN 
# TCP ACK probes --PA syn or ack both!

# UDP --higher is better [53]
# ping types ..echo request -PE ..timestamp -PP ..netmask -PW

def nmap():
    nmap_quit = False
    d = { "local" : "192.168.1.0/24 " , 
	"all" : " -p- ", 
	"common" : "-F ",
	"defcon" : "-PE -PP -PS21,22,23,25,80,113,21339 -PA80,113,443,10042 --source_port 53 ",
        "os" : "-A ",
	"write" : "-oN out.txt "
        }
    while not nmap_quit:
        print("--- MENU ---")
        print("")
        print("--- port [all,common,defcon] or os  ---")
        print("")
        print("--- write ---")
        print("")
        print("--- local or target ---")
        command = "nmap -v "
        for i in input(">>> ").split():
            if(i=="quit") : nmap_quit = True; break
            try:
                if(i=="target"):
                    k = raw_input("target>>> ")
                    command += k
                elif(i!="port"):
                    print(d[i])
                    k = d[i]
                    command += k
            except:
                print("Failed")
                break
        print(command)
        os.system(command)

quit = False
while not quit:
    choices = [ "nmap", "airm", "aird", "airr", "quit" ]
    print("--- MENU ---")
    print("------------")
    print("---######---")
    print("--- nmap ---")
    print("")
    print("---######---")
    print("--- airm ---")
    print("--- aird ---")
    print("--- airr ---")
    print("--- airc ---")
    print("")
    print("------------")
    print("--- quit ---")
    choice = input(">>>")
    print(choice, choices)
    if(choice in choices):
        if(choice == "nmap"):
            nmap()
        if(choice== "airm"):
            if(str(input("Start[Y/N]:")) == "Y"):
                os.system("airmon-ng start wlan0")
                os.system("airmon-ng check kill")
            if(str(input("Stop[Y/N]:")) == "Y"):
                os.system("airmon-ng stop wlan0mon")
                os.system("ifconfig wlan0 down")
                os.system("ifconfig wlan0 up")
        if(choice== "aird"):
            if(str(input("See All[Y/N]:")) == "Y"):
                os.system("airodump-ng wlan0mon")
            if(str(input("target[Y/N]:")) == "Y"):
                b = raw_input("BSSID:")
                c = raw_input("CHANNEL:")
                if(str(input("Write[Y/N]:")) == "Y"):
                    os.system("airodump-ng wlan0mon --bssid "+b+" --channel "+c+" -w dump")  
                else:
                    os.system("airodump-ng wlan0mon --bssid " + b + " --channel " + c)    
        if(choice== "airr"):
            b = str(input("BSSID:"))
            c = str(input("CHANNEL:"))

            os.system("airmon-ng stop wlan0mon")
            os.system("ifconfig wlan0 down")
            os.system("ifconfig wlan0 mode managed")
            os.system("ifconfig wlan0 up")
            os.system("ifconfig wlan0 channel " + c)
            os.system("ifconfig wlan0 down")
            os.system("ifconfig wlan0 mode monitor")
            os.system("ifconfig wlan0 up")
            os.system("airmon-ng start wlan0")

            os.system("aireplay-ng -1 0 -a " + b + " wlan0mon ")
        if(choice== "airc"):
            quit = False
        if(choice== "quit"):
            quit = True
