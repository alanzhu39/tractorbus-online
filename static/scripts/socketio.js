var socket = io();
let userID;
const playerSelections = [];
const myDrawer;

console.log('test log');

socket.on('connect', function() {
  socket.emit('connected', 'I\'m connected!');
});

socket.on('message', (data) => {
  console.log(data);
});

socket.on('assign_id', (numConns) => {
  if (typeof userID == "undefined") {
    userID = numConns;
    myDrawer = new Drawer(userID, playerSelections);
  }
  console.log(numConns);
});

socket.on('game-data', (data) => {
  // TODO: import drawing functions
  myDrawer.setData(data);
  myDrawer.draw();
});

socket.on('game-start', () => {
  setInterval(() => { socket.emit('data-query', 'Asking for data'); }, 17);
});

function testFunc() {
  myDrawer.drawTurn();
}

function cardClick(index) {
  // TODO: create index detection, if index is already in selections remove it
  playerSelections.push(index)
}

function playButton() {
  socket.emit('make-move', {'userID': userID,
                            'selection': playerSelections});
}

function clearButton() {
  playerSelections.length = 0;
}
