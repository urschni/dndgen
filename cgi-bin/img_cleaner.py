import os, time
    
def clean():
    path = os.getcwd() + "\\tmp_dungeon_img"
    now = time.time()
    
    for f in os.listdir(path):
        file_path = os.path.join(path,f)
        if(os.stat(file_path).st_mtime < now - 900): #1 hour = 3600
            if(os.path.isfile(file_path)):
                os.remove(file_path)

def thread():
    print("cleaner startet")              
    starttime = time.time()
    while True:
        print("cleaning files")
        clean()
        time.sleep(600 - (time.time()- starttime) % 600.0)