// show victory overlay if game is over
function show_victory_screen(winner, return_link) {
  var winner = winner;
  winner = winner.charAt(0).toUpperCase() + winner.slice(1);
  var game_over_div = document.createElement('div');
  game_over_div.classList.add('popup');
  var inner_message_div = document.createElement('div');
  inner_message_div.classList.add('popup_text')
  game_over_div.appendChild(inner_message_div);
  inner_message_div.innerHTML = winner + ' wins!<br><a class="popup_link" href=' + return_link + '>Return to main menu</a>';
  document.getElementById('board_container').appendChild(game_over_div);
}

// determine which message to show user about current phase
function showPhase(phase) {
var phase_div = document.getElementById("phase");
if (window.phase === 'preparation') {
  phase_div.innerHTML = "<h3>Set Your Pieces</h3>";
}
else if (window.phase === own_team) {
  phase_div.innerHTML = "<h3>Your Turn</h3>";
}
else if (window.phase !== "game_over") {
  phase_div.innerHTML = "<h3>Opponent's Turn</h3>";
}
}


// hide or unhide element in html
function toggle_element(ele) {
  if (ele.classList.contains('hidden') === true) {
    ele.classList.add('fullscreen');
    ele.classList.remove('hidden');
  } else {
    ele.classList.add('hidden');
    ele.classList.remove('fullscreen');
  }
  scroll_chat("x");
}


// get height of element, scroll to bottom...used for chat box 
function scroll_chat(x) {
  var height = 0;
  $('div.msg').each(function(i, value){
      height += parseInt($(this).height()) * 200;
  });

  height += '';

  $('div#msg_holder').animate({scrollTop: height});
}


// functions for board interactions

// select square to move in UI, store value for transfer
function extractData(target) {
  target.classList.add("selected");
  window.transfer_payload = target.innerHTML.trim();
  }


// transfer data to selected destination in UI
function loadData(target,payload = window.transfer_payload,team=own_team,sync_board=false) {
var origin = document.getElementsByClassName("selected")[0]
if ( origin !== undefined ) {
  var origin_coords = [origin.parentNode.parentNode.parentNode.id,origin.parentNode.parentNode.id];
  origin.classList.remove("selected","blue","red");
  origin.classList.add('empty');
  origin.innerHTML = "";
};

var target_coords = [target.parentNode.parentNode.parentNode.id,target.parentNode.parentNode.id];
if (target.classList.contains('empty') || sync_board==true) {
  target.innerHTML = payload;
  target.classList.remove('empty','blue','red');
  target.classList.add(team);    
} 

delete window.transfer_payload;

return {
      origin_cell : origin_coords,
      destination_cell : target_coords,
      moved_piece : {'color':team,'piece':payload},
      phase : window.phase,
      responsible_team : team
    };
}


// return message for invalid moves in handleData()
function setMessage(message) {
  document.getElementById("invalid_move_message").innerHTML = message;
}

 // used to make one of several changes to grid tables, iterates through squares
function modifyGrid(table,modification=undefined,movementRange=undefined) {
    var grid = document.getElementById(table);

    if (table == 'grid') {
      rowStart = 1;
    } else {
      rowStart = 0;
    }

  if (modification == 'addListeners') {
    function makeModification(square,movementRange) {
      square.addEventListener('click',handleData,false);
      if (square.querySelector('.content').classList.contains('blue') === false && square.querySelector('.content').classList.contains('red') === false && square.querySelector('.content').classList.contains('water') === false) {square.querySelector('.content').classList.add('empty');}
  }
  }
  else if (modification == 'removeListeners') {
    function makeModification(square,movementRage) {
      square.removeEventListener('click',handleData,false);
    }
  }
  else if (modification == 'highlightSquares') {
    function makeModification(square,movementRange) {
      if (window.phase == 'preparation') {
        if (own_team == 'blue') {
          if (i > 4) {square.querySelector('.content').classList.add('out_of_range');}
        }
        else if (own_team == 'red') {
          if (i < 7) {square.querySelector('.content').classList.add('out_of_range');}
        }
      } 
      else if (window.phase == own_team) {
        if (movementRange !== undefined) {
          console.log('change me');
          if (movementRange[i] == undefined || movementRange[i].includes(j) == false) {
            square.querySelector('.content').classList.add('out_of_range');
          }
        }
      }
    }
  } else if (modification == 'clearHighlighting') {
    function makeModification(square,movementRange) {
      square.querySelector('.content').classList.remove('out_of_range');
    }
  }

  for (var i = rowStart, row; row = grid.rows[i]; i++) {
    // iterate through rows
    // rows would be accessed using the "row" variable assigned in the for loop
    for (var j = rowStart, col; col = row.cells[j]; j++) {
      // iterate through columns
      // columns would be accessed using the "col" variable assigned in the for loop
      makeModification(col.querySelector('.square'),movementRange);
    }  
  }
}

function handleData(evt) {
  var team = window.own_team;
  var clickedOn = evt.target;

  // check if existing payload is in browser
  if (typeof window.transfer_payload !== 'undefined') {
    // check if user is trying to move piece to same square
    if (clickedOn.classList.contains('selected') === false) {
          // check if user is trying to move where they already have another piece
          if (clickedOn.classList.contains(team) === false) {
            // check if user is trying to move to the water
            if (clickedOn.classList.contains('water') === false) {
              //send new board state to back end, render changes in client
              if (clickedOn.classList.contains('out_of_range') === false) {
                socket.emit( 'board state', loadData(clickedOn) );
                modifyGrid('grid',modification='clearHighlighting');
                return false;
              }
            } else {
                setMessage('pieces don\'t float!');
                setTimeout(setMessage, 2000,'<br>');                  
            }
        } else {
              setMessage('you already have a piece there');
              setTimeout(setMessage, 2000,'<br>');
        }
      }
    // if move is invalid, get selected grid square, and remove class
    document.getElementsByClassName("selected")[0].classList.remove("selected");
    delete window.transfer_payload;
    modifyGrid('grid',modification='clearHighlighting');
    // if payload does not already exist & square is controlled by own team, extract from grid square
  } 
  else if (clickedOn.classList.contains(team) && (window.phase === team || window.phase === "preparation")) {
    extractData(clickedOn);
    if (clickedOn.classList.contains(team) && window.phase === team) {
         var selected = document.getElementsByClassName("selected")[0];
         if ( selected !== undefined ) {
          var selected_coords = [selected.parentNode.parentNode.parentNode.id,selected.parentNode.parentNode.id];
          window.transfer_payload = selected.innerHTML.trim();
          socket.emit('get range', { 'coordinates': selected_coords, 'color': window.own_team });
      }
    }
    modifyGrid('grid',modification='highlightSquares');
  }
}