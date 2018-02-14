import React from 'react'
import Knight from '../Pieces/Knight'
import Queen from '../Pieces/Queen'
import { selectPiece } from '../Game'

export function getPiece(props,x,y) {
    if(x === props.state.black_knightA.x && y === props.state.black_knightA.y) {
        return <Knight 
        key={"Black_KnightA"} 
        click={selectPiece.bind(this, "Black_KnightA")}
        selected={
            props.selectedPiece === "Black_KnightA" ? true : false
        }/>
    } else if (x === props.state.black_knightB.x && y === props.state.black_knightB.y){
        return <Knight 
        key={"Black_KnightB"} 
        click={selectPiece.bind(this, "Black_KnightB")} 
        selected={
            props.selectedPiece === "Black_KnightB" ? true : false
        }/>
    } else if (x === props.state.black_queen.x && y === props.state.black_queen.y) {
        return <Queen
        key={"Black_Queen"}
        click={selectPiece.bind(this, "Black_Queen")}
        selected= {
            props.selectedPiece === "Black_Queen" ? true : false
        }/>
    } else {
        return null
    }
}