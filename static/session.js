function extractData(target) {
target.classList.add("selected");
window.transfer_payload = target.innerHTML;
console.log(transfer_payload);
}

function loadData(target,payload = window.transfer_payload) {
target.innerHTML = payload;
var origin = document.getElementsByClassName("selected")[0]
var origin_coords = [origin.parentNode.parentNode.parentNode.id,origin.parentNode.parentNode.id];
var target_coords = [target.parentNode.parentNode.parentNode.id,target.parentNode.parentNode.id];
var team = "{{ session.get('color') }}";
target.classList.add(team);
console.log(payload);
origin.classList.remove("selected","blue","red");
origin.innerHTML = "";
socket.emit( 'board state', {
      origin_cell : origin_coords,
      destination_cell : target_coords,
      moved_piece : {'team':team,'piece':payload}
    });
console.log('transfer');
delete window.transfer_payload;
}

function handleData(evt) {
var clickedOn = evt.target;
if (typeof window.transfer_payload !== 'undefined') {
  loadData(clickedOn);
} else {
  extractData(clickedOn);
}}

function changeColor(evt){
var clickedOn= evt.target;
// for HTML
clickedOn.style.backgroundColor = '#f00';
}


var grid = document.getElementById("grid");
for (var i = 1, row; row = grid.rows[i]; i++) {
   //iterate through rows
   //rows would be accessed using the "row" variable assigned in the for loop
   console.log(i)
   for (var j = 1, col; col = row.cells[j]; j++) {
     //iterate through columns
     //columns would be accessed using the "col" variable assigned in the for loop
     col.querySelector('.square').addEventListener('click',handleData,false);
   }  
}
var chest = document.getElementById("chest");
for (var i = 0, row; row = chest.rows[i]; i++) {
   //iterate through rows
   //rows would be accessed using the "row" variable assigned in the for loop
   console.log(i)
   for (var j = 0, col; col = row.cells[j]; j++) {
     //iterate through columns
     //columns would be accessed using the "col" variable assigned in the for loop
     col.querySelector('.square').addEventListener('click',handleData,false);
   }  
}