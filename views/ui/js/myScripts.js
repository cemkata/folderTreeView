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


function setFilefileIcons(jd){
   fileIcons = jd;
   fileIconsReady = true;
}

function fillTable(jd){
   let tableTxt = ""
   if (typeof jd.error === "string"){
       tableTxt+=`<div class="row">
      <div class="cell">
        <img src="`+fileIcons.blankIcon+`" alt="[FILE]">
      </div>
      <div class="cell">
        <b>Error:</b>  `+jd.error+`
      </div>
      <div class="cell"></div>
      <div class="cell"></div>
    </div>
    `;
      //$("#tableHeader").after(tableTxt);
      //return;
   }else{
       tableTxt+=`<div class="row">
          <div class="cell">
            <input type="checkbox" name="all" id="checkAllChBox"/>
          </div>
          <div class="cell">
            <img src="`+fileIcons.backIcon+`" alt="[PARENTDIR]">
          </div>
          <div onclick="openFolder(event, '`+ jd.perentfolder.replace(/([/'"])/g, "&quot;")+`', true)" class="cell">
            <a href="">Perent folder</a>
          </div>
          <div class="cell"></div>
          <div class="cell"></div>
        </div>
        `;

       for (i = 0; i < jd.folders.length;i++){
           tableTxt+=`<div class="row">
          <div class="cell">
            <input type="checkbox" name="`+jd.folders[i].name+`"/>
          </div>
          <div class="cell">
            <img src="`+fileIcons.folderIcon+`" alt="[FOLDER]">
          </div>
          <div onclick="openFolder(event, '`+ jd.folders[i].name.replace(/([/'"])/g, "&quot;") +`', false)" class="cell">
             <a href="">`+jd.folders[i].name+`</a>
          </div>
          <div class="cell">`+jd.folders[i].date+`</div>
          <div class="cell">`+jd.folders[i].size+`</div>
        </div>
        `;
           //$("#tableHeader").after(tableTxt);
       }

       for (i = 0; i < jd.files.length;i++){
           tableTxt+=`<div class="row">
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
           //$("#tableHeader").after(tableTxt);
       }
       folderContent = jd;
       filesReady = true;
   }
   $("#fileHolder").html(emptyTable);
   $("#indexOf").text("Index of " + subFolder);
   $('#blankIco').attr("src", fileIcons.blankIcon);
   $("#tableHeader").after(tableTxt);
 
   $('#checkAllChBox').click(function() {
       $('#fileHolder input[type=checkbox]').each(function() {
          if(this.name != "all"){
              this.checked = !this.checked
          }
       });
   });

}

function listFiles(){
    if(fileIconsReady == false){
       $.getJSON(rootPath + "/getFileImages", setFilefileIcons);
    }
    url = rootPath + subFolder + "?client=JS";
    filesReady = false;
    $.getJSON(url, fillTable);
}

function openFolder(evt, folderUrl, upFolder){
  evt.preventDefault();  
  if(upFolder == true){
    subFolder = "/";
  }
  if (folderUrl == ""){
     subFolder = "/";//*TODO returning back*/
  }else{
     //folderUrl = folderUrl.replace(/([/'"])/g, "'");
     // Bad fix but seems to work
     folderUrl = folderUrl.replace(/([/""])/g, "/");
     subFolder = subFolder + folderUrl + "/";
  }
  listFiles();
  history.pushState(null, null, rootPath + subFolder);
}

function openFolderCMD(evt, folderUrl, upFolder){
  showDialog = false;
  openFolder(evt, folderUrl, upFolder);
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
   }else if (fileNames.length > 0){
	   return true;
   }
}

function uploadFileCmd(){
   var msg = `<div id="fileHolderModal">`;
   
   msg +=`<form id="fileForm" action="`+rootPath+`/uploadFile" method="post" enctype="multipart/form-data">
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
      if(jd === "undefined"){
		  listFiles();
		  showInModalFilesTimer = setTimeout(fileMoveCopyCmd, 10); // check again in few seconds
		  return;
	  }
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
      <div onclick="openFolderCMD(event, '`+ jd.perentfolder.replace(/([/'"])/g, "&quot;") +`', true)" class="cell">
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
      <div onclick="openFolderCMD(event, '`+ jd.folders[i].name.replace(/([/'"])/g, "&quot;") +`', false)" class="cell">
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
    url = rootPath + "/fileCmd";
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
        url: rootPath+'/uploadFile',  
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

function addModalStuff(){
  modal = $("#modalDiv"); // Get the <span> element that closes the modal
  span = $("#modalDiv-span"); // When the user clicks on <span> (x), close the modal
  span.click(function() {
        toggleDialog();
        clearVars();
        return 1;
  });
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
