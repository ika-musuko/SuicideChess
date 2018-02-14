import React from 'react'
import Knight from '../Pieces/Knight'
import Queen from '../Pieces/Queen'
import Bishop from '../Pieces/Bishop'
import Rook from '../Pieces/Rook'
import King from '../Pieces/King'
import { selectPiece } from '../Game'

export function getPiece(props,x,y) {
    if(x === props.state.black_knightA.x && y === props.state.black_knightA.y) {
        return <Knight 
        key={"Black_KnightA"} 
        pieceKey={"Black_KnightA"}
        click={selectPiece.bind(this, "Black_KnightA")}
        selected={
            props.selectedPiece === "Black_KnightA" ? true : false
        }/>
    } else if (x === props.state.black_knightB.x && y === props.state.black_knightB.y){
        return <Knight 
        key={"Black_KnightB"}
        pieceKey={"Black_KnightB"} 
        click={selectPiece.bind(this, "Black_KnightB")} 
        selected={
            props.selectedPiece === "Black_KnightB" ? true : false
        }/>
    } else if (x === props.state.black_queen.x && y === props.state.black_queen.y) {
        return <Queen
        key={"Black_Queen"}
        pieceKey={"Black_Queen"}
        click={selectPiece.bind(this, "Black_Queen")}
        selected= {
            props.selectedPiece === "Black_Queen" ? true : false
        }/>
    } else if (x === props.state.black_king.x && y === props.state.black_king.y) {
        return <King
        key={"Black_King"}
        pieceKey={"Black_King"}
        click={selectPiece.bind(this, "Black_King")}
        selected= {
            props.selectedPiece === "Black_King" ? true : false
        }/>
    } else if (x === props.state.black_bishopA.x && y === props.state.black_bishopA.y) {
        return <Bishop
        key={"Black_BishopA"}
        pieceKey={"Black_BishopA"}
        click={selectPiece.bind(this, "Black_BishopA")}
        selected= {
            props.selectedPiece === "Black_BishopA" ? true : false
        }/>
    } else if (x === props.state.black_bishopB.x && y === props.state.black_bishopB.y) {
        return <Bishop
        key={"Black_BishopB"}
        pieceKey={"Black_BishopB"}
        click={selectPiece.bind(this, "Black_BishopB")}
        selected= {
            props.selectedPiece === "Black_BishopB" ? true : false
        }/>
    } else if (x === props.state.black_rookA.x && y === props.state.black_rookA.y) {
        return <Rook
        key={"Black_RookA"}
        pieceKey={"Black_RookA"}
        click={selectPiece.bind(this, "Black_RookA")}
        selected= {
            props.selectedPiece === "Black_RookA" ? true : false
        }/>
    } else if (x === props.state.black_rookB.x && y === props.state.black_rookB.y) {
        return <Rook
        key={"Black_RookB"}
        pieceKey={"Black_RookB"}
        click={selectPiece.bind(this, "Black_RookB")}
        selected= {
            props.selectedPiece === "Black_RookB" ? true : false
        }/>
    } else {
        return null
    }
}