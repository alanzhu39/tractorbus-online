var socket = io();
let userID;
const playerSelections = [];
const myDrawer = new Drawer(playerSelections);

socket.on('connect', function() {
  socket.emit('connected', 'I\'m connected!');
});

socket.on('message', (data) => {
  console.log(data);
});

socket.on('assign_id', (numConns) => {
  if (typeof userID == "undefined") {
    userID = numConns;
    myDrawer.setID(userID);
  }
  console.log(numConns);
});

socket.on('game-data', (data) => {
  myDrawer.setData(data);
  myDrawer.draw();
});

socket.on('game-start', (data) => {
  setTimeout(() => { socket.emit('data-query', 'Asking for data'); }, 3000);
});

socket.on('test-event', (data) => {
  console.log(data);
});

function testFunc() {
  const testData = {0: [['2C','2D','2H','2S','3C','3D','3H','3S','4C','4D','4H','4S',
      '5C','5D','5H','5S','6C','6D','6H','6S','7C','7D','7H','7S','8C'], ['8D', '8H']],
                    1: [['2C','2D','2H','2S','3C','3D','3H','3S','4C','4D','4H','4S',
      '5C','5D','5H','5S','6C','6D','6H','6S','7C','7D','7H','7S','8C'], ['8D', '8H']],
                    2: [['2C','2D','2H','2S','3C','3D','3H','3S','4C','4D','4H','4S',
      '5C','5D','5H','5S','6C','6D','6H','6S','7C','7D','7H','7S','8C'], ['8D', '8H']],
                    3: [['2C','2D','2H','2S','3C','3D','3H','3S','4C','4D','4H','4S',
      '5C','5D','5H','5S','6C','6D','6H','6S','7C','7D','7H','7S','8C'], ['8D', '8H']],
                    'clear': true, 'di_pai': true, 'game_start': true, 'attacker_points': 25,
                    'trump_suit': 'test suit', 'current_player': 1};
  myDrawer.setData(testData);
  myDrawer.draw();
}

function testDraw() {
  const context = document.getElementById('gameCanvas').getContext('2d');
  const backOfCard = new Image();
  backOfCard.src = '/static/cards_png/back.jpg';
  context.drawImage(backOfCard, 0, 0, 68, 100);
  backOfCard.src = '/static/cards_png/2C.png';
  context.drawImage(backOfCard, 200, 0, 85, 125);
}

function cardClick(index) {
  if (!playerSelections.includes(index)) {
    playerSelections.push(index);
  } else {
    for (var i = 0; i < playerSelections.length; i++) {
      if (playerSelections[i] == index) {
        playerSelections.splice(i, 1);
        break;
      }
    }
  }
  console.log(playerSelections);
}

function playButton() {
  socket.emit('make-move', {'userID': userID,
                            'selection': playerSelections});
  playerSelections.length = 0;
}

function clearButton() {
  playerSelections.length = 0;
}

function passButton() {
  socket.emit('make-move', {'userID': userID,
                            'selection': ['space']});
}

function takeBack() {
  socket.emit('make-move', {'userID': userID,
                            'selection': ['b']});
}
