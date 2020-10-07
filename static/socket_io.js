// runs when user connects
function connect_socket(session_id,user_id) {
  // send websocket message re: connection
  socket.emit( 'my event', {
    data: 'User Connected'
  } );
  // listener on server creates new session 
  console.log('Creating game...');
  socket.emit('create', {
    data: session_id
  });

  // message handler for the 'join_room' channel
  socket.on('join_room', function(msg) {
      console.log(msg);
  });

  // establish input for sending chat messages
  // chat message listener on server handles emits
  var form = $( 'form' ).on( 'submit', function( e ) {
  e.preventDefault()
  let user_name = user_id
  let user_input = $( 'input.message' ).val()
  socket.emit( 'chat message', {
    user_name : user_name,
    message : user_input
  } )
  $( 'input.message' ).val( '' ).focus()
  } )
}


// main function for handling chats & board states
function handle_incoming_data(msg) {
  // check if response is chat message
  if ( typeof msg.user_name !== 'undefined' ) {
    $( 'div#msg_holder' ).append( '<div class="msg"><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' );
    scroll_chat("x");
  // otherwise handle as board state
  } else {
      // actions for both players when a board state is sent from back end
      if ( msg.game_over === true) { 
        modifyGrid('grid',modification='removeListeners');
          show_victory_screen(msg.responsible_team);
      } else {
      window.phase = msg['phase'];
      showPhase(window.phase);
      if ((window.phase != 'preparation') & (document.getElementById('chest').classList.contains('hidden') === false)) {
        toggle_element(document.getElementById('chest'));
      }
      }
      // handling of board states received by backend for opposing moves only
      // modifies front end based on change
      console.log(msg);
      if ( window.own_team !== msg['responsible_team'] ) {
        var origin_row = msg['origin_cell'][0];
        var origin_col = msg['origin_cell'][1];
        var destination_row = msg['destination_cell'][0];
        var destination_col = msg['destination_cell'][1];
        var team = msg['moved_piece']['color'];

        if ( team == window.own_team) {
          var payload = msg['moved_piece']['piece'];
        } else {
          var payload = "";
        }
  
        var offboard_origin = msg['origin_cell'].includes("");
        if ( offboard_origin  === false) {
          extractData(document.getElementById(origin_row).querySelector('#' + CSS.escape(origin_col)).querySelector('.square').querySelector('.content'));
        }

        loadData(document.getElementById(destination_row).querySelector('#' + CSS.escape(destination_col)).querySelector('.square').querySelector('.content'),payload=payload,
          team=team,sync_board=true);
        socket.emit( 'opposing board sync' );
              }
          }
}


// modify grid to highlight valid moves
function return_range(msg) {
  console.log(msg['phase']);
  if (window.phase === window.own_team) {
    modifyGrid('grid',modification='highlightSquares',movementRange=msg);
  }
}


// enact front-end changes for your own combats after getting result from server
function handle_own_combat_result(msg) {
  if (window.phase === window.own_team) {
    var destination_row = msg['destination_cell'][0];
    var destination_col = msg['destination_cell'][1];
    var winning_team = msg['moved_piece']['color'];
    if (winning_team === window.own_team) {
      var payload = msg['moved_piece']['piece'];
    } else {
      var payload = "";
    }


    loadData(document.getElementById(destination_row).querySelector('#' + CSS.escape(destination_col)).querySelector('.square').querySelector('.content'),
      payload=payload,team=winning_team,sync_board=true);
  }
}