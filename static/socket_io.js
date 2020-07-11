var io = require('socket.io')(80);
include('"https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"');

      var socket = io.connect('http://' + document.domain + ':' + location.port);
      var session_id = "{{ session.get('session_id') }}";

      socket.on( 'connect', function() {
        socket.emit( 'my event', {
          data: 'User Connected'
        } );

        console.log('Creating game...');
        socket.emit('create', {
          data: '{{ g.session_id }}'
        });

        // message handler for the 'join_room' channel
        socket.on('join_room', function(msg) {
            console.log(msg);
        });

        var form = $( 'form' ).on( 'submit', function( e ) {
          e.preventDefault()
          let user_name = '{{ session.get("user_id") }}'
          let user_input = $( 'input.message' ).val()
          socket.emit( 'chat message', {
            user_name : user_name,
            message : user_input
          } )
          $( 'input.message' ).val( '' ).focus()
        } )
      } )


      socket.on( 'my response', function( msg ) {
        console.log( msg )
        console.log("breakpoint")
        if( typeof msg.user_name !== 'undefined' ) {
          $( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )
        } else if ( '{{ session.get('color') }}' !== msg['moved_piece']['team'] ) 
          {
          console.log( 'yayyyyy')
          socket.emit( 'board state', msg );
          var origin_row = msg['origin_cell'][0];
          var origin_col = msg['origin_cell'][1];
          var destination_row = msg['destination_cell'][0];
          var destination_col = msg['destination_cell'][1];
          console.log(msg);
          console.log(document.getElementById(destination_row).querySelector('#\\3' + destination_col + ' '));
          document.getElementById(destination_row).querySelector('#\\3' + destination_col + ' ').classList.add( msg['moved_piece']['team']);
          var offboard_origin = msg['origin_cell'].includes("");
          console.log(offboard_origin);
          if ( offboard_origin  === false) {
            console.log(msg['origin_cell'].includes(""));
            console.log('nooooooo');
            extractData(document.getElementById(origin_row).querySelector('#\\3' + origin_col + ' ').querySelector('.square'));
          }

          loadData(document.getElementById(destination_row).querySelector('#\\3' + destination_col + ' ').querySelector('.square'),payload="");
        }
      })
