<!DOCTYPE html>
<html lang="en-US"><head>
<title>{{title}}</title>
<meta name="viewport" content="width=device-width">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="200">
<meta property="og:image:height" content="200">
<link rel="stylesheet" type="text/css" href="/static/treemenu.css"/>
<!--[if lt IE 8]>
<style>
#textareacontainer, #iframecontainer {width:48%;}
#container {height:500px;}
#textarea, #iframe {width:90%;height:450px;}
#iframeResult {height:450px;}
.stack {display:none;}
</style>
<![endif]-->
<body>
<div class="trytopnav">
	  <div class="search-container">
		<!--<form action="/action_page.php">-->
		  <input type="search" placeholder="Search.." name="search" id="searchinput">
		  <button onclick="search()" id="gobutton"><i>GO</i></button>
		<!--</form>-->
	  </div>
</div>

<div id="shield" style="display: none;"></div>

<div id="mySidenav" class="sidenav">
  <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
</div>

<a href="javascript:void(0)" id="dragbar" style="width: 5px; top: 144px; left: 830px; height: 503px; cursor: col-resize;"></a>
<div id="container">
  <div id="textareacontainer" style="width: 15%;">
    <div id="textarea">
      <div id="textareawrapper"><ul id="treemenu"></ul></div>
    </div>
  </div>
  <div id="iframecontainer" style="width: 85%;">
    <div id="iframe">
      <div id="iframewrapper"><iframe frameborder="0" id="iframeResult" name="iframeResult" allowfullscreen="true"></iframe></div>
    </div>
  </div>
</div>
<script src="/static/treemenu.js"></script>
</body></html>

<!-- Version 2.3-->
<!-- © Copyright 2021, Angel Garabitov -->