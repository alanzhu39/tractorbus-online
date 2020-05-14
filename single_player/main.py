"""
add players
start the rounds
keep track of scores
"""
from single_player.player import *
from single_player.round import *
if __name__ == '__main__':
    sheng_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    rank_ids = [0, 0, 0, 0]

    # todo: implement first draw
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

