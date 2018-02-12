import React, { Component } from 'react'
import './Board.css'
import Tile from '../Tile/Tile'
import Knight from '../Pieces/Knight'
import {movePiece} from '../Game'
import { selectPiece } from '../Game'

class board extends Component {
    handleSquareClick = (move) => {
        if(move.piece !== null){
            movePiece(move)
        }
    }

    renderSquare(i) {
        let x = i % 8
        let y = Math.floor(i / 8)
        let color = false
        if ((x + y) % 2 === 0){
            color = true
        }
        return (
            <Tile x={x} y={y} key={8*y + x} color={color} click={this.handleSquareClick.bind(this, {piece: this.props.selectedPiece, x: x, y: y})}>{this.renderPiece(x,y)}</Tile>
        )
    }

    renderPiece(x, y) {
        if(x === this.props.state.black_knightA.x && y === this.props.state.black_knightA.y) {
            return <Knight 
            key={"Black_KnightA"} 
            click={selectPiece.bind(this, "Black_KnightA")} 
            selected={
                this.props.selectedPiece === "Black_KnightA" ? true : false
            }/>
        } else if (x === this.props.state.black_knightB.x && y === this.props.state.black_knightB.y){
            return <Knight 
            key={"Black_KnightB"} 
            click={selectPiece.bind(this, "Black_KnightB")} 
            selected={
                this.props.selectedPiece === "Black_KnightB" ? true : false
            }/>
        } else {
            return null
        }
    }

    render () {
        let squares = []
        for (let i = 0; i < 64; i++) {
            squares.push(this.renderSquare(i))
        }
        // for(let i = 0; i < 8; i++ ) {
        //     for (let j = 0; j < 8; j++) {
        //         let color = false;
        //         if((i + j) % 2 === 0) {
        //             color = true;
        //         }
        //         if(j === this.state.pieces.black_knight.x && i === this.state.pieces.black_knight.y) {
        //             var piece = <Knight key={"Black_Knight"}/>
        //             squares.push(<Tile 
        //                 x={j} 
        //                 y={i} 
        //                 key={8*i+j} 
        //                 color={color} 
        //                 piece={piece}
        //                 onClick={() => this.handleSquareClick(j,i)}/>)
        //         } else {
        //             squares.push(<Tile x={j} y={i} key={8*i+j} color={color} click={this.handleSquareClick.bind(this, j, i)}/>)
        //         }
        //     }
        // }
        return (
            <div className="Board">
                {squares}
            </div>
        );
    }
}

export default board;