function writeMessage(text) {
  const parent = document.querySelector('#events');

  const el = document.createElement('li');
  el.innerHTML = text;

  parent.appendChild(el);
}

function testFunc() {
  sock.emit('test', 'test message');
}

const sock = io();

sock.on('message', writeMessage);
