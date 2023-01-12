if (window.addEventListener) {
	window.addEventListener("resize", browserResize);
} else if (window.attachEvent) {
	window.attachEvent("onresize", browserResize);
}
var xbeforeResize = window.innerWidth;
function browserResize() {
	var afterResize = window.innerWidth;
	if ((xbeforeResize < (970) && afterResize >= (970)) || (xbeforeResize >= (970) && afterResize < (970)) ||
		(xbeforeResize < (728) && afterResize >= (728)) || (xbeforeResize >= (728) && afterResize < (728)) ||
		(xbeforeResize < (468) && afterResize >= (468)) ||(xbeforeResize >= (468) && afterResize < (468))) {
		xbeforeResize = afterResize;
	}
	if (window.screen.availWidth <= 768) {
		restack(window.innerHeight > window.innerWidth);
	}
	fixDragBtn();
}

var currentStack=true;
if ((window.screen.availWidth <= 768 && window.innerHeight > window.innerWidth) || "" == " horizontal") {restack(true);}
function restack(horizontal) {
	var tc, ic, t, i, c, f, d, height, flt, width;
	tc = document.getElementById("textareacontainer");
	ic = document.getElementById("iframecontainer");
	t = document.getElementById("textarea");
	i = document.getElementById("iframe");
	c = document.getElementById("container");
	tc.className = tc.className.replace("horizontal", "");
	ic.className = ic.className.replace("horizontal", "");
	t.className = t.className.replace("horizontal", "");
	i.className = i.className.replace("horizontal", "");
	c.className = c.className.replace("horizontal", "");
	stack = "";
	if (horizontal) {
		tc.className = tc.className + " horizontal";
		ic.className = ic.className + " horizontal";
		t.className = t.className + " horizontal";
		i.className = i.className + " horizontal";
		c.className = c.className + " horizontal";

		stack = " horizontal";
		document.getElementById("textareacontainer").style.height = "50%";
		document.getElementById("iframecontainer").style.height = "50%";
		document.getElementById("textareacontainer").style.width = "100%";
		document.getElementById("iframecontainer").style.width = "100%";
		currentStack=false;
	} else {
		document.getElementById("textareacontainer").style.height = "100%";
		document.getElementById("iframecontainer").style.height = "100%";
		document.getElementById("textareacontainer").style.width = "50%";
		document.getElementById("iframecontainer").style.width = "50%";
		currentStack=true;
	}
	fixDragBtn();
}

var dragging = false;
var stack;
function fixDragBtn() {
  var textareawidth, leftpadding, dragleft, containertop, buttonwidth
  var containertop = Number(w3_getStyleValue(document.getElementById("container"), "top").replace("px", ""));
  if (stack != " horizontal") {
	document.getElementById("dragbar").style.width = "5px";
	textareasize = Number(w3_getStyleValue(document.getElementById("textareawrapper"), "width").replace("px", ""));
	leftpadding = Number(w3_getStyleValue(document.getElementById("textarea"), "padding-left").replace("px", ""));
	buttonwidth = Number(w3_getStyleValue(document.getElementById("dragbar"), "width").replace("px", ""));
	textareaheight = w3_getStyleValue(document.getElementById("textareawrapper"), "height");
	dragleft = textareasize + leftpadding + (leftpadding / 2) - (buttonwidth / 2);
	document.getElementById("dragbar").style.top = containertop + "px";
	document.getElementById("dragbar").style.left = dragleft + "px";
	document.getElementById("dragbar").style.height = textareaheight;
	document.getElementById("dragbar").style.cursor = "col-resize";

  } else {
	document.getElementById("dragbar").style.height = "5px";
	if (window.getComputedStyle) {
		textareawidth = window.getComputedStyle(document.getElementById("textareawrapper"),null).getPropertyValue("height");
		textareaheight = window.getComputedStyle(document.getElementById("textareawrapper"),null).getPropertyValue("width");
		leftpadding = window.getComputedStyle(document.getElementById("textarea"),null).getPropertyValue("padding-top");
		buttonwidth = window.getComputedStyle(document.getElementById("dragbar"),null).getPropertyValue("height");
	} else {
		dragleft = document.getElementById("textareawrapper").currentStyle["width"];
	}
	textareawidth = Number(textareawidth.replace("px", ""));
	leftpadding = Number(leftpadding .replace("px", ""));
	buttonwidth = Number(buttonwidth .replace("px", ""));
	dragleft = containertop + textareawidth + leftpadding + (leftpadding / 2);
	document.getElementById("dragbar").style.top = dragleft + "px";
	document.getElementById("dragbar").style.left = "5px";
	document.getElementById("dragbar").style.width = textareaheight;
	document.getElementById("dragbar").style.cursor = "row-resize";
  }
}
function dragstart(e) {
  e.preventDefault();
  dragging = true;
}
function dragmove(e) {
  if (dragging) 
  {
	document.getElementById("shield").style.display = "block";
	if (stack != " horizontal") {
	  var percentage = (e.pageX / window.innerWidth) * 100;
	  if (percentage > 15 && percentage < 75) {
		var mainPercentage = 100-percentage;
		document.getElementById("textareacontainer").style.width = percentage + "%";
		document.getElementById("iframecontainer").style.width = mainPercentage + "%";
		fixDragBtn();
	  }
	} else {
	  var containertop = Number(w3_getStyleValue(document.getElementById("container"), "top").replace("px", ""));
	  var percentage = ((e.pageY - containertop + 20) / (window.innerHeight - containertop + 20)) * 100;
	  if (percentage > 15 && percentage < 75) {
		var mainPercentage = 100-percentage;
		document.getElementById("textareacontainer").style.height = percentage + "%";
		document.getElementById("iframecontainer").style.height = mainPercentage + "%";
		fixDragBtn();
	  }
	}
  }
}
function dragend() {
  document.getElementById("shield").style.display = "none";
  dragging = false;
}
if (window.addEventListener) {
  document.getElementById("dragbar").addEventListener("mousedown", function(e) {dragstart(e);});
  document.getElementById("dragbar").addEventListener("touchstart", function(e) {dragstart(e);});
  window.addEventListener("mousemove", function(e) {dragmove(e);});
  window.addEventListener("touchmove", function(e) {dragmove(e);});
  window.addEventListener("mouseup", dragend);
  window.addEventListener("touchend", dragend);
}

function w3_getStyleValue(elmnt,style) {
	if (window.getComputedStyle) {
		return window.getComputedStyle(elmnt,null).getPropertyValue(style);
	} else {
		return elmnt.currentStyle[style];
	}
}

browserResize();

var treeValues; //Json file generated by the server 

function iniTree(){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			// Typical action to be performed when the document is ready:
			treeValues = JSON.parse(xhttp.responseText);
			treeMenu.innerHTML = '';
			//recursive function creating the tree menu
			addleaf(treeMenu, treeValues, "");
			//add onclick handler for each leaf of the tree
			//uses toggler counter
			for (let i = 1; i < toggler.length; i++) {
			  toggler[i].addEventListener("click", function() {
				this.parentElement.querySelector(".nested").classList.toggle("active");
				this.classList.toggle("caret-down");
			  });
			}
			//Open the tree root
			toggler[0].parentElement.querySelector(".nested").classList.toggle("active");
			toggler[0].classList.toggle("caret-down");
			toggler[0].title="Updated at " + treeValues.timestamp + "\nClick to refresh"; //add the timestamp to the tree
			toggler[0].addEventListener("click", iniTree);
			pdfView.src = "./getHelp";
		}
	};
	xhttp.open("GET", "/getFiles", true);
	xhttp.send();
}

var toggler = document.getElementsByClassName("caret"); //Conter used when generating the tree menu Filled after addleaf call
var left = document.getElementById("textareawrapper");
var right = document.getElementById("iframewrapper");
var pdfView = document.getElementById('iframeResult');
var treeMenu = document.getElementById('treemenu'); //holder for the treeMenu
var m_pos; //mouse position
var searchResultsHolder = document.getElementById("mySidenav")

iniTree();

//resize the right pane
//right.style.height = (parseInt(getComputedStyle(left, '').height)) + "px";

function addleaf(root, leaf, path){
	//Add tree menu
	var li = document.createElement("li");
	var span = document.createElement("span");
	span.appendChild(document.createTextNode(leaf.name));
	span.setAttribute("class", "menuleaf");
	if(leaf.type=="directory"){
		//span.setAttribute("class", "caret"); // added line
		span.className += " " + "caret"; // added line
	}else{
		span.title=leaf.name;
	}
	li.appendChild(span);

	if(leaf.type=="directory"){ //add branch (folder)
		var ul = document.createElement("ul");
		ul.setAttribute("class", "nested");
		if(root.id == "treemenu"){
			root.insertBefore(li, root.firstChild);
			root = root.firstChild;
		}else if(root.firstChild==null){
			root.insertBefore(li, root.firstChild);
			root = root.firstChild;
		}else if(root.firstChild.firstChild.className == "caret"){
			for(let i = 0; i < root.children.length; i++){
				if(root.children[i].children[0].className != "caret"){
					root.insertBefore(li, root.children[i]);
					root = root.children[i];
					break;
				}
			}
		}else{
			root.insertBefore(li, root.firstChild);
			root = root.firstChild;
		}

		root.appendChild(ul);
		if(leaf.children.length != 0){
			for(let i = 0; i < leaf.children.length; i++){
				addleaf(ul, leaf.children[i], path + "/" + leaf.name);
			}
		}
	}else{ //add leaf (file)
		root.appendChild(li);
		li.filePath = path + "/" + leaf.name;
		li.addEventListener("click", function() {
			pdfView.src = this.filePath;
			templist = treeMenu.getElementsByClassName("selected");
			for(let i = 0; i < templist.length; i++){
				templist[i].classList.remove("selected");
			}
			this.className = "selected";
		});
	}
}

var searchField = document.getElementById("searchinput");
searchField.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) { // 13 is the value for enter
   event.preventDefault();
   document.getElementById("gobutton").click();
  }
});

function search(){
	var variable = searchField.value;
	if (variable === ""){return} //if the search text is empty exit
	var expression = `.*${variable}.*`;
	var re = new RegExp(expression, 'i');
	// ^i = Ignore case flag for RegExp
	searchResult = searchInJSON(re, treeValues);

	//Clear the result holder
	links = searchResultsHolder.getElementsByTagName('a');
	totalNumberOfLinks = links.length; //Length chenges on each iteration and we store the array length 
	for(let i = 1; i < totalNumberOfLinks; i++){
		links[1].remove(); //remove the second link. First is the close button
	}

	//Fill the result holder
	for(let i = 0; i < searchResult.length; i++){
		var a = document.createElement('a');
		a.setAttribute('href',"#");
		let tmp = searchResult[i].split('/');
		a.innerHTML = tmp[tmp.length-1];
		a.addEventListener("click", function() {
			pdfView.src = treeValues.name + "/" + searchResult[i];
			foldTree();
			unselectLeaf();
			openLeaf(searchResult[i]);
		});
		searchResultsHolder.appendChild(a);
	}
	openNav();
}

//var variable = 'foo';
//var expression = `.*${variable}.*`;
//var re = new RegExp(expression, 'g');
//re.test('fdjklsffoodjkslfd')   // true
//re.test('fdjklsfdjkslfd')   // false

function searchInJSON(re, jsonContainer){
	var result = [];
	for(let i = 0; i < jsonContainer.children.length; i++){
		if(jsonContainer.children[i].type=="file"){
			if (re.test(jsonContainer.children[i].name)) {
				result.push(jsonContainer.children[i].name)
				//console.log(jsonContainer.children[i].name)
			}
		}else{
			value = searchInJSON(re, jsonContainer.children[i]);
			if(value){
				if(value.length > 0){
					for(let k = 0; k < value.length; k++){
						result.push(jsonContainer.children[i].name + '/' + value[k]);
					}
				}else{
					result.push(jsonContainer.children[i].name + '/' + value);
				}
			}
		}
	}
	if(result.length != 0){
		return result;
	}else{
		return false;
	}
}


document.getElementById('searchinput').addEventListener('input', (e) => {
	if(e.currentTarget.value == "") {
		//alert("You either clicked the X or you searched for nothing.");
		closeNav();
	}
	/*else {
		//alert("You searched for " + input.value);
		console.log(`Input value: "${e.currentTarget.value}"`);
	}*/
})

/* Set the width of the side navigation to 250px */
function openNav() {
  //searchResultsHolder.style.width = "250px";
  if(currentStack){
		searchResultsHolder.style.width = "25%";
  }else{
		searchResultsHolder.style.width = "100%";
  }
}

/* Set the width of the side navigation to 0 */
function closeNav() {
  searchResultsHolder.style.width = "0";
  searchField.value = "";
}

function foldTree(){
	x = document.querySelectorAll('.caret-down');
	y = document.querySelectorAll('.active');

	for(let i = 1; i< x.length; i++){
		x[i].classList.toggle("caret-down");
	/*}
	for(let i = 1; i< y.length; i++){*/
		y[i].classList.toggle("active");
	}
}

function unselectLeaf(){
	z = document.querySelectorAll('.selected');
	for(let i = 0; i< z.length; i++){
		z[i].classList.toggle("selected");
	}
}

function openLeaf(inString){
	var tmpStrings = inString.split("/");
	//var exitFlag = true;
	var j = 0;
	var curentLeaf = treeMenu.childNodes[0].children[1].children;
	while(j != tmpStrings.length){
	/*while(exitFlag){
		if(j == tmpStrings.length){
			exitFlag = false
			continue;
		}*/
		for(let i = 0; i<curentLeaf.length; i++){
			if(curentLeaf[i].children[0].textContent === tmpStrings[j]){
				try {
					curentLeaf[i].children[1].classList.toggle("active");
					curentLeaf[i].children[0].classList.toggle("caret-down");
					curentLeaf = curentLeaf[i].children[1].children;
				} catch (exceptionVar) {
					curentLeaf[i].children[0].classList.toggle("selected");
				}finally {
					break;
				}
			}
		}
		j++;
	}
}

file_organaser_url = "./files/"

document.getElementById("logo").addEventListener("click", function(event) {
   /*if(event.ctrlKey)
      console.log('ctrl');
   if(event.altKey)
      console.log('alt');*/
  if(event.ctrlKey && event.altKey){
	  window.open(file_organaser_url, '_blank').focus();
  }
});

console.log("treemenu version 3.3")