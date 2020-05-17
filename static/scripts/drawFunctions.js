class Drawer {
  constructor(selections) {
    this.selections = selections;
    this.cardHeight = 125;
    this.cardWidth = 86;
    this.cardDeltaX = 30;
    this.cardY = 600;
    this.backHeight = 100;
    this.backWidth = 68.8;
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
    this.drawTurn();
    this.drawPlayerCards();
    this.drawOpponents();
    this.drawPlayed();
    this.drawDeck();
    this.drawStats();
  }

  drawPlayerCards() {
    for (var i = 0; i < 33; i++) {
      const myEl = document.getElementById(String(i));
      if (myEl) {
        myEl.remove();
      }
    }
    const myHand = this.data[this.userID][0];
    for (var i = 0; i < myHand.length; i++) {
      const card = document.createElement('div');
      card.className = 'playerCard';
      const j = i;
      card.onclick = () => {
        cardClick(j);
        const y = (this.selections.includes(j)) ? (this.cardY - this.selectDelta) : this.cardY;
        card.style.top = String(y) + 'px';
      };
      const yPos = (this.selections.includes(i)) ? (this.cardY - this.selectDelta) : this.cardY;
      card.style.top = String(yPos) + 'px';
      card.style.width = String(this.cardWidth) + 'px';
      card.style.height = String(this.cardHeight) + 'px';
      card.style.left = String((this.boardWidth - (myHand.length - 1)*this.cardDeltaX
                          - this.cardWidth)/2 + i*this.cardDeltaX) + 'px';
      card.style.visibility = "visible";
      card.style.zIndex = String(i);
      card.id = String(i);
      card.innerHTML = ("<img src=\"{{ url_for('static', filename='cards_png/" + String(myHand[i]) + ".png' width='"
                  + String(this.cardWidth) + "' height='" + String(this.cardHeight) + "'/>");
      document.body.appendChild(card);
    }
  }

  drawOpponents() {
    const backOfCard = new Image();
    backOfCard.src = "{{ url_for('static', filename='cards_png/back.jpg') }}";
    const backOfCardHor = new Image();
    backOfCardHor.src = "{{ url_for('static', filename='cards_png/back-hor.jpg') }}";
    // right
    let handLen = this.data[(this.userID + 1) % 4][0].length;
    for (var i = 0; i < handLen; i++) {
      const xPos = this.boardWidth - this.backHeight;
      const yPos = (570 - (handLen - 1)*this.backDelta - this.backWidth)/2 + i*this.backDelta;
      this.ctx.drawImage(backOfCardHor, xPos, yPos, this.backHeight, this.backWidth);
    }
    // across
    handLen = this.data[(this.userID + 2) % 4][0].length;
    for (var i = 0; i < handLen; i++) {
      const xPos = (this.boardWidth - (handLen - 1)*this.backDelta
                          - this.backWidth)/2 + i*this.backDelta;
      const yPos = 0;
      this.ctx.drawImage(backOfCardHor, xPos, yPos, this.backWidth, this.backHeight);
    }
    // left
    handLen = this.data[(this.userID + 3) % 4][0].length;
    for (var i = 0; i < handLen; i++) {
      const xPos = 0;
      const yPos = (570 - (handLen - 1)*this.backDelta - this.backWidth)/2 + i*this.backDelta;
      this.ctx.drawImage(backOfCardHor, xPos, yPos, this.backHeight, this.backWidth);
    }
  }
  drawPlayed() {
    const playedCard = new Image();
    // player
    let played = this.data[(this.userID) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = (this.boardWidth - (played.length - 1)*this.backDelta
                          - this.backWidth)/2 + i*this.backDelta;
      const yPos = this.cardY - this.turnRadius - this.playedDelta - this.backHeight;
      playedCard.src = `{{ url_for('static', filename='cards_png/${played[i]}.png') }}`;
      this.ctx.drawImage(playedCard, xPos, yPos, this.backWidth, this.backHeight);
    }
    // right
    played = this.data[(this.userID + 1) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = this.boardWidth - this.backHeight - (played.length - 1)*this.backDelta - this.backWidth
                  - this.turnRadius - this.playedDelta + i*this.backDelta;
      const yPos = (this.backHeight + this.cardY - this.backHeight)/2;
      playedCard.src = `{{ url_for('static', filename='cards_png/${played[i]}.png') }}`;
      this.ctx.drawImage(playedCard, xPos, yPos, this.backWidth, this.backHeight);
    }
    // across
    played = this.data[(this.userID + 2) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = (this.boardWidth - (played.length - 1)*this.backDelta
                          - this.backWidth)/2 + i*this.backDelta;
      const yPos = this.backHeight + this.turnRadius + this.playedDelta;
      playedCard.src = `{{ url_for('static', filename='cards_png/${played[i]}.png') }}`;
      this.ctx.drawImage(playedCard, xPos, yPos, this.backWidth, this.backHeight);
    }
    // left
    played = this.data[(this.userID + 3) % 4][1];
    for (var i = 0; i < played.length; i++) {
      const xPos = this.backHeight + this.turnRadius + this.playedDelta + i*this.backDelta;
      const yPos = (this.backHeight + this.cardY - this.backHeight)/2;
      playedCard.src = `{{ url_for('static', filename='cards_png/${played[i]}.png') }}`;
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
      backOfCard.src = "{{ url_for('static', filename='cards_png/back.jpg') }}";
      this.ctx.drawImage(backOfCard, 55, 570, this.backWidth, this.backHeight);
    }
  }

  drawStats() {
    const scoreText = document.getElementById('score');
    scoreText.innerHTML = "Attacker points: " + String(this.data['attacker_points']);
    const suitText = document.getElementById('trump-suit');
    suitText.innerHTML = "Trump suit: " + String(this.data['trump_suit']);
  }

  drawNewGame() {
    ctx.font = "42px Comic Sans MS";
    ctx.fillStyle = "red";
    ctx.textAlign = "center";
    ctx.fillText("Refresh the page to join new game!", this.boardWidth/2, this.boardHeight/2);
  }
}
