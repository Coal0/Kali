import sys
import subprocess

if __name__ == "__main__":
    print("Upgrading...")
    try:
        subprocess.check_call(
          "apt-get update && apt-get upgrade && apt-get dist-upgrade",
          shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Upgrade failed, try again.")
    else:
        print("Upgrade successful.")
        if sys.version_info.major < 3:
            if raw_input("Reboot [Y/N]: ") in ("Y", "y"):
                subprocess.call("reboot", shell=True)
        else:
            if input("Reboot [Y/N]: ") in ("Y", "y"):
                subprocess.call("reboot", shell=True)
