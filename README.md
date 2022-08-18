# Simple http server
This will list the content of a folder and alow the viewing of selected file.
It need only python no other frameworks execpt [bottle framework](https://github.com/bottlepy/bottle).  

How to configure in config.ini  
- port - Poer where the webserver will listen
- ip - Address where ther server will listen. 0.0.0.0 will listen on any v4 IP.
- serverRoot - Folder that will be listed. Can be relative or full path.
- skipPath - file containing the paths to be skipped when listing the folder
- skipPrefix - File with prefixes of files to be ignored. For exsample all file starting with .(dot).
- skipExtension - skipp files exnding with this extensions. Files that can not be visualised in browser (exe, rar, etc)
- updateInterval - how ofther the folder is scaned for updates:
	- 0 is disabled. Each reload of the page will scan the folder. Imidiate update but bad loading times
	- 1,2,3 ... is in munites (no minus (positive))
	- -1,-2,-4 ... in in hours (negative)
- sortFlag = True Posible values ; Posible values true, false, none

The format of the skip files (skipPath/skipPrefix/skipExtension) is  
Each path,prefix/extension on new line. If you need to coment a line insert :: infrom the line.  
Use the provided 3 files are exsample.  

***Versions***  
*folderTreeView v2.9*  
