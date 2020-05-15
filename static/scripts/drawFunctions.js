class Drawer {
  constructor() {
    this.data;
  }

  setData(data) {
    this.data = data;
  }

  draw() {
    if (!this.data) {
      return;
    }
    self.drawHands();
    self.drawButtons();
    self.drawTurn();
    self.drawDeck();
    self.drawStats();
  }

  drawHands() {

  }

  drawButtons() {

  }

  drawTurn() {

  }

  drawDeck() {
    if (this.data['di_pai']) {
      
    }
  }

  drawStats() {
    scoreText = document.getElementsById('score');
    scoreText.innerHTML = "Attacker points: " + String(this.data['attacker_points']);
    suitText = document.getElementsById('trump-suit');
    suitText.innerHTML = "Trump suit: " + String(this.data['trump_suit']);
  }
}
