try:
    import Tkinter as tk
    import Tkinter.messagebox
except ImportError:
    import tkinter as tk
    import tkinter.messagebox

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import sys

from bottle import Bottle, run, static_file, template, abort, ServerAdapter
import os
import threading
from datetime import datetime

app = Bottle()
ver = 3.2

cnfgFile = "config.ini"

skipPaths = []
skipPrefix = []
skipExtension = []
skipComents = "::"
serverRoot = ''
sortFlag = None
updateInterval = 0
docFolder = ''
titleFolder = ''

server = None

dicts = [{},{}]
selcetedDict = 0

@app.route('/favicon.ico')
def favicon():
    return static_file('download.png', root='./views')

@app.route('/static/<filepath:path>')
def static_content(filepath):
     return static_file(filepath, root='./views/static')

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
      dicts[selcetedDict] = path_to_dict(serverRoot)
      dicts[selcetedDict]['timestamp'] = genTimeStamp()
   return dicts[selcetedDict]

def updateDict():
    global selcetedDict
    didx = (selcetedDict + 1) % 2
    dicts[didx] = path_to_dict(serverRoot)
    dicts[didx]['timestamp'] = genTimeStamp()
    selcetedDict = didx
    threading.Timer(updateInterval, updateDict,[]).start()

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

def path_to_dict(path):
    baseName = os.path.basename(path)
    if(checkHidenFiles(baseName)):
        d = {'name': baseName}
        if os.path.isdir(path):
            d['type'] = "directory"
            itemsList = []
            folderContent = os.listdir(path) #Get the content of the folder
            if sortFlag is not None:
                folderContent.sort(reverse=sortFlag) #Sort the list in reverse order
            for x in folderContent:
                item = path_to_dict(os.path.join(path,x))
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

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        print("Shuting down.")
        self.server.shutdown()

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")
        #b1 = tk.Button(self, text="print to stdout", command=self.print_stdout)
        #b1.pack(in_=toolbar, side="left")
        self.text = ScrolledText(self, wrap="word")
        self.text.pack(side="top", fill="both", expand=True)
        self.text.tag_configure("stderr", foreground="#b22222", \
                                background="", font='TkFixedFont', \
                                selectbackground = "")
        self.text.tag_configure("stdout", foreground="", \
                                background="", font='TkFixedFont', \
                                selectbackground = "")

        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")

    #def print_stdout(self):
    #    '''Illustrate that using 'print' writes to stdout'''
    #    global S
    #    tk.messagebox.showinfo(str(S.is_alive()))
    #    #https://stackoverflow.com/questions/11282218/bottle-web-framework-how-to-stop
    #    #https://docs.python.org/3/library/threading.html#threading.Thread.daemon
    #    #https://www.section.io/engineering-education/how-to-perform-threading-timer-in-python/
    #    #print("this is stdout")
        
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.see('end')
        self.widget.configure(state="disabled")

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

def mainFunction():
    global serverRoot
    global sortFlag
    global updateInterval
    global docFolder
    global titleFolder
    if os.path.isfile(cnfgFile):
        import configparser
        print("Found " + cnfgFile)
        config = configparser.ConfigParser()
        config.read(cnfgFile)
        port = config['DEFAULT']['Port']
        host = config['DEFAULT']['ip']
        serverRoot = config['DEFAULT']['serverRoot']
        docFolder, titleFolder = os.path.split(serverRoot)
        cnfgSkipFile = config['DEFAULT']['skipPath']
        cnfgSkipPrefix = config['DEFAULT']['skipPrefix']
        cnfgSkipExtension = config['DEFAULT']['skipExtension']
        updateInterval = int(config['DEFAULT']['updateInterval'])
        sortFlagTxt = config['DEFAULT']['sortFlag']
        if sortFlagTxt.lower() == "true":
            sortFlag = True
        elif sortFlagTxt.lower() == "false":
            sortFlag = False
        else:
            sortFlag = None
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
        docFolder, titleFolder = os.path.split(serverRoot)

    ##
    if os.path.isfile(cnfgSkipFile):
        with open(cnfgSkipFile, 'r', encoding='utf-8') as infile:
            print("Loading " + cnfgSkipFile)
            global skipPaths
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
            global skipPrefix
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
            global skipExtension
            for line in infile:
                if not line.startswith(skipComents):
                    skipExtension.append(line.rstrip())
            skipExtension = list(filter(None, skipExtension))
    else:
        print("File not found " + cnfgSkipExtension)
        print("  Skiping skipExtension configuration")
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
    global server
    server = MyWSGIRefServer(host = host,\
                                  port = port)
    S = threading.Timer(0.5, app.run, kwargs={'server': server})
    S.start()
    ##run(app, host = host, port = port, debug=True)

app_Tk = ExampleApp()
app_Tk.after(20, mainFunction)
#def after(self, ms, func=None, *args):
"""Call function once after given time.

MS specifies the time in milliseconds. FUNC gives the
function which shall be called. Additional parameters
are given as parameters to the function call.  Return
identifier to cancel scheduling with after_cancel."""
def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        app_Tk.destroy()
        #global server
        #server.stop()
        
        #Perform harakiri
        pid = os.getpid()
        from signal import SIGTERM
        os.kill(pid, SIGTERM)

app_Tk.protocol("WM_DELETE_WINDOW", on_closing)
app_Tk.mainloop()
