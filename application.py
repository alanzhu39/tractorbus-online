from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, emit
from single_player.round import *
from single_player.player import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

testUI = False;

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def message(data):
    print(data)
    send(data)

@socketio.on('connected')
def new_connection(data):
    global num_conns
    emit('assign_id', num_conns)
    num_conns += 1
    if num_conns == 4 and not testUI:
        emit('game-start', 'Game started!', broadcast=True)
        start_game()

@socketio.on('test-event')
def test_func(data):
    print(type(data['stuff']))
    send(data['stuff'])

@socketio.on('make-move')
def make_move(move_data):
    if move_data['userID'] == r.get_current_player():
        if move_data['selection'] != ['b']:
            r.set_client_input(move_data['selection'])
    elif move_data['userID'] == r.get_last_player() and r.get_current_player() != 5:
        if move_data['selection'] == ['b']:
            r.set_take_back(True)
    emit('game-data', r.get_data())

@socketio.on('data-query')
def data_query(_):
    emit('game-data', r.get_data())

def start_game():
    global r
    sheng_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    rank_ids = [0, 0, 0, 0]

    zj_id = 0
    players = [Player("Adam", sheng_order[0]), Player("Andrew", sheng_order[0]),
               Player("Alan", sheng_order[0]), Player("Raymond", sheng_order[0])]
    players[zj_id].set_is_zhuang_jia(True)

    while True:
        r = Round(players)
        pts = r.play_round()

        if pts == 0:
            # increase trump rank of players[zj_id] and players[(zj_id+2)%4] by 3
            rank_ids[zj_id] += 3
            rank_ids[(zj_id + 2) % 4] += 3
            zj_id = (zj_id + 2) % 4
        elif pts < 40:
            # increase trump rank of players[zj_id] and players[(zj_id+2)%4] by 2
            rank_ids[zj_id] += 2
            rank_ids[(zj_id + 2) % 4] += 2
            zj_id = (zj_id + 2) % 4
        elif pts < 80:
            # increase trump rank of players[zj_id] and players[(zj_id+2)%4] by 1
            rank_ids[zj_id] += 1
            rank_ids[(zj_id + 2) % 4] += 1
            zj_id = (zj_id + 2) % 4
        else:
            num_shengs = (pts - 80) // 40
            # increase trump rank of players[(zj_id+1)%4] and players[(zj_id+3)%4] by num_shengs
            rank_ids[(zj_id + 1) % 4] += num_shengs
            rank_ids[(zj_id + 3) % 4] += num_shengs
            zj_id = (zj_id + 1) % 4

        for i in range(4):
            players[i].set_is_zhuang_jia(False)
            players[i].set_trump_rank(sheng_order[rank_ids[i]])
        players[zj_id].set_is_zhuang_jia(True)

        if rank_ids[zj_id] >= len(sheng_order):
            print(players[zj_id].get_name() + ' and ' + players[(zj_id + 2) % 4].get_name() + 'win!')
            break

if __name__ == "__main__":
    num_conns = 0
    r = None
    socketio.run(app, debug=True)
