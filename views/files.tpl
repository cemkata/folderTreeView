<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Files</title>
    <link href="/favicon.ico" rel="icon" type="image/x-icon" />

    <script src="/ui/js/jquery-3.4.1.min.js" type="text/javascript"></script>
    <script src="/ui/js/myScripts.js" type="text/javascript"></script>
    <script src="/ui/js/dialog.js" type="text/javascript"></script> 
    <link rel="stylesheet" type="text/css" href="/ui/css/style.css" />
    <link rel="stylesheet" type="text/css" href="/ui/css/dialog.css" />
    <link rel='stylesheet' type="text/css" href='/ui/css/table.css' />
    <link rel='stylesheet' type="text/css" href="/ui/css/buttons.css" />
    <link rel='stylesheet' type="text/css" href="/ui/css/waitinganimation.css" />
    <link rel='stylesheet' type="text/css" href="/ui/css/fileUpload.css" />

</head>
<body>
  <div id="header">
    <nav class="menu">
      <ul class="menu__list">
      </ul>
    </nav>
  </div> <!-- End of header Area -->
    <!-- Content Area -->
    <div id="main">
	
            <div class="statusBar"><p class="label">Files operations</p></div>
            <div class="groupData">
<div id="container">
    <div id="fileHolder"></div>
    <div id="buttonHolder">
<br><br>
% for cmd in ['move', 'copy', 'delete', 'rename', 'folder']:
	% if cmd == "folder":
					<a href="#" onclick="prepareFileCMD('{{cmd}}')" id="fileOperations" class="myButtonActive">Create {{cmd.capitalize()}} </a><br/><div></div>
	% else:
					<a href="#" onclick="prepareFileCMD('{{cmd}}')" id="fileOperations" class="myButtonActive">{{cmd.capitalize()}} selected ...</a><br/><div></div>
	% end
% end

% for cmd in ['upload']:
<br><br>
            <div class="upload-area" onclick="prepareFileCMD('{{cmd}}')" id="uploadfile">
                <h1>Drag and Drop file here<br/>Or<br/>Click to select file</h1>
            </div>
    </div>
</div>
% end

            </div>
  <!-- The Modal -->
  <div id="modalDiv" class="modal">
    <!-- Modal content -->
    <div class="modal-content">
        <span id="modalDiv-span" class="close">&times;</span>
        <div id='title'></div>
        <p id="modal-text"></p>
        <div class="cd-popup-container">
                <p></p>
                <ul class="cd-buttons">
                    <li id='btnYes'>Yes</li>
                    <li id='btnNo'>No</li>
                </ul>
            </div> <!-- cd-popup-container -->
    </div>  
  </div>
      <script>
<%
 if defined('subFolder'):
   folderToBeListed = "/" + subFolder
 else:
   folderToBeListed = "/"
 end
%>
            var subFolder = '{{!folderToBeListed.replace("'", r"\'")}}';
            $(function() {listFiles();addModalStuff();addDragAndDrop();});
      </script>

      </div><!-- end div id="main"-->
    <div id="footer">
      <p align="right">CEMKATA ™</p>
    </div><!-- end id footer -->
</div><!-- end id body -->
</body>
    <!-- <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="-1"> -->
</html>