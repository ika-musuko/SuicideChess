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
      selectedPiece: null
    }
    observe(this.handleChange.bind(this))
    pieceObserve(this.handlePieceSelect.bind(this))
  }

  handleChange (pieces) {
    if (this.state) {
      this.setState({
          ...pieces,
          selectedPiece: null
      })
    }
  }

  handlePieceSelect (piece) {
    this.setState({
      selectedPiece: piece
    })
  }

  render() {
    return (
      <div className="Gamescene"> 
        <Board state={this.state} selectedPiece={this.state.selectedPiece}/>
      </div>
    );
  }
}

export default gamescene;