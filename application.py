from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

num_conns = 0

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def message(data):
    print(data)
    send(data)

@socketio.on('connected')
def new_connection(data):
    num_conns += 1
    emit('assign_id', num_conns)

if __name__ == "__main__":
    socketio.run(app, debug=True)
