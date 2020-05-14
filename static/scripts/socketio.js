document.addEventListener('DOMContentLoaded', () => {
  var socket = io();
  let userID;

  socket.on('connect', function() {
    socket.emit('connected', 'I\'m connected!');
  });

  socket.on('message', (data) => {
    console.log(`Message received: ${data}`);
  });

  socket.on('assign_id', (num_conns) => {
    if (!userID) {
      userID = num_conns;
    }
  })
});
