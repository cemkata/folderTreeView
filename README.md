# Simple folder Tree View
This will list the content of a folder and alow the viewing of selected file.
It need only python no other frameworks execpt [bottle framework](https://github.com/bottlepy/bottle).  

How to configure in config.ini  
- ***In DEFAULT section:***
- port - Port where the webserver will listen
- ip - Address where ther server will listen. 0.0.0.0 will listen on any v4 IP.
- serverRoot - Folder that will be listed
- skipPath - file containing the paths to be skipped when listing the folder
- skipPrefix - File with prefixes of files to be ignored. For exsample all file starting with .(dot).
- skipExtension - skipp files exnding with this extensions. Files that can not be visualised in browser (exe, rar, etc)
- updateInterval - how ofther the folder is scaned for updates:
	- 0 is disabled. Each reload of the page will scan the folder. Imidiate update but bad loading times
	- 1,2,3 ... is in munites (no minus (positive))
	- -1,-2,-4 ... in in hours (negative)
- sortFlag - Posible values true, false, none
- fileOrganaserFlag - Posible values true, false

- ***In section FILEORGANISER:***
- recycle_bin_enabled - File organiser should it delete the file or mode to hidden folder
	- 0 is disabled (Files are deleted)
	- 1 is enabled (Files are moved to the configured bellow recyclebin_folder)
- recyclebin_folder - Path where the Deleted file will be stored

- ***In section APPLOGER:***
- log2File -  Posible values true, false
- access_log - file for the access logs
- app_log - file with other application logs, if there is any

The format of the skip files (skipPath/skipPrefix/skipExtension) is  
Each path,prefix/extension on new line. If you need to coment a line insert :: infrom the line.  
Use the provided 3 files are exsample.  

You can start the folderTreeView2Tkinter.pyw as Desktop Tkinter application (Linux and MAC migth need additional packages).  
file_orginiser.py is a module for folderTreeView. The settings are included in config.ini.
To access the the file organiser hold Ctrl + Alt and click in the upper left corner of the page.
You can export the content of the folder as html just start export_folder_2_html.py, the out put file will be store under html_output(folder will be created if doesn't exist).

***Versions***  
*folderTreeView v3.7*  
*folderTreeView GUI v1.3*  
