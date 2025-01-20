import subprocess

#subprocess.run("python3 MMI.py", shell=True, capture_output=True, text=True)
subprocess.run("h5topng -t 0:100 -R -Zc dkbluered -a yarg -A ./MMI-out/MMI-eps-000000.00.h5 ./MMI-out/MMI-ez.h5", shell=True, capture_output=True, text=True)
subprocess.run("convert ./MMI-out/MMI-ez.t*.png ez.gif", shell=True, capture_output=True, text=True)
