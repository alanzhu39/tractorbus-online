var socket = io();
let userID;
const player_selections = [];
const myDrawer = new Drawer();

console.log('test log');

socket.on('connect', function() {
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

socket.on('game-data', (data) => {
  // TODO: import drawing functions
  myDrawer.setData(data);
  myDrawer.draw();
});

socket.on('game-start', () => {
  setInterval(queryData() {
    socket.emit('data-query', 'Asking for data');
  }, 17);
});

function testFunc() {
  socket.emit('test-event', 'this is a test');
}

function cardClick(index) {
  // TODO: create index detection, if index is already in selections remove it
  player_selections.push(index)
}

function playButton() {
  socket.emit('make-move', {'userID': userID,
                            'selection': player_selections});
}

function clearButton() {
  player_selections.length = 0;
}
