/*
* Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
*                Davide Sanvito <davide.sanvito@neclab.eu>
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

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

function matchesRegex(re, text) {
  var regex = new RegExp(re);
  if(regex.test(text)) {
      return true;
  } else {
      return false;
  }
}

function addMatch(){
  //TODO how to define non-exact matches? Like in P4?
  var match = document.getElementById("matchesList");
  var matchField = document.getElementById("matchField");
  var matchFieldText = matchField.options[matchField.selectedIndex].text;
  var matchValueText = document.getElementById("matchValue").value.trim();
  if (matchField.selectedIndex == 0) {
    alert("Please select a match field!")
    return;
  }
  if (matchValueText.length == 0) {
    alert("Please specify a non-empty match value!")
    return;
  }
  if (!matchesRegex("[0-9\.]+\&\&\&[0-9]+", matchValueText)) {
    alert("Invalid match value!")
    return;
  }
  var input = document.createElement("label");
  input.value = matchFieldText + " == " + matchValueText;
  input.innerHTML = matchFieldText + " == " + matchValueText;
  input.className = "matchDiv baseDiv";
  input.onclick = function() { this.remove(); };
  input.title = "Click to remove";
  match.appendChild(input);
  // clear match
  matchField.selectedIndex = 0;
  document.getElementById("matchValue").value = "";
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////

function addCondition(){
  //TODO valide input: strings are variables, numbers are constants
  var conditionOperator = document.getElementById("condOperator");
  var condOperand1Text = document.getElementById("condOperand1").value.trim();
  var condOperand2Text = document.getElementById("condOperand2").value.trim();
  if (conditionOperator.selectedIndex == 0) {
    alert("Please select an operator!")
    return;
  }
  if (condOperand1Text.length == 0) {
    alert("Please insert a non-empty operand 1!")
    return;
  }
  if (condOperand2Text.length == 0) {
    alert("Please insert a non-empty operand 2!")
    return;
  }
  if (!matchesRegex("[#@]{0,1}[0-9a-zA-Z_-]+", condOperand1Text)) {
    alert("Invalid operand1!")
    return;
  }
  if (!matchesRegex("[#@]{0,1}[0-9a-zA-Z_-]+", condOperand2Text)) {
    alert("Invalid operand2!")
    return;
  }

  var condition = document.getElementById("conditionsList");
  var conditionOperatorText = conditionOperator.options[conditionOperator.selectedIndex].text;
  var input = document.createElement("label");
  input.value = condOperand1Text + " " + conditionOperatorText + " " + condOperand2Text;
  input.innerHTML = escapeHtml(condOperand1Text + " " + conditionOperatorText + " " + condOperand2Text);
  input.className = "conditionDiv baseDiv";
  input.onclick = function() { this.remove(); };
  input.title = "Click to remove";
  condition.appendChild(input);
  // clear condition
  conditionOperator.selectedIndex = 0;
  document.getElementById("condOperand1").value = "";
  document.getElementById("condOperand2").value = "";
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////

function addUpdate(){
  //TODO valide input: strings are variables, numbers are constants
  var updateOperation = document.getElementById("updateOperation");
  var updateOutputText = document.getElementById("updateOutput").value.trim();
  var updateOperand1Text = document.getElementById("updateOperand1").value.trim();
  var updateOperand2Text = document.getElementById("updateOperand2").value.trim();
  if (updateOutputText.length == 0) {
    alert("Please insert a non-empty output!")
    return;
  }
  if (!matchesRegex("[#@]{0,1}[0-9a-zA-Z_-]+", updateOutputText)) {
    alert("Invalid output!")
    return;
  }

  if (updateOperand1Text.length == 0) {
    alert("Please insert a non-empty operand 1!")
    return;
  }
  if (!matchesRegex("[#@]{0,1}[0-9a-zA-Z_-]+", updateOperand1Text)) {
    alert("Invalid operand1!")
    return;
  }

  // update operand 2 is optional: if no operation is selected we admit an empty value
  if (updateOperation.selectedIndex == 0 && updateOperand2Text.length > 0) {
    alert("Please select an operator!");
    return;
  }
  if (updateOperation.selectedIndex > 0) {
    if (updateOperand2Text.length == 0) {
      alert("Please insert a non-empty operand 2!")
      return;
    }
    if (!matchesRegex("[#@]{0,1}[0-9a-zA-Z_-]+", updateOperand2Text)) {
      alert("Invalid operand2!")
      return;
    }
  }

  var condition = document.getElementById("updateList");
  var updateOperationText = updateOperation.options[updateOperation.selectedIndex].text;
  var input = document.createElement("label");
  if (updateOperation.selectedIndex == 0) {
    input.value = document.getElementById("updateOutput").value + " = " + updateOperand1Text;
    input.innerHTML = document.getElementById("updateOutput").value + " = " + updateOperand1Text;
  } else {
    input.value = document.getElementById("updateOutput").value + " = " + updateOperand1Text + " " + updateOperationText + " " + updateOperand2Text;
    input.innerHTML = document.getElementById("updateOutput").value + " = " + updateOperand1Text + " " + updateOperationText + " " + updateOperand2Text;
  }

  input.className = "updateDiv baseDiv";
  input.onclick = function() { this.remove(); };
  input.title = "Click to remove";
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
  var actionParamText = document.getElementById("actionParam").value.trim();
  var actionParamTextNum = actionParamText.split(',').length;

  var actionParamStr = actionText.match(/.*\((.*)\)/)[1];
  var actionParamNum = actionParamStr.split(',').length;
  if (actionParamStr.length == 0 && actionParamText.length > 0) {
    alert("The selected action do not expect any parameter!");
    return;
  }
  if (actionParamStr.length > 0 && actionParamNum == 1 && (actionParamText.length == 0 || actionParamTextNum > 1)) {
    alert("The selected action expects one parameter!");
    return;
  }
  if (actionParamStr.length > 0 && actionParamTextNum != actionParamNum) {
    alert("The selected action expects " + actionParamNum + " comma separated parameters!");
    return;
  }

  var input = document.createElement("label");
  input.value = document.getElementById("action").value + "(" + actionParamText + ")";
  input.innerHTML = document.getElementById("action").value + "(" + actionParamText + ")";
  input.className = "actionDiv baseDiv";
  input.onclick = function() { this.remove(); };
  input.title = "Click to remove";
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
      out.value += " ; ";
    }
  }

  out.value += " | ";

  children = document.getElementById("conditionsList").children;
  for (var i = 0; i < children.length; i++) {
    out.value += children[i].value;
    if (i < children.length - 1){
      out.value += " ; ";
    }
  }

  out.value += " | ";
  
  children = document.getElementById("updateList").children;
  for (var i = 0; i < children.length; i++) {
    out.value += children[i].value;
    if (i < children.length - 1){
      out.value += " ; ";
    }
  }

  out.value += " | ";

  children = document.getElementById("actionList").children;
  for (var i = 0; i < children.length; i++) {
    out.value += children[i].value;
    if (i < children.length - 1){
      out.value += " ; ";
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

function generateCfg(){
  saveBackup();

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/generateCfg", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.responseType = 'blob';
  xhr.onload = function () {
    var blob = xhr.response;
    var contentDispo = xhr.getResponseHeader('Content-Disposition');
    if (contentDispo != null) {
      // https://stackoverflow.com/a/23054920/
      var fileName = contentDispo.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)[1];
      saveBlob(blob, fileName);
    } else {
      alert("The EFSM includes invalid transitions!\nCheck the debug message");
    }
    document.getElementById("debug_msg").value = atob(xhr.getResponseHeader('debug_msg'));
  };
  xhr.send(localStorage['fsm']);
}

function generateCfgOnos(){
  saveBackup();
  var onos_ip = document.getElementById("onos_ip").value;
  var onos_port = document.getElementById("onos_port").value;
  var flwblz_dev_id = document.getElementById("flwblz_dev_id").value;
  var params = "onosIp="+onos_ip+"&onosPort="+onos_port+"&flowBlazeDevId="+flwblz_dev_id;

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/generateCfgOnos?"+params, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.responseType = 'blob';
  xhr.onload = function () {
    document.getElementById("debug_msg").value = atob(xhr.getResponseHeader('debug_msg'));
    if (xhr.getResponseHeader('gen_ok') == null || xhr.getResponseHeader('gen_ok') === 'False' ) {
      alert("The EFSM includes invalid transitions!\nCheck the debug message");
    } else if (xhr.getResponseHeader('onos_ok') == null || xhr.getResponseHeader('onos_ok') === 'False') {
      alert("Errors pushing to ONOS!\nCheck the debug message")
    } else {
      alert("Pushed to ONOS!")
    }
  };
  xhr.send(localStorage['fsm']);
}

function saveBlob(blob, fileName) {
  var a = document.createElement('a');
  a.href = window.URL.createObjectURL(blob);
  a.download = fileName;
  a.dispatchEvent(new MouseEvent('click'));
}

function loadSampleFSMrate(){
  localStorage.clear();
  localStorage['fsm'] = '{"nodes":[{"x":91,"y":164,"text":"0","isAcceptState":false},{"x":392,"y":176,"text":"1","isAcceptState":false},{"x":679,"y":247,"text":"2","isAcceptState":false}],"links":[{"type":"Link","nodeA":0,"nodeB":1,"text":"| | rate = @meta ; t_lim = @now + 5000000 | forward()","lineAngleAdjust":3.141592653589793,"parallelPart":0.7678759086685021,"perpendicularPart":-95.75499679381257},{"type":"SelfLink","node":1,"text":"| rate <= 800000 ; t_lim >= @now | rate = rate + @meta | forward()","anchorAngle":-1.3159402802923779},{"type":"SelfLink","node":1,"text":"| t_lim < @now | rate = @meta ; t_lim = @now + 5000000 | forward()","anchorAngle":2.0797860706936744},{"type":"Link","nodeA":1,"nodeB":2,"text":"| rate > 800000 ; t_lim >= @now | | drop() ","lineAngleAdjust":3.141592653589793,"parallelPart":0.7043226684819606,"perpendicularPart":-26.90542774619244},{"type":"SelfLink","node":2,"text":"| t_lim >= @now | | drop()","anchorAngle":1.4249710602599328},{"type":"Link","nodeA":2,"nodeB":1,"text":"| t_lim < @now | rate = @meta ; t_lim = @now + 5000000 | forward()","lineAngleAdjust":3.141592653589793,"parallelPart":0.3311863631163482,"perpendicularPart":-70.57964277427901}]}';
  location.reload();
}

function loadSampleFSMcount(){
  localStorage.clear();
  localStorage['fsm'] = '{"nodes":[{"x":118,"y":168,"text":"0","isAcceptState":false},{"x":331,"y":168,"text":"count","isAcceptState":false},{"x":594,"y":168,"text":"block","isAcceptState":false}],"links":[{"type":"Link","nodeA":0,"nodeB":1,"text":" |  | pkt = 1 | forward()","lineAngleAdjust":0,"parallelPart":0.5233644859813084,"perpendicularPart":-59},{"type":"Link","nodeA":1,"nodeB":2,"text":" | pkt >= 10 |  | drop()","lineAngleAdjust":3.141592653589793,"parallelPart":0.5295658538464503,"perpendicularPart":-58.19084654409617},{"type":"SelfLink","node":2,"text":" |  |  | drop()","anchorAngle":1.5707963267948966},{"type":"SelfLink","node":1,"text":" | pkt < 10 | pkt = pkt + 1 | forward()","anchorAngle":1.5707963267948966}]}';
  location.reload();
}

function loadFSM(){
  localStorage.clear();
  document.getElementById('fileinput').dispatchEvent(new MouseEvent('click'));
  //fileinput's onchange event have been registered in fsm.js's window.onload
}

function saveFSM(){
  var blob = new Blob([localStorage['fsm']], {type: 'text/json'});
  saveBlob(blob, 'FSM.json');
}

function loadFileIntoLocalStorage() {
  //https://stackoverflow.com/a/21446426
  var input, file, fr;

  if (typeof window.FileReader !== 'function') {
    alert("The file API isn't supported on this browser yet.");
    return;
  }

  input = document.getElementById('fileinput');
  if (!input) {
    alert("Um, couldn't find the fileinput element.");
  }
  else if (!input.files) {
    alert("This browser doesn't seem to support the `files` property of file inputs.");
  }
  else if (!input.files[0]) {
    alert("Please select a file before clicking 'Load'");
  }
  else {
    file = input.files[0];
    fr = new FileReader();
    fr.onload = receivedText;
    fr.readAsText(file);
  }

  function receivedText(e) {
    let lines = e.target.result;
    localStorage['fsm'] = lines;
    location.reload();
  }
}