
from selen_module import *


if __name__ == '__main__':
    dv = boot()
    startup_link(dv)
    
    print("Press ENTER when the bot can start working.")
    start = input()
    
    time.sleep(5)
    worker(dv)
    
    killb(dv)