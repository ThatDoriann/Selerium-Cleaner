import os
import shutil
import requests
import subprocess
import psutil
import time
from colorama import Fore
from colorama import init

currentDir = os.path.dirname(os.path.abspath(__file__))
localAppData = os.getenv('LOCALAPPDATA')
temp = os.getenv('TEMP')

installerUrl = "https://www.roblox.com/download/client?os=win&renderingPlatform=nextjs"
lookForFolders = {"Roblox", "Fishstrap", "Bloxstrap", "Voidstrap"}

def log(message):
    print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] {message}')

def info(message):
    print(f'[{Fore.LIGHTCYAN_EX}@{Fore.RESET}] {message}')

def warn(message):
    print(f'[{Fore.LIGHTYELLOW_EX}!{Fore.RESET}] {message}')

def error(message):
    print(f'[{Fore.LIGHTRED_EX}-{Fore.RESET}] {message}')

def niceInput(prompt):
    return input(f'[{Fore.LIGHTCYAN_EX}?{Fore.RESET}] {prompt} ')

def delRoblox():
    notFound = {}
    for folder in lookForFolders:
        folderPath = os.path.join(localAppData, folder)
        if os.path.exists(folderPath):
            shutil.rmtree(folderPath)
            log(f"{folder} deleted successfully.")
        else:
            notFound[folder] = True
    
    if notFound:
        warn(f"{', '.join(notFound.keys())} not found.")

def delTemp():
    for folder in lookForFolders:
        folderPath = os.path.join(temp, folder)
        if os.path.exists(folderPath):
            shutil.rmtree(folderPath)
            log(f"{folder} deleted successfully.")

def closeRoblox():
    for process in psutil.process_iter():
        if process.name() == "RobloxPlayerBeta.exe":
            process.kill()
            log("Roblox client closed.")
            return True
    warn("Roblox client not running.")
    return False

def installRoblox():
    downloadPath = os.path.join(temp, "RobloxPlayerLauncher.exe")
    
    response = requests.get(installerUrl)
    if response.status_code == 200:
        with open(downloadPath, 'wb') as file:
            file.write(response.content)
        log("Roblox installer downloaded successfully.")
        
        process = subprocess.Popen([downloadPath])
        process.wait()
        log("Roblox installation completed.")
        
        os.remove(downloadPath)
        log("Roblox installer deleted.")
    else:
        error("Failed to download Roblox installer.")


info("selerium cleaner v2.0 rewrite created by z.raf @ discord")
info("this version is a complete rewrite of the original selerium v1.0, with improved functionality.")
info("currently supports -> fishtrap, bloxstrap, and voidstrap")
info("last updated -> 28/09/2026")
print("———————————————————————————————————————————————————————")

time.sleep(0.5)
log('starting cleaner...')
start_time = time.time()

closeRoblox()
delRoblox()
delTemp()
installRoblox()
closeRoblox()

info(f'successfully cleaned roblox in {time.time() - start_time:.2f} seconds! exiting...')
time.sleep(5)
