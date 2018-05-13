import React, { Component } from 'react'
import './Board.css'
import Tile from '../Tile/Tile'
import {movePiece} from '../Game'
import { getPiece } from '../Utilities/GetPieceForSquare'

class board extends Component {
    handleSquareClick = (move) => {
        if(move.piece !== null){
            movePiece(move)
        }
    }

    renderSquare = (i) => {
        let x = i % 8
        let y = Math.floor(i / 8)
        let color = false
        if ((x + y) % 2 === 0){
            color = true
        }
        var greenTile = false
        for(var v = 0; v < this.props.validTiles.length; v++) {
            if(this.props.validTiles[v].x === x && this.props.validTiles[v].y === y) {
                greenTile = true
            }
        }
        return (
            <Tile
                x={x}
                y={y}
                key={8*y + x}
                color={color}
                requiredMove={this.checkIfRequiredMove(x,y)}
                flip={this.props.flip}
                click={this.handleSquareClick.bind(this, {piece: this.props.selectedPiece, x: x, y: y})}
            >
                <div>
                    {greenTile ?
                        <div className="move-indicator"></div>
                        :
                        null
                    }
                    {this.renderPiece(x,y)}
                </div>
            </Tile>
        )
    }

    checkIfRequiredMove = (x,y) => {
      var piece = getPiece(this.props, x, y)
      if(piece !== null) {
        return Object.keys(this.props.requiredMoves).includes(getPiece(this.props,x,y).key) && ((this.props.state.isWhite && this.props.state.whiteTurn) || (!this.props.state.isWhite && !this.props.state.whiteTurn))
      } else {
        return false
      }
    }

    renderPiece = (x, y) => {
        var piece = getPiece(this.props, x, y)
        if(piece !== null) {
        }
        return getPiece(this.props, x, y)
    }

    render () {
        let squares = []
        for (let i = 0; i < 64; i++) {
            squares.push(this.renderSquare(i))
        }
        return (
          <div>
            {this.props.flip ? (
              <div className="board-flipped">
                {squares}
              </div>
            ) : (
              <div className="board">
                {squares}
              </div>
            )}
          </div>
        );
    }
}

export default board;
