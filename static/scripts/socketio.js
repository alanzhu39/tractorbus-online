var socket = io();
let userID;
console.log('test log');

socket.on('connect', function() {
  console.log('im connected');
  socket.emit('connected', 'I\'m connected!');
});

socket.on('message', (data) => {
  console.log(`Message received: ${data}`);
});

socket.on('assign_id', (numConns) => {
  if (typeof userID == "undefined") {
    userID = numConns;
  }
  console.log(numConns);
});

function testFunc() {
  socket.emit('test-event', 'this is a test');
}
