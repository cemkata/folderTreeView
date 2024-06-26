var treeValues; //Json file generated by the server 

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		// Typical action to be performed when the document is ready:
		treeValues = JSON.parse(xhttp.responseText);
			//recursive function creating the tree menu
		addleaf(treeMenu, treeValues, "");
		//add onclick handler for each leaf of the tree
		//uses toggler counter
		for (let i = 0; i < toggler.length; i++) {
		  toggler[i].addEventListener("click", function() {
			this.parentElement.querySelector(".nested").classList.toggle("active");
			this.classList.toggle("caret-down");
		  });
		}
		//sortList();
	}
};
xhttp.open("GET", "/getFiles", true);
xhttp.send();

var toggler = document.getElementsByClassName("caret"); //Conter used when generating the tree menu Filled after addleaf call
var left = document.getElementById("textareawrapper");
var right = document.getElementById("iframewrapper");
var pdfView = document.getElementById('iframeResult');
var treeMenu = document.getElementById('treemenu'); //holder for the treeMenu
var m_pos; //mouse position


//resize the right pane
right.style.height = (parseInt(getComputedStyle(left, '').height)) + "px";

function addleaf(root, leaf, path){
	//Add tree menu
	var li = document.createElement("li");
	var span = document.createElement("span");
	span.appendChild(document.createTextNode(leaf.name));
	if(leaf.type=="directory"){
		span.setAttribute("class", "caret"); // added line
	}
	li.appendChild(span);

	if(leaf.type=="directory"){ //add branch
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
	}else{ //add leaf
		root.appendChild(li);
		root = root.children[root.children.length-1];
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

function resize(e){
	var dx = m_pos - e.x;
	m_pos = e.x;
	resize_el.style.marginLeft = (parseInt(getComputedStyle(resize_el, '').marginLeft) - dx) + "px";
	right.style.marginLeft = (parseInt(getComputedStyle(resize_el, '').marginLeft)) + "px";
	left.style.width = (parseInt(getComputedStyle(resize_el, '').marginLeft) - tempX.x * 0.033) + "px";;
}

//get the resize slider
var resize_el = document.getElementById("resize");
var cnthld_el = document.getElementById("contentholder");
resize_el.addEventListener("mousedown", function(e){
	m_pos = e.x;
	document.addEventListener("mousemove", resize, false);
	cnthld_el.addEventListener("mousemove", resize, false);
}, false);
document.addEventListener("mouseup", function(){
	document.removeEventListener("mousemove", resize, false);
	cnthld_el.removeEventListener("mousemove", resize, false);
}, false);
/**
tempX.x is procent from the body
0.10 = 10%	
0.25 = 25%
0.33 = 33%
0.50 = 50%
*/
var tempX={x: document.body.clientWidth*0.25};
m_pos = 0;
resize(tempX);