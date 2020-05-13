const http = require('http');
const express = require('express');
const socketio = require('socket.io');
let PORT = process.env.PORT || 8080;

const app = express();

const clientPath = `${__dirname}/../client`;
console.log('Serving static from: ', clientPath);

app.use(express.static(clientPath));

const server = http.createServer(app);

const io = socketio(server);

// array to track connected sockets
const socks = [];

io.on('connection', (sock) => {
  socks.push(sock);
  const sockID = socks.length;
  console.log('Someone connected');
  sock.emit('message', socks.length);
})


server.on('error', (err) => {
  console.error('Server error: ', err);
});

server.listen(PORT, () => {
  console.log('Tractor server started on 8080');
});
