var dialogState = false;
//show hide the modal div
function toggleDialog() {
  if (dialogState){	
    modal.css({ display: "none" });
  }else{
    modal.css({ display: "block" });
  }
  dialogState = !dialogState;
}

function updateDialog(message) {
    $('#title').html(message);
}

function dialog(message, yesCallback, noCallback) {
    $('#title').html(message);
    toggleDialog();
    //$("#modal-text").html(messeges);
    $('#btnYes').one('click', function(e){
        e.preventDefault();
        toggleDialog();
        yesCallback();
        return 1;
    });
    $('#btnNo').one('click', function(e){
        e.preventDefault();
        toggleDialog();
        noCallback();
        return 1;
    });
}

function passFunction() { var i = 0;}