import os
import time

def restart(file_name:str):
    time.sleep(5)
    os.system('nohup python {} > nohup.out'.format(file_name))
