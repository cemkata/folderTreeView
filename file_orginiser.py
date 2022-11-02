#!/usr/bin/python3
from bottle import Bottle, request, redirect, template, static_file, HTTPError
import json
import os
import configparser
import re
import time
import shutil
from urllib.parse import unquote

ver="1.2"

rootApp = Bottle()

@rootApp.route('/uploadFile', method='POST')
def do_upload():
    targetFolder = request.forms.get('targetFolder')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext.lower() in ('.zip', '.rar', '.exe', '.bat', '.vbs', '.com'):
        return "File extension not allowed."
    targetFolder = targetFolder.replace("/","",1)# strip the first slash "/"
    targetFolder = os.path.join(mediaRootFolder, targetFolder)
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)
    file_path = os.path.join(targetFolder, upload.filename)
    upload.save(file_path)
    return "File successfully uploaded"

@rootApp.route('/fileCmd', method='post')
def fileCmd():
       comand = request.forms.get('comand') or -1
       if comand == -1:
          return HTTPError(404, "Page not found") 
       parameters = json.loads(comand)
       files = json.loads(parameters['fileNames'])
       fileComand(parameters['fileCMD'], parameters['sourceFolder'], parameters['targetFolder'], files)

@rootApp.route('/files<filepath:path>', method='get')
def filesIndex(filepath):
   if not filepath.startswith("/"):
      return HTTPError(404, "Page not found")
   filepath = filepath.replace("/","",1)# strip the first slash "/" otherwise there is unexpected bahaviour of os.path.join or in this case just join
   if filepath.startswith("/"):
      return HTTPError(404, "Page not found")
   filepath = unquote(filepath)
   if os.path.isfile(os.path.join(mediaRootFolder, filepath)):
      return static_file(filepath, root=mediaRootFolder)
   else:
       client = request.query.client or 0
       if client == 0:
             return template('files', subFolder = filepath)
       elif client.lower() != "js":
             return template('files', subFolder = filepath)
       if '..' in filepath: #Security check and go to index
           return HTTPError(404, "Page not found")

       jsonOutput = json.dumps(getFolderContent(filepath))
       return jsonOutput
       
@rootApp.route('/ui/<filepath:path>')
def staticFiles(filepath):
    return static_file(filepath, root=webRootFolder)

@rootApp.route('/favicon.ico')
def favIcon():
    return static_file("img/favicon.png", root=webRootFolder)

@rootApp.route('/getFileImages')
def getFileImages():
    fileImages = {
'blankIcon' : 'data:image/gif;base64, R0lGODlhFAAWAKEAAP///8z//wAAAAAAACH+TlRoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAh+QQBAAABACwAAAAAFAAWAAACE4yPqcvtD6OctNqLs968+w+GSQEAOw==',
'backIcon' : 'data:image/gif;base64, R0lGODlhFAAWAMIAAP///8z//5mZmWZmZjMzMwAAAAAAAAAAACH+TlRoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAh+QQBAAABACwAAAAAFAAWAAADSxi63P4jEPJqEDNTu6LO3PVpnDdOFnaCkHQGBTcqRRxuWG0v+5LrNUZQ8QPqeMakkaZsFihOpyDajMCoOoJAGNVWkt7QVfzokc+LBAA7',
'fileIcon' : 'data:image/gif;base64, R0lGODlhEgAWAEAAACH+T1RoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAAIfkEAQAAAQAsAAAAABIAFgCHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACGUAYwgcSHDgvoMHYyBciFChwoYMGT58uI9ixIoQMV5MuNDhxoMAYoQcaTEigJMoQ348mKllS5Ur97nMBDMmy5o2aZZcqdMmwp4+ZeKMCdRn0ZxDeSb9eJRoyBgzo0YVCTKl1asBAQA7',
'folderIcon' : 'data:image/gif;base64, R0lGODlhEwARAEAAACH+T1RoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAAIfkEAQAAAgAsAAAAABMAEQCHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACMUA9+0DQLAgQYEIEw7UN4+hw3kAFCIEMG8etHnK5j2jl0yfwYMDJc2j96xhMnr5GOVDyTIiAH2SdknixYjXLpUkOZLkRXDkynwdO847CVRfLUkxACjLlzEjyoz6hC7llXRlSX0ln5pEyWhXUp1MR27USI9sPqQAfkI9OfYiR15UlYadm9MsvUhVy16MWpbpyo6L4rIdKdQt0alJGeYE+tRq2ZlJO0a6S3nyLmW7KscYaItXJLieecUUvUt0jM0DT6tezXpzQAA7'
}
    return json.dumps(fileImages)
    
@rootApp.route('/')
def index():
       redirect("/files/")

def getFolderContent(filepath):
    foldersList = []
    fileList = []
    try:
        for fn in os.listdir(os.path.join(mediaRootFolder, filepath)):
           if(checkHidenFiles(fn)):
              fileName = os.path.join(mediaRootFolder, filepath, fn)
              date = time.strftime('%Y-%M-%d %H:%M', time.localtime(os.path.getmtime(fileName)))
              if os.path.isdir(fileName):
                temp = {'name': fn , 'size': '-', 'date': date}
                foldersList.append(temp.copy())
              else:
                size = bytesConvert(os.path.getsize(fileName))
                temp = {'name': fn , 'size': size, 'date': date}
                fileList.append(temp.copy())
        perentfolder = os.path.dirname(filepath[:-1]) # remove the last slash '/'
        temp = {'perentfolder': perentfolder, 'files': fileList , 'folders': foldersList}
    except FileNotFoundError:
        temp = {'error': 'Not found'}
    return temp
       
def checkHidenFiles(instring):
    if(instring in skipPaths):
       return False
    for prefix in skipPrefix:
        if(instring.startswith(prefix)):
            return False
    for extension in skipExtension:
        if(instring.endswith(extension)):
            return False
    return True

def bytesConvert(inBytes):
    if inBytes < 0:
        return '-'
    step = 1024.
    precision = 1
    units = ['bytes','KB','MB','GB','TB']
    for i in range(len(units)):
        if (inBytes / step) >= 1:
            inBytes /= step
            inBytes = round(inBytes, precision)
            unit = units[i]
        else:
            return str(inBytes) + ' ' + units[i]

def fileComand(comand, source, traget, fileList):
    source = source.replace("/","",1)# strip the first slash "/"
    traget = traget.replace("/","",1)# strip the first slash "/"

    if RecycleBinEnabled and comand == fileComands[2]: #delete
        comand = fileComands[0]
        traget = RecycleBin
    
    if comand == fileComands[0]: #move
        for f in fileList:
           sorceFile = os.path.join(mediaRootFolder, source, f)
           targetFile = os.path.join(mediaRootFolder, traget, f)
           os.rename(sorceFile, targetFile)
        return

    elif comand == fileComands[1]: #copy
        for f in fileList:
           sorceFile = os.path.join(mediaRootFolder, source, f)
           targetFile = os.path.join(mediaRootFolder, traget, f)
           if os.path.isfile(sorceFile): ## If it is a file ##
              shutil.copy2(sorceFile, targetFile)
           else:                         ## If it is a folder ## 
              copytree(sorceFile, targetFile)
        return
    elif comand == fileComands[2]: #delete
        for f in fileList:
           sorceFile = os.path.join(mediaRootFolder, source, f)
           if os.path.isfile(sorceFile): ## If it is a file ##
              os.remove(sorceFile)
           else:                         ## If it is a folder ## 
              shutil.rmtree(sorceFile)
        return
    elif comand == fileComands[3]: #rename
        if len(fileList) > 1:
            i = range(0, len(fileList))
        else:
            i = ""
        for f in fileList:
           sorceFile = os.path.join(mediaRootFolder, source, f)
           targetFile = os.path.join(mediaRootFolder, source, traget + str(i))
           os.rename(sorceFile, targetFile)
           try:
               i+=1
           except TypeError:
               pass
    elif comand == fileComands[4]: #new folder
        targetFile = os.path.join(mediaRootFolder, traget)
        if not os.path.exists(targetFile):
            os.makedirs(targetFile)
        return

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

configFile = "config.ini"
configFile2 = "file_orginiser_config.ini"

if not os.path.isfile(configFile) or not os.path.isfile(configFile2) :
   print("Config file not found.")
   exit(0)

config_all = configparser.ConfigParser()
config_all.read(configFile)

config_trash = configparser.ConfigParser()
config_trash.read(configFile2)

skipPaths = []
skipPrefix = []
skipExtension = []
skipComents = "::"

try:
   mediaRootFolder = config_all['DEFAULT']['serverRoot']
   RecycleBinEnabled = config_trash['DEFAULT']['recycle_bin_enabled']
   RecycleBin = config_trash['DEFAULT']['recyclebin_folder']
   
   if int(RecycleBinEnabled) == 1:
     #Flag for deleteing from the disk or
     #just moving he files out from the media server root folder
     #to folder specified in RecycleBin
     #When the value is set to True the files are moved to RecycleBin. By Flase the files are deleted   RecycleBin = config_trash['DEFAULT']['recyclebin_folder']
     RecycleBinPath = os.path.join(mediaRootFolder, RecycleBin)
     #be sure that the folder exist
     if not os.path.exists(RecycleBinPath):
       os.makedirs(RecycleBinPath)
   serverIP = config_all['DEFAULT']['ip']
   ip_pattern = re.compile('(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])')
   testIP = ip_pattern.match(serverIP)
   if testIP:
     pass
   else:
     raise KeyError('Server IP address')
   
   serverPort = int(config_all['DEFAULT']['port'])+100

   cnfgSkipFile = config_all['DEFAULT']['skipPath']
   cnfgSkipPrefix = config_all['DEFAULT']['skipPrefix']
   cnfgSkipExtension = config_all['DEFAULT']['skipExtension']

   if os.path.isfile(cnfgSkipFile):
      with open(cnfgSkipFile, 'r', encoding='utf-8') as infile:
         print("Loading " + cnfgSkipFile)
         for line in infile:
            if not line.startswith(skipComents):
               skipPaths.append(line.rstrip())
         skipPaths = list(filter(None, skipPaths))
   else:
      print("File not found " + cnfgSkipFile)
      print("  Skiping skipPaths configuration")

   if os.path.isfile(cnfgSkipPrefix):
      with open(cnfgSkipPrefix, 'r', encoding='utf-8') as infile:
         print("Loading " + cnfgSkipPrefix)
         for line in infile:
            if not line.startswith(skipComents):
               skipPrefix.append(line.rstrip())   
         skipPrefix = list(filter(None, skipPrefix))         
   else:
      print("File not found " + cnfgSkipPrefix)
      print("  Skiping skipPrefix configuration")

   if os.path.isfile(cnfgSkipExtension):  
      with open(cnfgSkipExtension, 'r', encoding='utf-8') as infile:
         print("Loading " + cnfgSkipExtension)
         for line in infile:
            if not line.startswith(skipComents):
               skipExtension.append(line.rstrip())
         skipExtension = list(filter(None, skipExtension))

except KeyError as e:
   print("Problem in the configuration file.\nPlease check the value for " + str(e))
   exit(0)
except ValueError as e:
   print("Problem in the configuration file.\nPlease check the value for " + str(e))
   exit(0)

webRootFolder = os.path.join('.', 'views/ui/')
fileComands = ['move', 'copy', 'delete', 'rename', 'folder']


if __name__ == '__main__':
    print("Starting file organiser " + ver)
    if mediaRootFolder is '.': # some security. We dont want to show all the python scripts
                               # in future a login form may be added
       print("Please change the root folder of the file server!!!")
       print("Exiting now!")
       input("Press enter...")
    else:
       rootApp.run(host = serverIP, port = serverPort, debug=True)
