import React, { Component } from 'react'
import Board from '../Board/Board'
import './Gamescene.css'
import { observe } from '../Game'
import { pieceObserve } from '../Game'
import { getValidMoves } from '../Utilities/GetValidMoves'
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

      user1: '',

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
      let validTiles = getValidMoves(this.state, piece)
      if(piece !== null && this.state.whiteTurn && piece.substring(0,5) === "white") {
        this.setState({
          validTiles: validTiles,
          selectedPiece: piece
        });
      } else if (piece !== null && !this.state.whiteTurn && piece.substring(0,5) === "black") {
        this.setState({
          validTiles: validTiles,
          selectedPiece: piece
        });
      }
    }
  };

  handleFormChange (event) {
    this.setState({user1: event.target.value});
  };

  handleSelectButton (event) {
    let a = this;
    this.state.databaseRef.once('value').then(function(snapshot) {
      var games = snapshot.val();
      console.log(games);
      if(games === null) {
        var info = {
          whiteTurn: a.state.whiteTurn,
          user1: a.state.user1,
          gameData: [],
        }
        a.state.databaseRef.push(info);
      } else {
        for(var property in games) {
          if(games.hasOwnProperty(property)) {
            if(games.user1 === null) {
              
            }
          }
        }
      }
    })
  };

  render() {
    return (
      <div className="Gamescene">
        <h2>{this.state.blackWin ? "Black won!" : this.state.whiteWin ? "White won!" : this.state.whiteTurn ? "White's Turn" : "Black's Turn"}</h2>
        {this.state.submitted ? 
          <h2> Username: {this.state.user1}</h2>
           : 
          <form> 
            Username: <input type="text" name="FirstName" value={this.state.user1} onChange= {this.handleFormChange}/>
            <button type="button" onClick={this.handleSelectButton}>Submit</button>
          </form>
        }
        <Board state={this.state} selectedPiece={this.state.selectedPiece} validTiles={this.state.validTiles}/>
      </div>
    );
  };
}

export default gamescene;