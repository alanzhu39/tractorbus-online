class Card {

  constructor(rank, suit, ID=0, is_big_joker=False, is_small_joker=False) {
    this._rank = rank;
    this._suit = suit;
    this._ID = ID;
    this._isBJ = is_big_joker;
    this._isSJ = is_small_joker;
    this._isJ = is_big_joker || is_small_joker;
    if (this._rank == '5') {
      this._points = 5;
    } else if (this._rank == '10' || this._rank == 'K') {
      this._points = 10;
    } else {
      this._points = 0;
    }
  }

  toString() {
    if (this._isBJ) return 'BJo';
    if (this._isSJ) return 'SJo';
    return this._rank + this._suit;
  }
}

const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
const suits = ['clubs', 'diamonds', 'hearts', 'spades'];
module.exports = Card;
