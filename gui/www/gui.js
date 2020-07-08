function escapeHtml(text) {
  var map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };

  return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function addMatch(){
    var match = document.getElementById("matchesList");
    var matchField = document.getElementById("matchField");
    var matchFieldText = matchField.options[matchField.selectedIndex].text;
    if (matchField.selectedIndex == 0) {
      alert("Please select a match field!")
      return;
    }
    if (document.getElementById("matchValue").value == "") {
      alert("Please specify a match value!")
      return;
    }
    var input = document.createElement("label");
    input.value = matchFieldText + "==" + document.getElementById("matchValue").value;
    input.innerHTML = matchFieldText + "==" + document.getElementById("matchValue").value;
    input.className = "matchDiv";
    match.appendChild(input);
    // clear match
    matchField.selectedIndex = 0;
    document.getElementById("matchValue").value = "";
  }
           
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////

  function addCondition(){
    var conditionOperator = document.getElementById("condOperator");
    if (conditionOperator.selectedIndex == 0) {
      alert("Please select an operator!")
      return;
    }
    if (document.getElementById("condOperand1").value == "") {
      alert("Please insert operand 1!")
      return;
    }
    if (document.getElementById("condOperand2").value == "") {
      alert("Please insert operand 2!")
      return;
    }
    var condition = document.getElementById("conditionsList");
    var conditionOperatorText = conditionOperator.options[conditionOperator.selectedIndex].text;
    var input = document.createElement("label");
    input.value = document.getElementById("condOperand1").value + conditionOperatorText + document.getElementById("condOperand2").value;
    input.innerHTML = escapeHtml(document.getElementById("condOperand1").value + conditionOperatorText + document.getElementById("condOperand2").value);
    input.className = "conditionDiv";
    condition.appendChild(input);
    // clear condition
    conditionOperator.selectedIndex = 0;
    document.getElementById("condOperand1").value = "";
    document.getElementById("condOperand2").value = "";
  }
           
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////

  function addUpdate(){
    var updateOperation = document.getElementById("updateOperation");
    if (updateOperation.selectedIndex == 0) {
      alert("Please select an operator!"); //TODO potremmo ammetere vuoto solo se operando 2 è vuoto!
      return;
    }
    if (document.getElementById("updateOutput").value == "") {
      alert("Please insert output!")
      return;
    }
    if (document.getElementById("updateOperand1").value == "") {
      alert("Please insert operand 1!")
      return;
    }
    if (document.getElementById("updateOperand2").value == "") {
      alert("Please insert operand 2!")
      return;
    }
    var condition = document.getElementById("updateList");
    var updateOperationText = updateOperation.options[updateOperation.selectedIndex].text;
    var input = document.createElement("label");
    input.value = document.getElementById("updateOutput").value + "=" + document.getElementById("updateOperand1").value + updateOperationText + document.getElementById("updateOperand2").value;
    input.innerHTML = document.getElementById("updateOutput").value + "=" + document.getElementById("updateOperand1").value + updateOperationText + document.getElementById("updateOperand2").value;
    input.className = "updateDiv";
    condition.appendChild(input);
    // clear update
    updateOperation.selectedIndex = 0;
    document.getElementById("updateOutput").value = "";
    document.getElementById("updateOperand1").value = "";
    document.getElementById("updateOperand2").value = "";
  }
           
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////

  function setAction(){
    var action = document.getElementById("action");
    if (action.selectedIndex == 0) {
      alert("Please select an action!");
      return;
    }
    var actionList = document.getElementById("actionList");
    var actionText = action.options[action.selectedIndex].text;
    var input = document.createElement("label");
    input.value = document.getElementById("action").value; // + "(" + document.getElementById("actionParam").value + ")";
    input.innerHTML = document.getElementById("action").value; // + "(" + document.getElementById("actionParam").value + ")";
    input.className = "actionDiv";
    actionList.appendChild(input);
    // clear update
    action.selectedIndex = 0;
    document.getElementById("actionParam").value = "";
  }
           
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////

  function createTransitionString(){
    var children = document.getElementById("matchesList").children;
    var out = document.getElementById("out");
    out.value = "";
    for (var i = 0; i < children.length; i++) {
      out.value += children[i].value;
      if (i < children.length - 1){
        out.value += ";";
      }
    }

    out.value += "|";

    children = document.getElementById("conditionsList").children;
    for (var i = 0; i < children.length; i++) {
      out.value += children[i].value;
      if (i < children.length - 1){
        out.value += ";";
      }
    }

    out.value += "|";
    
    children = document.getElementById("updateList").children;
    for (var i = 0; i < children.length; i++) {
      out.value += children[i].value;
      if (i < children.length - 1){
        out.value += ";";
      }
    }

    out.value += "|";
    
    children = document.getElementById("actionList").children;
    for (var i = 0; i < children.length; i++) {
      out.value += children[i].value;
      if (i < children.length - 1){
        out.value += ";";
      }
    }
  }

function clearTransitionString(){
  var myNode = document.getElementById("matchesList");
  while (myNode.firstChild) {
      myNode.removeChild(myNode.firstChild);
  }
  myNode = document.getElementById("conditionsList");
  while (myNode.firstChild) {
      myNode.removeChild(myNode.firstChild);
  }
  myNode = document.getElementById("updateList");
  while (myNode.firstChild) {
      myNode.removeChild(myNode.firstChild);
  }
  myNode = document.getElementById("actionList");
  while (myNode.firstChild) {
      myNode.removeChild(myNode.firstChild);
  }
}

function generateP4(){
  saveBackup();

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/generateP4", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.responseType = 'blob';
  xhr.onload = function () {
    var blob = xhr.response;
    var contentDispo = xhr.getResponseHeader('Content-Disposition');
    // https://stackoverflow.com/a/23054920/
    var fileName = contentDispo.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)[1];
    saveBlob(blob, fileName);
  };
  xhr.send(localStorage['fsm']);
}
function saveBlob(blob, fileName) {
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = fileName;
    a.dispatchEvent(new MouseEvent('click'));
}

function loadSampleFSM(){
  localStorage.clear();
  localStorage['fsm'] = '{"nodes":[{"x":91,"y":164,"text":"0","isAcceptState":false},{"x":392,"y":176,"text":"1","isAcceptState":false},{"x":679,"y":247,"text":"2","isAcceptState":false}],"links":[{"type":"Link","nodeA":0,"nodeB":1,"text":"||rate=META+0;t_lim=NOW+5000000|forward","lineAngleAdjust":3.141592653589793,"parallelPart":0.7678759086685021,"perpendicularPart":-95.75499679381257},{"type":"SelfLink","node":1,"text":"|rate<=800000;t_lim>=NOW|rate=rate+META|forward","anchorAngle":-1.3159402802923779},{"type":"SelfLink","node":1,"text":"|t_lim<NOW|rate=META+0;t_lim=NOW+5000000|forward","anchorAngle":2.0797860706936744},{"type":"Link","nodeA":1,"nodeB":2,"text":"|rate>800000;t_lim>=NOW||_drop","lineAngleAdjust":3.141592653589793,"parallelPart":0.7043226684819606,"perpendicularPart":-26.90542774619244},{"type":"SelfLink","node":2,"text":"|t_lim>=NOW||_drop","anchorAngle":1.4249710602599328},{"type":"Link","nodeA":2,"nodeB":1,"text":"|t_lim<NOW|rate=META+0;t_lim=NOW+5000000|forward","lineAngleAdjust":3.141592653589793,"parallelPart":0.3311863631163482,"perpendicularPart":-70.57964277427901}]}';
  location.reload();
}