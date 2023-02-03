import os
import collections
from bottle import template

import folderTreeView
folderTreeView.updateTimer.cancel()

folderTemplate = '''<p class="heading"><b>__folder__</b></p>'''
itemsTemplate = '''<div class="content">__idems__</div>'''
fileTemplate = '''<p>__file__</p>'''

def checkHidenFiles(instring):
    if(instring in folderTreeView.skipPaths):
       return False
    for prefix in folderTreeView.skipPrefix:
        if(instring.startswith(prefix)):
            return False
    for extension in folderTreeView.skipExtension:
        if(instring.endswith(extension)):
            return False
    return True	
	
def dict_to_html(inDict):
    finalHtml = ""
    if inDict['type'] == 'directory':
        finalHtml += folderTemplate.replace("__folder__", inDict['name'])
        itemsList = ""
        folderContent = inDict['children']
        for x in folderContent:
            item = dict_to_html(x)
            itemsList += fileTemplate.replace("__file__", item)
        finalHtml += itemsTemplate.replace("__idems__", itemsList)
        return finalHtml
    else:
        return inDict['name']

tmpDict = folderTreeView.path_to_dict(folderTreeView.serverRoot, False)
folderHTML = dict_to_html(tmpDict)

outputFolder = os.path.join(os.getcwd(), "html_output")
if not os.path.exists(outputFolder):
   # Create a new directory because it does not exist
   os.makedirs(outputFolder)

outFileName = os.path.join(outputFolder, f'result_{folderTreeView.titleFolder}.html')
with open(outFileName, mode='w', encoding='utf-8') as f:
    f.write(template('html_export', title = "Content of "+folderTreeView.titleFolder, html = folderHTML))

print(f"Export done in {outputFolder}.")
print(f"File name - result_{folderTreeView.titleFolder}.html")