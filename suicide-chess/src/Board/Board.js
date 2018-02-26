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
        for(var i = 0; i < this.props.validTiles.length; i++) {
            if(this.props.validTiles[i].x === x && this.props.validTiles[i].y === y) {
                greenTile = true
            }
        }
        return (
            <Tile 
                x={x} 
                y={y} 
                key={8*y + x} 
                color={color}
                click={this.handleSquareClick.bind(this, {piece: this.props.selectedPiece, x: x, y: y})}
            >
                <div>
                    {greenTile ?
                        <div className="circle"></div>
                        :
                        null
                    }
                    {this.renderPiece(x,y)}
                </div>
            </Tile>
        )
    }

    renderPiece = (x, y) => {
        return getPiece(this.props, x, y)
    }

    render () {
        let squares = []
        for (let i = 0; i < 64; i++) {
            squares.push(this.renderSquare(i))
        }
        return (
            <div className="Board">
                {squares}
            </div>
        );
    }
}

export default board;