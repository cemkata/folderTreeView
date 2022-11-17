#!/usr/bin/python3
from bottle import Bottle, request, redirect, template, static_file, HTTPError
import json
import os
import time
import shutil
from urllib.parse import unquote

ver="2.0"

app = Bottle()

mediaRootFolder = ""
RecycleBinEnabled = -1
RecycleBin = ""

skipPaths = []
skipPrefix = []
skipExtension = []

fileComands = ['move', 'copy', 'delete', 'rename', 'folder']

@app.route('/uploadFile', method='POST')
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

@app.route('/fileCmd', method='post')
def fileCmd():
       comand = request.forms.get('comand') or -1
       if comand == -1:
          return HTTPError(404, "Page not found") 
       parameters = json.loads(comand)
       files = json.loads(parameters['fileNames'])
       fileComand(parameters['fileCMD'], parameters['sourceFolder'], parameters['targetFolder'], files)

@app.route('/getFileImages')
def getFileImages():
    fileImages = {
'blankIcon' : 'data:image/gif;base64, R0lGODlhFAAWAKEAAP///8z//wAAAAAAACH+TlRoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAh+QQBAAABACwAAAAAFAAWAAACE4yPqcvtD6OctNqLs968+w+GSQEAOw==',
'backIcon' : 'data:image/gif;base64, R0lGODlhFAAWAMIAAP///8z//5mZmWZmZjMzMwAAAAAAAAAAACH+TlRoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAh+QQBAAABACwAAAAAFAAWAAADSxi63P4jEPJqEDNTu6LO3PVpnDdOFnaCkHQGBTcqRRxuWG0v+5LrNUZQ8QPqeMakkaZsFihOpyDajMCoOoJAGNVWkt7QVfzokc+LBAA7',
'fileIcon' : 'data:image/gif;base64, R0lGODlhEgAWAEAAACH+T1RoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAAIfkEAQAAAQAsAAAAABIAFgCHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACGUAYwgcSHDgvoMHYyBciFChwoYMGT58uI9ixIoQMV5MuNDhxoMAYoQcaTEigJMoQ348mKllS5Ur97nMBDMmy5o2aZZcqdMmwp4+ZeKMCdRn0ZxDeSb9eJRoyBgzo0YVCTKl1asBAQA7',
'folderIcon' : 'data:image/gif;base64, R0lGODlhEwARAEAAACH+T1RoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAAIfkEAQAAAgAsAAAAABMAEQCHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACMUA9+0DQLAgQYEIEw7UN4+hw3kAFCIEMG8etHnK5j2jl0yfwYMDJc2j96xhMnr5GOVDyTIiAH2SdknixYjXLpUkOZLkRXDkynwdO847CVRfLUkxACjLlzEjyoz6hC7llXRlSX0ln5pEyWhXUp1MR27USI9sPqQAfkI9OfYiR15UlYadm9MsvUhVy16MWpbpyo6L4rIdKdQt0alJGeYE+tRq2ZlJO0a6S3nyLmW7KscYaItXJLieecUUvUt0jM0DT6tezXpzQAA7'
}
    return json.dumps(fileImages)

@app.route('/', method='get')
def emptyIndex():
    return index("/")

@app.route('/<filepath:path>', method='get')
def index(filepath):
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
