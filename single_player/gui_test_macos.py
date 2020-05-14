from single_player.client_macos import TractorClient
import pygame

my_client = TractorClient(True)

test_hand = list(my_client.deck_dict.keys())[:25]
test_played = list(my_client.deck_dict.keys())[25:27]
test_data = []
for i in range(4):
    test_data += [i, test_hand, test_played]
test_data += ['True', 'True', 'True', 'test_score', 'test_suit', '1']
my_client.set_data(test_data)

while True:
    for event in pygame.event.get():
        # quit if the quit button was pressed
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)
        elif event.type == pygame.KEYUP:
            print(event.key)
        my_client.update(True)