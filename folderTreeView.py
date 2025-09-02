#!/usr/bin/python3
from bottle import Bottle, run, static_file, template, abort
import os
import threading
from datetime import datetime
import re
import collections

app = Bottle()
ver = 4.0

cnfgFile = "config.ini"

skipPaths = []
skipPrefix = []
skipExtension = []
skipComents = "::"

dicts = [{},{}]
selcetedDict = 0

@app.route('/favicon.ico')
def favicon():
    return static_file('download.png', root='./views')

@app.route('/static/<filepath:path>')
def static_content(filepath):
     return static_file(filepath, root='./views/static')

@app.route('/ui/<filepath:path>')
def staticFiles(filepath):
    return static_file(filepath,  root='./views/ui')

@app.route('/')
def index(filepath = '/'):
   return template('index_new', title = "Content of "+titleFolder)

@app.route('/old')
def old_index():
    return template('index_old', title = "Content of "+titleFolder)

@app.route('/<filepath:path>')
def filesFolders(filepath = '/'):
   if os.path.isfile(os.path.join(docFolder, filepath)):
      return static_file(filepath, root=docFolder)
   else:
      abort(404, "Not Found.")

@app.route('/getFiles')
def filesFolders(filepath = '/'):
   if not dicts[selcetedDict] or updateInterval == 0:
      dicts[selcetedDict] = path_to_dict(serverRoot, webSort = False)
      dicts[selcetedDict]['timestamp'] = genTimeStamp()
   return dicts[selcetedDict]

@app.route('/getHelp')
def filesFolders(filepath = '/'):
   return template('help')

updateTimer = None

def updateDict():
    global selcetedDict
    didx = (selcetedDict + 1) % 2
    dicts[didx] = path_to_dict(serverRoot, webSort = False)
    if not dicts[didx]:
        print("Configuration problem")
        from sys import exit
        exit(1)
    dicts[didx]['timestamp'] = genTimeStamp()
    selcetedDict = didx
    global updateTimer
    updateTimer = threading.Timer(updateInterval, updateDict,[]) #this will allow stoping the thread
    updateTimer.start()

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

def path_to_dict(path, webSort = True):
    baseName = os.path.basename(path)
    d = collections.OrderedDict()
    if(checkHidenFiles(baseName)):
        d = {'name': baseName}
        if os.path.isdir(path):
            d['type'] = "directory"
            itemsList = []
            folderContent = os.listdir(path) #Get the content of the folder
            if webSort: #The web page sort the content automaticly
                if sortFlag is not None:
                    folderContent.sort(reverse=sortFlag) #Sort the list in reverse order
            else:
                files = []
                folders = []
                for fc in folderContent:
                   if os.path.isdir(os.path.join(path,fc)):
                       folders.append(fc)
                   else:
                       files.append(fc)
                if sortFlag is not None:
                    folders.sort(reverse=sortFlag, key=sort_condition)
                    files.sort(reverse=not sortFlag, key=sort_condition)
                    folderContent = folders + files
            for x in folderContent:
                item = path_to_dict(os.path.join(path,x), webSort)
                if item:
                    itemsList.append(item)
            d['children'] = itemsList
        else:
            d['type'] = "file"
        return d
    return False

def genTimeStamp():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
    return dt_string

def sort_condition(in_data):
    pattern = '^\\d+'
    if re.match(pattern, in_data):
        if leadingZero:
            return "0" * (total_number_length - len(re.search(pattern,\
                          in_data).group(0))) + in_data
    else:
        if caseInsensitive:
            return in_data[0].upper() + in_data[1:]
    return in_data

if os.path.isfile(cnfgFile):
    import configparser
    print("Found " + cnfgFile)
    config = configparser.ConfigParser()
    config.read(cnfgFile)
    port = config['DEFAULT']['Port']
    host = config['DEFAULT']['ip']
    ip_pattern = re.compile('(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])')
    if not ip_pattern.match(host):
        raise KeyError('Server IP address')
    serverRoot = os.path.abspath(config['DEFAULT']['serverRoot'])
    docFolder, titleFolder = os.path.split(serverRoot)
    cnfgSkipFile = config['DEFAULT']['skipPath']
    cnfgSkipPrefix = config['DEFAULT']['skipPrefix']
    cnfgSkipExtension = config['DEFAULT']['skipExtension']
    updateInterval = int(config['DEFAULT']['updateInterval'])
    sortFlag = config['DEFAULT']['sortFlag']
    if sortFlag.lower() == "true":
        sortFlag = True
    elif sortFlag.lower() == "false":
        sortFlag = False
    else:
        sortFlag = None

    leadingZero = config['DEFAULT']['leadingZero']
    if leadingZero.lower() == "false":
        leadingZero = False
    else:
        leadingZero = True
    total_number_length = 10 # maybe read from the config file later

    caseInsensitive = config['DEFAULT']['caseInsensitive']
    if caseInsensitive.lower() == "true":
        caseInsensitive = True
    else:
        caseInsensitive = False



    fileOrganaserFlag = config['DEFAULT']['fileOrganaserFlag']
    if fileOrganaserFlag.lower() == "true":
        import file_orginiser
        file_orginiser.mediaRootFolder = serverRoot
        file_orginiser.RecycleBinEnabled = config['FILEORGANISER']['recycle_bin_enabled']
        file_orginiser.RecycleBin = config['FILEORGANISER']['recyclebin_folder']
        if int(file_orginiser.RecycleBinEnabled) == 1:
        #Flag for deleteing from the disk or
        #just moving he files out from the media server root folder
        #to folder specified in RecycleBin
        #When the value is set to True the files are moved to RecycleBin. By Flase the files are deleted   RecycleBin = config_trash['DEFAULT']['recyclebin_folder']
            RecycleBinPath = os.path.join(file_orginiser.mediaRootFolder, file_orginiser.RecycleBin)
            #be sure that the folder exist
            if not os.path.exists(RecycleBinPath):
               os.makedirs(RecycleBinPath)
        app.mount('/files', file_orginiser.app)
    else:
        @app.route('/files/<filepath:path>')
        def fileshandler(filepath = '/'):
           abort(404, "Not cofiured")

    log2File = config['APPLOGER']['log2File']
    if log2File.lower() == "true":
        log2File = True
        access_log = config['APPLOGER']['access_log']
        app_log = config['APPLOGER']['app_log']
    else:
        log2File = False

else:
    print("Using default config")
    port = 8000
    host = '0.0.0.0'
    serverRoot = '.'
    cnfgSkipFile = "skipPaths.txt"
    cnfgSkipPrefix = "skipPrefix.txt"
    cnfgSkipExtension = "skipExtension.txt"
    updateInterval = 0;
    sortFlag = None
    caseInsensitive = False
    total_number_length = 10
    leadingZero = True
    log2File = False
    #serverRoot = config['DEFAULT']['serverRoot']
    docFolder, titleFolder = os.path.split(serverRoot)

##

skipedContent = [
                {'config':cnfgSkipFile, 'ignoreList':[], 'cnfigName':'skipPaths'},
                {'config':cnfgSkipPrefix, 'ignoreList':[], 'cnfigName':'skipPrefix'},
                {'config':cnfgSkipExtension, 'ignoreList':[], 'cnfigName':'skipExtension'}]

for sk in skipedContent:
    if os.path.isfile(sk['config']):
        with open(sk['config'], 'r', encoding='utf-8') as infile:
            print(f"Loading {sk['config']}")
            tmpList = []
            for line in infile:
                if not line.startswith(skipComents):
                    tmpList.append(line.rstrip())
            sk['ignoreList'] = list(filter(None, tmpList))
            if fileOrganaserFlag.lower() == "true":
                file_orginiser.skipPaths = sk['ignoreList']
    else:
        print(f"File not found {sk['config']}")
        print(f"  Skiping {sk['cnfigName']} configuration")

skipPaths     = skipedContent[0]['ignoreList']
skipPrefix    = skipedContent[1]['ignoreList']
skipExtension = skipedContent[2]['ignoreList']
##

if updateInterval == 0:
   pass
elif updateInterval < 0:
   updateInterval = -1 * updateInterval * 60 * 60
   # 60 * 60 is hour
   print(f"Scaning {titleFolder}")
   updateDict()
else:
   updateInterval = updateInterval * 60
   # This is in munites
   print(f"Scaning {titleFolder}")
   updateDict()

print(f"Starting treeViewDocu - version {ver}")
if __name__ == "__main__":
    if log2File:
        import sys
        from tee import StdoutTee, StderrTee
        with StdoutTee(app_log), StderrTee(access_log):
            run(app, host = host, port = port, debug=True)
    else:
        run(app, host = host, port = port, debug=True)
