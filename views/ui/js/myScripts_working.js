var CPU, RAM, HDD, Details;
var CPUReady = RAMReady = HDDReady = DetailsReady = false;

var addHDDPartitonsTable = false;

var fileIcons;//No need for default value
var fileIconsReady = false;//No need ???
const rootPath = "/files";
var filesReady = false; //Added to cleanVals
var showDialog = true; //Added to cleanVals
var fileUpdate = true; //Added to cleanVals
var folderContent;

var sourceFolder = -1; //Added to cleanVals
var fileNames = []; //Added to cleanVals
var fileCMDName = 0; //Added to cleanVals

var url; //Added to cleanVals
var argument; //Added to cleanVals

var modal;//No need for default value it holds html elemnt
var span; //No need for default value it holds html elemnt
var showInModalFilesTimer; //timer for loading the files in the modal dive when moving/copping

var serviceStatusIcon;//No need for default value
var serviceStatusIconsReady = false;//No need ???

var emptyTable = `
    <div><p id="indexOf"></p></div>
    <div class="row header green">
    </div>
    <div class="row header green" id="tableHeader">
      <div class="cell"></div>
      <div class="cell"><img id="blankIco" src="" alt="[ICO]"></div>
      <div class="cell">Name</div>
      <div class="cell">Last modified</div>
      <div class="cell">Size</div>
    </div>
`;

const waitingAnimation =`<div id="modalBar" class="modal">
<div id="bar"></div>
</div>`;

var systemCMD = [['reboot', 'OS restart'],
                 ['shutdown', 'OS shutdown'],
                 ['restartWebServer', 'WebServer restart'],
                 ['stopWebServer', 'WebServer shutdown']]

var updateCharts = function(){
    if(CPUReady == true && RAMReady == true && HDDReady == true && DetailsReady == true){ // run when condition is met
        if(addHDDPartitonsTable == false){
            addHDDTable();
        }
        addCharts();
        addDetails();
    }
    else {
        setTimeout(updateCharts, 2000); // check again in a second
    }
}

function setCPU(jd){
    CPU = jd.cpuload;
    CPUReady = true;
}

function setRAM(jd){
    RAM = jd;
    RAMReady = true;
}

function setHDD(jd){
    HDD = jd;
    HDDReady = true;
}

function setDetails(jd){
    Details = jd;
    DetailsReady = true;
}

function refreshSystemInfo(){
    CPUReady = RAMReady = HDDReady = DetailsReady = false;
    $.getJSON("/getCpu", setCPU);
    $.getJSON("/getRam", setRAM);
    $.getJSON("/getHDD", setHDD);
    $.getJSON("/getDetails", setDetails);
    updateCharts();
}

function addDetails(){
        $('#swVersion').val(Details.osVersion.trim());
        $('#mdHostname').val(Details.hostname.trim());
        $('#systemUptime').val(Details.uptime.trim());
}

function addHDDTable(){
   addHDDPartitonsTable = true;
   var tableTxt = ""
   for (i = 0; i < HDD.partition.length;i++){
       tableTxt += `<b>`+HDD.partition[i].leter+`:</b><br><div id="hddGauge`+i+`"class="progressbar"><div></div></div>
       <label>Free `+HDD.partition[i].size.used+" from "+HDD.partition[i].size.total+`</label><br><br>`;
       $('#diskLoad').html(tableTxt);
   }
}

function addCharts(){
   ramTotal = parseFloat(RAM.total);
   ramFree = parseFloat(RAM.free);
   ramProCent = Math.round(ramFree/ramTotal * 10000) / 100;
   progressBar(CPU, $('#cpuGauge'));
   progressBar(ramProCent, $('#ramGauge'));
   for (i = 0; i < HDD.partition.length;i++){
               hddTotal = parseFloat(HDD.partition[i].size.total);
               hddFree = hddTotal - parseFloat(HDD.partition[i].size.used);
               hddProCent = Math.round(hddFree/hddTotal * 10000) / 100;
               progressBar(hddProCent, $('#hddGauge'+i));
   }
}

function setFilefileIcons(jd){
   fileIcons = jd;
   fileIconsReady = true;
}

function fillTable(jd){
   $('#blankIco').attr("src", fileIcons.blankIcon);
   if (typeof jd.error === "string"){
       tableTxt=`<div class="row">
      <div class="cell">
        <img src="`+fileIcons.blankIcon+`" alt="[FILE]">
      </div>
      <div class="cell">
        `+jd.error+`
      </div>
      <div class="cell"></div>
      <div class="cell"></div>
    </div>
    `;
      $("#tableHeader").after(tableTxt);
      return;
   }

   for (i = 0; i < jd.files.length;i++){
       tableTxt=`<div class="row">
      <div class="cell">
        <input type="checkbox" name="`+ jd.files[i].name +`"/>
      </div>
      <div class="cell">
        <img src="`+fileIcons.fileIcon+`" alt="[FILE]">
      </div>
      <div onclick="location.href='`+rootPath + subFolder + jd.files[i].name+`';" class="cell">
        <a href="`+rootPath + subFolder + jd.files[i].name+`">`+jd.files[i].name+`</a>
      </div>
      <div class="cell">`+jd.files[i].date+`</div>
      <div class="cell">`+jd.files[i].size+`</div>
    </div>
    `;
       $("#tableHeader").after(tableTxt);
   }
   for (i = 0; i < jd.folders.length;i++){
       tableTxt=`<div class="row">
      <div class="cell">
        <input type="checkbox" name="`+jd.folders[i].name+`"/>
      </div>
      <div class="cell">
        <img src="`+fileIcons.folderIcon+`" alt="[FOLDER]">
      </div>
      <div onclick="openFolder(event, '`+ jd.folders[i].name.replace(/([/'"])/g, "&quot;") +`')" class="cell">
         <a href="">`+jd.folders[i].name+`</a>
      </div>
      <div class="cell">`+jd.folders[i].date+`</div>
      <div class="cell">`+jd.folders[i].size+`</div>
    </div>
    `;
       $("#tableHeader").after(tableTxt);
   }
   tableTxt=`<div class="row">
      <div class="cell">
        <input type="checkbox" name="all" id="checkAllChBox"/>
      </div>
      <div class="cell">
        <img src="`+fileIcons.backIcon+`" alt="[PARENTDIR]">
      </div>
      <div onclick="upFolder(event, '`+ jd.perentfolder.replace(/([/'"])/g, "&quot;")+`')" class="cell">
        <a href="">Perent folder</a>
      </div>
      <div class="cell"></div>
      <div class="cell"></div>
    </div>
    `;
   $("#tableHeader").after(tableTxt);
 
   $('#checkAllChBox').click(function() {
       $('#fileHolder input[type=checkbox]').each(function() {
          if(this.name != "all"){
              this.checked = !this.checked
          }
       });
   });
   folderContent = jd;
   filesReady = true;
}

function listFiles(){
    $("#fileHolder").html(emptyTable);
    if(fileIconsReady == false){
       $.getJSON("/getFileImages", setFilefileIcons);
    }
    url = rootPath + subFolder + "?client=JS";
    filesReady = false;
    $.getJSON(url, fillTable);
    $("#indexOf").text("Index of " + subFolder);

}

function openFolder(evt, folderUrl){
  evt.preventDefault();  
  folderUrl = folderUrl.replace(/([/'"])/g, "'");
  subFolder = subFolder + folderUrl + "/";
  listFiles();
  history.pushState(null, null, rootPath + subFolder);
}

function upFolder(evt, folderUrl){
  evt.preventDefault();  
  if (folderUrl == ""){
     subFolder = "/";
  }else{
     folderUrl = folderUrl.replace(/([/'"])/g, "'");
     subFolder = "/" + folderUrl + "/";
  }
  listFiles();
  history.pushState(null, null, rootPath + subFolder);
}

function upFolderCMD(evt, folderUrl){
  showDialog = false;
  upFolder(evt, folderUrl);
  fileMoveCopyCmd();
}

function openFolderCMD(evt, folderUrl){
  showDialog = false;
  openFolder(evt, folderUrl);
  fileMoveCopyCmd();
}

function addDragAndDrop(){
    $('html').on({
                    dragover: function(e) {
                        e.stopPropagation();
                        e.preventDefault();
                        $('#uploadfile').removeClass('upload-area').addClass('upload-area-hovering');
                    },
                    dragleave: function(e) {
                        e.stopPropagation();
                        e.preventDefault();
                        $('#uploadfile').removeClass('upload-area-hovering').addClass('upload-area');
                    },
                    drop: function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                });
	
    $('#uploadfile').on({
                    dragenter: function(e) {
                        e.stopPropagation();
                        e.preventDefault();
                    },
                    dragleave: function(e) {
                        e.stopPropagation();
                        e.preventDefault();
                    },
                    drop: function(e) {
                        e.stopPropagation();
                        e.preventDefault();
                        var file = e.originalEvent.dataTransfer.files;
                        sendFile(file[0]);
                        $('#uploadfile').removeClass('upload-area-hovering').addClass('upload-area');
                    }
                });
}

function prepareFileCMD(cmd){
    fileCMDName = cmd;
    switch(cmd){
      case "delete":
        fileDeleteCmd();
        break;
      case "move":
      case "copy":
        fileMoveCopyCmd();
        break;
      case "rename":
        newNameCmd("file");
        break;
      case "folder":
        newNameCmd("folder");
        break;
      case "upload":
        uploadFileCmd();
        break;
  }
}

function getSelectedFiles(){
   if(sourceFolder == -1){
      fileNames = [];
      var selectedCount = 0; 
      $('#fileHolder input:checked').each(function() {
         fileNames.push(this.name);
         selectedCount++;
      });
      if (selectedCount == 0){
          return false;
      }else{
          sourceFolder = subFolder;
          return true;
      }
   }
}

function uploadFileCmd(){
   var msg = `<div id="fileHolderModal">`;
   
   msg +=`<form id="fileForm" action="/uploadFile" method="post" enctype="multipart/form-data">
  <h4>Select a file:<br/><br/><h4> 
  <a href="#" class ="myButtonDisabled" id="fileSelector">Select file for upload</a><br/>
  <input type="file" name="upload" id="fileSelectorInput" style="opacity:0;"/>
</form>`
   msg += `</div>`;
   dialog(msg, sendFile, clearVars);
   $("#fileSelector").click(function(e){
       e.preventDefault();
       $("#fileSelectorInput").trigger('click');
   });
}

function fileDeleteCmd(){
   if (getSelectedFiles() == false){
       return;
   }
   var msg = `<div id="fileHolderModal">`;
   msg +="<h4>Do you want to delte selected files?</h4>";
   msg += `</div>`;
   dialog(msg, sendFileCMD, clearVars);
}

function newNameCmd(name){
   if(name != 'folder'){
     if (getSelectedFiles() == false){
         return;
     }
   }else{
     sourceFolder = subFolder;
   }
   var msg = `<div id="fileHolderModal">`;
   msg +="<h4>Please enter the new "+name+" name and click yes.</h4><br><br>";
   msg +=`<input type="text" class="nameTextBox" id="renameTextBox" placeholder="New name" />`;
   msg += `</div>`;
   dialog(msg, sendFileCMD, clearVars);
}

function fileMoveCopyCmd(){
   var jd = folderContent;
   if (getSelectedFiles() == false){
       //clearTimeout(showInModalFilesTimer);
       return;
   }
   if(!filesReady){ //Wait until the file list is loaded
      showInModalFilesTimer = setTimeout(fileMoveCopyCmd, 10); // check again in a second
	  return;
   }
   var msg ="<h4>Do you want to " + fileCMDName +" selected files to "+subFolder+"?</h4>";
   msg += `<div id="fileHolderModal">`;
   msg += emptyTable.replace('blankIco', 'blankIcoModal');
   msg = msg.replace('indexOf','indexOfModal');
   msg += `<div class="row">
      <div class="cell"></div>
      <div class="cell">
        <img src="`+fileIcons.backIcon+`" alt="[PARENTDIR]">
      </div>
      <div onclick="upFolderCMD(event, '`+ jd.perentfolder.replace(/([/'"])/g, "&quot;") +`')" class="cell">
        Perent folder
      </div>
      <div class="cell"></div>
      <div class="cell"></div>
    </div>`;
    
    for (i = 0; i < jd.folders.length;i++){
        msg += `<div class="row">
      <div class="cell"></div>
      <div class="cell">
        <img src="`+fileIcons.folderIcon+`" alt="[FOLDER]">
      </div>
      <div onclick="openFolderCMD(event, '`+ jd.folders[i].name.replace(/([/'"])/g, "&quot;") +`')" class="cell">
         `+jd.folders[i].name+`
      </div>
      <div class="cell">`+jd.folders[i].date+`</div>
      <div class="cell">`+jd.folders[i].size+`</div>
    </div>`;
   }
    msg += `</div>`;
    if(showDialog){
      dialog(msg, sendFileCMD, clearVars);
      showDialog = false;
    }else{
      updateDialog(msg);
    }

    $('#blankIcoModal').attr("src", fileIcons.blankIcon);
    $("#indexOfModal").text("Index of " + subFolder);
}

function sendFileCMD(){
    switch(fileCMDName){
      case "delete":
      case "move":
      case "copy":
        var targetFolder = subFolder;
        break;
      case "rename":
      case "folder":
        var targetFolder = $('#renameTextBox').val();
        break;
  }
    $("body").append(waitingAnimation);
    $("#modalBar").css({ display: "block" });
    url = "/fileCmd";
    jsonFilenames = JSON.stringify(fileNames);
    argument = JSON.stringify({fileNames:jsonFilenames, sourceFolder: sourceFolder, targetFolder: targetFolder, fileCMD:fileCMDName});
    fileUpdate = false;
    postCMDArg();
}

function sendFile(inputFile){
    $("body").append(waitingAnimation);
    $("#modalBar").css({ display: "block" });

    var formData = new FormData();
    if (inputFile === undefined){
        formData.append('upload', $('input[type=file]')[0].files[0]);
    }else{
        formData.append('upload', inputFile);
    }

    formData.append('targetFolder', subFolder);

    $.ajax({
        url: '/uploadFile',  
        type: 'POST',
        data: formData,
        success: function (data) {
            $("#modalBar").remove();
            listFiles();
            clearVars();
        },
        error: function (jXHR, textStatus, errorThrown) {
              $("#modalBar").remove();
              listFiles();
              var msg = `<div id="fileHolderModal">`;
              msg +="Something went wrong.\n";
                msg +=errorThrown;
              msg += `</div>`;
              dialog(msg, passFunction, passFunction);
              clearVars();
        },
        cache: false,
        contentType: false,
        processData: false
    });
    $("form#fileForm").on("submit", function (e) {
        e.preventDefault();
    });

}

function getPage(evt, id){
    evt.preventDefault();  
    $.post("/getHtml",{
      id: id
    },
    function(response){
      id = this.data.split("=")[1];
      $("#main").html(response);
      history.pushState(null, null, "/" + templates[id]);
    }).fail(function(response) {
      $("#main").html(response.responseText);
    });
    var target = evt.target;
    document.title = target.textContent || target.innerText;
    //$("#footer").css({ position: "fixed" }); //durty workaround that the footer shows over the files content
    addHDDPartitonsTable = false;
}

function addModalStuff(){
  modal = $("#modalDiv"); // Get the <span> element that closes the modal
  span = $("#modalDiv-span"); // When the user clicks on <span> (x), close the modal
  span.click(function() {
        toggleDialog();
        clearVars();
        return 1;
  });
  /*modal.click(function() {
        toggleDialog();
        clearVars();
        return 1;
  });*/
}

function sysCmd(cmd){ 
    url = "/sysCmd";
    argument = systemCMD[cmd][0];
    var msg = "<h4>Do you want to continue with " + systemCMD[cmd][1] +"?</h4>";
    dialog(msg, postCMDArg, clearVars)
}

function postCMDArg(){
    $.post(url,{
      comand: argument
    }, function(response){
      var i=1;
    })
    .done(function(){
        if(fileUpdate == false){ //If the files tab is opened after the post is done we clear the waiting animation
                                //And load the file list again.
              $("#modalBar").remove();
              listFiles();
        }
        clearVars(); // <-- this doesnt work must be debuged
    })
      .fail(function(){
        if(fileUpdate == false){ //If the files tab is opened after the post is done we clear the waiting animation
                                //And load the file list again.
              $("#modalBar").remove();
              listFiles();
              var msg = `<div id="fileHolderModal">`;
              msg +="Something went wrong."
              msg += `</div>`;
              dialog(msg, passFunction, passFunction);
        }
        clearVars(); // <-- this doesnt work must be debuged
    })
      .always(function(){
      var i=1;
    });
}

function clearVars(){
    url = 0;
    argument = 0;
    showDialog = true;
    sourceFolder = -1;
    fileNames = [];
    fileUpdate = true;
    filesReady = false;
    fileCMDName = 0;
	clearTimeout(showInModalFilesTimer);
}

function setServices(jd){
    serviceStatusIconsReady = true;
    serviceStatusIcon = jd;
}

var putServices = function(jd){
    if(serviceStatusIconsReady == true){ // run when condition is met
       var msg = `<div class="table">`;
       for (i = 0; i < jd.length;i++){
          msg +=`<div class="row">
            <div class="cell"><label>`+jd[i][1]+`</label></div>
            <div class="cell"><img id="`+jd[i][0]+`" src="`+serviceStatusIcon.notconfigured+`" class="serviceIcon"></div>
            <div class="cell"><label><a href="#" onclick="serviceAction(event, this, '`+jd[i][0]+`', true)">Start</a></label></div>
            <div class="cell"><label><a href="#" onclick="serviceAction(event, this, '`+jd[i][0]+`', false)">Stop</a></label></div>
          </div>`;
       }
       msg +=`</div>`;
       $("#serviceTable").html(msg);
       $.getJSON("/cehckServices", updateServiceStatus);
    }
    else {
        setTimeout(putServices, 2000, jd); // check again in a second
    }
}

function updateServiceStatus(jd){
    for (i = 0; i < jd.length;i++){
          var icon;
          var startClass, stopClass;
          switch(jd[i][1]){
             case 1: icon = serviceStatusIcon.running;startClass = "myButtonDisabled";stopClass = "myButtonActive";break; //"running"
             case 0: icon = serviceStatusIcon.stopped;startClass = "myButtonActive";stopClass = "myButtonDisabled";break; //"stopped"
             case -1: icon = serviceStatusIcon.notconfigured;startClass = "myButtonDisabled";stopClass = "myButtonDisabled";break; //"notconfigured"
             case -2: icon = serviceStatusIcon.configured;startClass = "myButtonDisabled";stopClass = "myButtonDisabled";break; //"configured"
          }
          changeServiceState(jd[i][0], icon, startClass, stopClass);
    }
}

function refreshServiceStatus(){
    $.getJSON("/cehckServices", updateServiceStatus);
}

function serviceAction(evt, btn, serviceID, toggle){
    evt.preventDefault();
    if(btn.className == "myButtonActive"){
        if(toggle){
             var action = 'startService';
             var startClass = "myButtonDisabled";
             var stopClass = "myButtonActive";
        }else{
             var action = 'stopService';
             startClass = "myButtonActive";
             stopClass = "myButtonDisabled";
        }
        t = "/toggleService"+"?serviceID="+serviceID+"&serviceAction="+action;
        $.get("/toggleService"+"?serviceID="+serviceID+"&serviceAction="+action, function(result){
          var icon;
          switch(parseInt(result)){
             case 1: icon = serviceStatusIcon.running; break; //"running"
             case 0: icon = serviceStatusIcon.stopped; break; //"stopped"
          }
          changeServiceState(serviceID, icon, startClass, stopClass);
        });
    }
}

function changeServiceState(serviceID, newIcon, startClass, stopClass){
    var serviceIcon = $("#"+serviceID);
    serviceIcon.attr("src", newIcon);
    btnStart = serviceIcon.parent().next().find('a');
    btnStop = serviceIcon.parent().next().next().find('a');
    btnStart.attr("class", startClass);
    btnStop.attr("class", stopClass);
}

function getServices(){
    if(serviceStatusIconsReady == false){
         $.getJSON("/getStatusImages", setServices);
    }
    
    $.getJSON("/getServices", putServices);
}