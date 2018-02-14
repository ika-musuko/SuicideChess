import React from 'react'
import Knight from '../Pieces/Knight'
import Queen from '../Pieces/Queen'
import Bishop from '../Pieces/Bishop'
import Rook from '../Pieces/Rook'
import King from '../Pieces/King'
import Pawn from '../Pieces/Pawn'
import { selectPiece } from '../Game'

export function getPiece(props,x,y) {
    if(x === props.state.black_knightA.x && y === props.state.black_knightA.y) {
        return <Knight 
        key={"black_knightA"} 
        pieceKey={"black_knightA"}
        click={selectPiece.bind(this, "black_knightA")}
        selected={
            props.selectedPiece === "black_knightA" ? true : false
        }/>
    } else if (x === props.state.black_knightB.x && y === props.state.black_knightB.y){
        return <Knight 
        key={"black_knightB"}
        pieceKey={"black_knightB"} 
        click={selectPiece.bind(this, "black_knightB")} 
        selected={
            props.selectedPiece === "black_knightB" ? true : false
        }/>
    } else if (x === props.state.black_queen.x && y === props.state.black_queen.y) {
        return <Queen
        key={"black_queen"}
        pieceKey={"black_queen"}
        click={selectPiece.bind(this, "black_queen")}
        selected= {
            props.selectedPiece === "black_queen" ? true : false
        }/>
    } else if (x === props.state.black_king.x && y === props.state.black_king.y) {
        return <King
        key={"black_king"}
        pieceKey={"black_king"}
        click={selectPiece.bind(this, "black_king")}
        selected= {
            props.selectedPiece === "black_king" ? true : false
        }/>
    } else if (x === props.state.black_bishopA.x && y === props.state.black_bishopA.y) {
        return <Bishop
        key={"black_bishopA"}
        pieceKey={"black_bishopA"}
        click={selectPiece.bind(this, "black_bishopA")}
        selected= {
            props.selectedPiece === "black_bishopA" ? true : false
        }/>
    } else if (x === props.state.black_bishopB.x && y === props.state.black_bishopB.y) {
        return <Bishop
        key={"black_bishopB"}
        pieceKey={"black_bishopB"}
        click={selectPiece.bind(this, "black_bishopB")}
        selected= {
            props.selectedPiece === "black_bishopB" ? true : false
        }/>
    } else if (x === props.state.black_rookA.x && y === props.state.black_rookA.y) {
        return <Rook
        key={"black_rookA"}
        pieceKey={"black_rookA"}
        click={selectPiece.bind(this, "black_rookA")}
        selected= {
            props.selectedPiece === "black_rookA" ? true : false
        }/>
    } else if (x === props.state.black_rookB.x && y === props.state.black_rookB.y) {
        return <Rook
        key={"black_rookB"}
        pieceKey={"black_rookB"}
        click={selectPiece.bind(this, "black_rookB")}
        selected= {
            props.selectedPiece === "black_rookB" ? true : false
        }/>
    } else if (x === props.state.black_pawnA.x && y === props.state.black_pawnA.y) {
        return <Pawn
        key={"black_pawnA"}
        pieceKey={"black_pawnA"}
        click={selectPiece.bind(this, "black_pawnA")}
        selected= {
            props.selectedPiece === "black_pawnA" ? true : false
        }/>
    } else if (x === props.state.black_pawnB.x && y === props.state.black_pawnB.y) {
        return <Pawn
        key={"black_pawnB"}
        pieceKey={"black_pawnB"}
        click={selectPiece.bind(this, "black_pawnB")}
        selected= {
            props.selectedPiece === "black_pawnB" ? true : false
        }/>
    } else if (x === props.state.black_pawnC.x && y === props.state.black_pawnC.y) {
        return <Pawn
        key={"black_pawnC"}
        pieceKey={"black_pawnC"}
        click={selectPiece.bind(this, "black_pawnC")}
        selected= {
            props.selectedPiece === "black_pawnC" ? true : false
        }/>
    } else if (x === props.state.black_pawnD.x && y === props.state.black_pawnD.y) {
        return <Pawn
        key={"black_pawnD"}
        pieceKey={"black_pawnD"}
        click={selectPiece.bind(this, "black_pawnD")}
        selected= {
            props.selectedPiece === "black_pawnD" ? true : false
        }/>
    } else if (x === props.state.black_pawnE.x && y === props.state.black_pawnE.y) {
        return <Pawn
        key={"black_pawnE"}
        pieceKey={"black_pawnE"}
        click={selectPiece.bind(this, "black_pawnE")}
        selected= {
            props.selectedPiece === "black_pawnE" ? true : false
        }/>
    } else if (x === props.state.black_pawnF.x && y === props.state.black_pawnF.y) {
        return <Pawn
        key={"black_pawnF"}
        pieceKey={"black_pawnF"}
        click={selectPiece.bind(this, "black_pawnF")}
        selected= {
            props.selectedPiece === "black_pawnF" ? true : false
        }/>
    } else if (x === props.state.black_pawnG.x && y === props.state.black_pawnG.y) {
        return <Pawn
        key={"black_pawnG"}
        pieceKey={"black_pawnG"}
        click={selectPiece.bind(this, "black_pawnG")}
        selected= {
            props.selectedPiece === "black_pwnG" ? true : false
        }/>
    } else if (x === props.state.black_pawnH.x && y === props.state.black_pawnH.y) {
        return <Pawn
        key={"black_pawnH"}
        pieceKey={"black_pawnH"}
        click={selectPiece.bind(this, "black_pawnH")}
        selected= {
            props.selectedPiece === "black_pawnH" ? true : false
        }/>
    } else {
        return null
    }
}