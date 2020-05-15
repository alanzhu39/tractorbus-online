class Drawer {
  constructor(selected) {
    this.userID;
    this.selected = selected;
    this.data;
    this.cardHeight = 125;
    this.cardWidth = 85;
    this.cardDeltaX = 30;
    this.cardY = 600;
    this.backHeight = 100;
    this.backWidth = 68;
    this.backDelta = 15;
    this.boardHeight = 800;
    this.boardWidth = 1400;
    this.selectDelta = 20;
    this.playedDelta = 15;
    this.turnRadius = 45;
    this.ctx = document.getElementById('gameCanvas').getContext('2d');
  }

  setID(userID) {
    this.userID = userID;
  }

  setData(data) {
    this.data = data;
  }

  draw() {
    if (!this.data) {
      return;
    }
    this.ctx.clearRect(0, 0, this.boardWidth, this.boardHeight);
    this.drawPlayerCards();
    this.drawOpponents();
    this.drawPlayed();
    this.drawTurn();
    this.drawDeck();
    this.drawStats();
  }

  drawPlayerCards() {
    for (card of document.getElementsByClassname('playerCard')) {
      card.remove();
    }
    const myHand = this.data[(this.data['current_player'] + 4 - this.userID) % 4][0];
    for (var i = 0; i < myHand.length; i++) {
      const card = document.createElement('div');
      div.class = 'playerCard';
      div.onclick = `cardClick(${i})`;
      const yPos = (this.selected.includes(i)) ? this.cardY + this.selectDelta : this.cardY;
      div.style.top = String(yPos) + 'px';
      div.style.width = String(this.cardWidth) + 'px';
      div.style.height = String(this.cardHeight) + 'px';
      div.style.left = String((this.boardWidth - (myHand.length - 1)*this.cardDeltaX
                          - this.cardWidth)/2 + i*this.cardDeltaX) + 'px';
      div.style.visibility = "visible";
      div.style.zIndex = String(i);
      card.innerHTML = ("<img src='/static/cards_png/" + String(myHand[i]) + ".png' width='"
                  + String(this.cardWidth) + "' height='" + String(this.cardHeight) + "'/>");
      document.getElementById('playerWrapper').appendChild(card);
    }
  }

  drawOpponents() {
    const backOfCard = new Image();
    backOfCard.src = '/static/cards_png/back.jpg';
    const backOfCardHor = new Image();
    backofCardHor.src = '/static/cards_png/back-hor.jpg';
    // right
    let handLen = this.data[(this.data['current_player'] + 4 - this.userID + 1) % 4][0].length;
    for (var i = 0; i < handLen; i++) {
      const xPos = this.boardWidth - this.backHeight;
      const yPos = (570 - (handLen - 1)*this.backDelta - this.backWidth)/2 + i*this.backDelta;
      this.ctx.drawImage(backOfCardHor, xPos, yPos, this.backHeight, this.backWidth);
    }
    // across
    handLen = this.data[(this.data['current_player'] + 4 - this.userID + 2) % 4][0].length;
    for (var i = 0; i < handLen; i++) {
      const xPos = (this.boardWidth - (handLen - 1)*this.backDelta
                          - this.backWidth)/2 + i*this.backDelta;
      const yPos = 0;
      this.ctx.drawImage(backOfCardHor, xPos, yPos, this.backWidth, this.backHeight);
    }
    // left
    handLen = this.data[(this.data['current_player'] + 4 - this.userID + 3) % 4][0].length;
    for (var i = 0; i < handLen; i++) {
      const xPos = 0;
      const yPos = (570 - (handLen - 1)*this.backDelta - this.backWidth)/2 + i*this.backDelta;
      this.ctx.drawImage(backOfCardHor, xPos, yPos, this.backHeight, this.backWidth);
    }
  }

  drawPlayed() {
    const playedCard = new Image();
    // player
    let played = this.data[(this.data['current_player'] + 4 - this.userID) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = (this.boardWidth - (played.length - 1)*this.backDelta
                          - this.backWidth)/2 + i*this.backDelta;
      const yPos = this.cardY - this.turnRadius - this.playedDelta - this.backHeight;
      playedCard.src = `/static/cards_png/${played[i]}.png`;
      this.ctx.drawImage(playedCard, xPos, yPos, this.backWidth, this.backHeight);
    }
    // right
    played = this.data[(this.data['current_player'] + 4 - this.userID + 1) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = this.boardWidth - (played.length - 1)*this.backDelta - this.backWidth
                  - this.turnRadius - this.playedDelta + i*this.backDelta;
      const yPos = (this.backHeight + this.cardY - this.backHeight)/2;
      playedCard.src = `/static/cards_png/${played[i]}.png`;
      this.ctx.drawImage(playedCard, xPos, yPos, this.backWidth, this.backHeight);
    }
    // across
    played = this.data[(this.data['current_player'] + 4 - this.userID + 2) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = (this.boardWidth - (played.length - 1)*this.backDelta
                          - this.backWidth)/2 + i*this.backDelta;
      const yPos = this.backHeight + this.turnRadius + this.playedDelta;
      playedCard.src = `/static/cards_png/${played[i]}.png`;
      this.ctx.drawImage(playedCard, xPos, yPos, this.backWidth, this.backHeight);
    }
    // left
    played = this.data[(this.data['current_player'] + 4 - this.userID + 3) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = this.backHeight + this.playedDelta + i*this.backDelta;
      const yPos = (this.backHeight + this.cardY - this.backHeight)/2;
      playedCard.src = `/static/cards_png/${played[i]}.png`;
      this.ctx.drawImage(playedCard, xPos, yPos, this.backWidth, this.backHeight);
    }
  }

  drawTurn() {
    const xPos = [this.boardWidth/2, this.boardWidth-this.backHeight, this.boardWidth/2, this.backHeight];
    const yPos = [this.cardY, 570/2, this.backHeight, 570/2];
    const myIndex = (this.data['current_player'] + 4 - this.userID) % 4;
    this.ctx.fillStyle = "#FF0000";
    this.ctx.beginPath();
    this.ctx.arc(xPos[myIndex], yPos[myIndex],this.turnRadius,0,2.0*Math.PI);
    this.ctx.fill();
  }

  drawDeck() {
    if (this.data['di_pai']) {
      const backOfCard = new Image();
      backOfCard.src = '/static/cards_png/back.jpg';
      this.ctx.drawImage(backOfCard, 55, 570, this.backWidth, this.backHeight);
    }
  }

  drawStats() {
    scoreText = document.getElementsById('score');
    scoreText.innerHTML = "Attacker points: " + String(this.data['attacker_points']);
    suitText = document.getElementsById('trump-suit');
    suitText.innerHTML = "Trump suit: " + String(this.data['trump_suit']);
  }
}
