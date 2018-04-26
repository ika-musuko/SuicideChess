import React, { Component } from 'react'
import Board from '../Board/Board'
import './Gamescene.css'
import { observe } from '../Game'
import { pieceObserve } from '../Game'
import { getValidMoves } from '../Utilities/GetValidMoves'
import { movePiece } from '../Game'
import firebase from '../firebase'

class gamescene extends Component {
  constructor(props) {
    super(props)
    this.state = {
      black_knightA: { x: 1, y: 0 },
      black_knightB: { x: 6, y: 0 },
      black_bishopA: { x: 2, y: 0 },
      black_bishopB: { x: 5, y: 0 },
      black_rookA: { x: 0, y: 0 },
      black_rookB: { x: 7, y: 0 },
      black_queen: { x: 3, y: 0 },
      black_king: { x: 4, y: 0 },
      black_pawnA: { x: 0, y: 1, firstMove: true },
      black_pawnB: { x: 1, y: 1, firstMove: true },
      black_pawnC: { x: 2, y: 1, firstMove: true },
      black_pawnD: { x: 3, y: 1, firstMove: true },
      black_pawnE: { x: 4, y: 1, firstMove: true },
      black_pawnF: { x: 5, y: 1, firstMove: true },
      black_pawnG: { x: 6, y: 1, firstMove: true },
      black_pawnH: { x: 7, y: 1, firstMove: true },

      white_knightA: { x: 1, y: 7 },
      white_knightB: { x: 6, y: 7 },
      white_bishopA: { x: 2, y: 7 },
      white_bishopB: { x: 5, y: 7 },
      white_rookA: { x: 0, y: 7 },
      white_rookB: { x: 7, y: 7 },
      white_queen: { x: 3, y: 7 },
      white_king: { x: 4, y: 7 },
      white_pawnA: { x: 0, y: 6, firstMove: true },
      white_pawnB: { x: 1, y: 6, firstMove: true },
      white_pawnC: { x: 2, y: 6, firstMove: true },
      white_pawnD: { x: 3, y: 6, firstMove: true },
      white_pawnE: { x: 4, y: 6, firstMove: true },
      white_pawnF: { x: 5, y: 6, firstMove: true },
      white_pawnG: { x: 6, y: 6, firstMove: true },
      white_pawnH: { x: 7, y: 6, firstMove: true },
      validTiles: [],

      whiteTurn: true,

      whiteWin: false,

      blackWin: false,

      databaseRef: firebase.database().ref('games'),

      submitted: false,

      isWhite: false,
      username: '',
      otherUser: '',
      gameID: '',

      selectedPiece: null
    }
    observe(this.handlePieceMove.bind(this))
    pieceObserve(this.handlePieceSelect.bind(this))

    this.handleFormChange = this.handleFormChange.bind(this);
    this.handleSelectButton = this.handleSelectButton.bind(this);
  };

  handlePieceMove (pieces, changesMade) {
    if(this.state.submitted) {
      let blackWin = true
      let whiteWin = true
      for(var property in pieces) {
        if(pieces.hasOwnProperty(property)) {
          if(pieces[property].x !== -1) {
            if(property.substring(0,5) === "black") {
              blackWin = false;
            } else {
              whiteWin = false;
            }
          }
        }
      }

      if(blackWin || whiteWin) {
        this.setState({
          whiteWin: whiteWin,
          blackWin: blackWin,
        });
      }

      if(this.state && changesMade) {
        var gameData = pieces;
        gameData['whiteTurn'] = changesMade ? !this.state.whiteTurn : this.state.whiteTurn;
        var updates = {};
        updates['/games/' + this.state.gameID + '/gameData/'] = gameData;
        firebase.database().ref().update(updates);
        this.setState({
          validTiles: [],
          ...pieces,
          selectedPiece: null,
          whiteTurn: changesMade ? !this.state.whiteTurn : this.state.whiteTurn,
        });
      } else {
        this.setState({
          selectedPiece: null,
          validTiles: []
        });
      }
    }
  };

  handlePieceSelect (piece) {
    if(this.state.submitted) {
      if((this.state.isWhite && this.state.whiteTurn) || (!this.state.isWhite && !this.state.whiteTurn)) {
        let validTiles = getValidMoves(this.state, piece)
        if(piece !== null && this.state.isWhite && this.state.whiteTurn && piece.substring(0,5) === "white") {
          this.setState({
            validTiles: validTiles,
            selectedPiece: piece
          });
        } else if (piece !== null && !this.state.isWhite && !this.state.whiteTurn && piece.substring(0,5) === "black") {
          this.setState({
            validTiles: validTiles,
            selectedPiece: piece
          });
        }
      }
    }
  };

  handleFormChange (event) {
    this.setState({username: event.target.value});
  };

  handleSelectButton (event) {
    let a = this;
    var gameData = {};
    for(var property in a.state) {
      if(a.state.hasOwnProperty(property) && (property.substring(0,1) === 'w' || property.substring(0,1) === 'b')){
        gameData[property] = a.state[property];
      }
    }
    this.state.databaseRef.once('value').then(function(snapshot) {
      var games = snapshot.val();
      if(games === null) {
        var info = {
          user1: a.state.username,
          user2: '',
          gameData: gameData,
        };
        var gameID = a.state.databaseRef.push(info).key
        a.setState({
          username: a.state.username,
          isWhite: true,
          gameID: gameID,
          submitted: true,
        });
        var user2Joins = firebase.database().ref('/games/' + gameID);
        user2Joins.on('child_changed', function(snapshot) {
          user2Joins.off('child_changed');
          var gameListener = firebase.database().ref('/games/' + gameID + '/gameData/');
          gameListener.on('child_changed', function(snapshot) {
            if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
              console.log(snapshot.key);
              console.log(snapshot.val());
              var data = snapshot.val();
              data['piece'] = snapshot.key;
              movePiece(data);
            }
          });
          a.setState({
            otherUser: snapshot.val()
          });
        });
      } else {
        for(var property in games) {
          if(games.hasOwnProperty(property)) {
            if(games[property]['user2'] === '') {
              var postData ={
                user1: games[property]['user1'],
                user2: a.state.username,
                gameData: games[property]['gameData']
              }
              var updates = {};
              updates['/games/' + property] = postData;
              firebase.database().ref().update(updates);
              var gameListener = firebase.database().ref('/games/' + property + '/gameData/');
              gameListener.on('child_changed', function(snapshot) {
                if(snapshot.key.substring(0,6) === 'white_' || snapshot.key.substring(0,6) === 'black_'){
                  console.log(snapshot.key);
                  console.log(snapshot.val());
                  var data = snapshot.val();
                  data['piece'] = snapshot.key;
                  movePiece(data);
                }
              });
              a.setState({
                username: a.state.username,
                otherUser: games[property]['user1'],
                submitted: true,
                gameID: property,
              });
            }
          }
        }
      }
    })
  };

  render() {
    return (
      <div className="Gamescene">
        <h2>{this.state.blackWin ? "Black won!" : this.state.whiteWin ? "White won!" : this.state.whiteTurn ? (this.state.isWhite ? "Your Turn" : "Their Turn") : (this.state.isWhite ? "Their Turn" : "Your Turn")}</h2>
        {this.state.submitted ?
          <p> Username: {this.state.username}  Opponent: {this.state.otherUser}</p>
           :
          <form>
            Username: <input type="text" value={this.state.username} onChange= {this.handleFormChange}/>
            <button type="button" onClick={this.handleSelectButton}>Submit</button>
          </form>
        }
        <Board state={this.state} selectedPiece={this.state.selectedPiece} validTiles={this.state.validTiles}/>
      </div>
    );
  };
}

export default gamescene;
