import React, { Component } from 'react'
import Board from '../Board/Board'
import './Gamescene.css'
import { observe } from '../Game'
import { pieceObserve } from '../Game'

class gamescene extends Component {
  constructor(props) {
    super(props)
    console.log(props)
    this.state = {
      black_knightA: { x: 2, y: 0 },
      black_knightB: { x: 5, y: 0 },
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