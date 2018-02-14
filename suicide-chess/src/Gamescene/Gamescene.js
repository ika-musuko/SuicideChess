import React, { Component } from 'react'
import Board from '../Board/Board'
import './Gamescene.css'
import { observe } from '../Game'
import { pieceObserve } from '../Game'

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

      whiteTurn: true,

      whiteInCheck: false,

      blackInCheck: false,

      selectedPiece: null
    }
    observe(this.handlePieceMove.bind(this))
    pieceObserve(this.handlePieceSelect.bind(this))
  }

  handlePieceMove (pieces, changesMade) {
    
    if (this.state) {
      this.setState({
          ...pieces,
          selectedPiece: null,
          whiteTurn: changesMade ? !this.state.whiteTurn : this.state.whiteTurn,
      })
    }
  }

  handlePieceSelect (piece) {
    if(piece !== null && this.state.whiteTurn && piece.substring(0,5) === "white") {
      this.setState({
        selectedPiece: piece
      })
    } else if (piece !== null && !this.state.whiteTurn && piece.substring(0,5) === "black") {
      this.setState({
        selectedPiece: piece
      })
    }
   
  }

  render() {
    return (
      <div className="Gamescene"> 
        <h2>{this.state.whiteTurn ? "White's Turn" : "Black's Turn"}</h2>
        <Board state={this.state} selectedPiece={this.state.selectedPiece}/>
        <h2>{this.state.whiteInCheck ? "White is in check!" : this.state.blackInCheck ? "Black is in check!" : ""}</h2>
      </div>
    );
  }
}

export default gamescene;