import React from 'react'
import Knight from '../Pieces/Knight'
import Queen from '../Pieces/Queen'
import Bishop from '../Pieces/Bishop'
import Rook from '../Pieces/Rook'
import King from '../Pieces/King'
import Pawn from '../Pieces/Pawn'

export function getPiece(pieceId) {
  if(pieceId === 'black_knightA') {
      return <Knight
      key={"black_knightA"}
      pieceKey={"black_knightA"}
      />
  } else if (pieceId === 'black_knightB'){
      return <Knight
      key={"black_knightB"}
      pieceKey={"black_knightB"}
      />
  } else if (pieceId === 'black_queen') {
      return <Queen
      key={"black_queen"}
      pieceKey={"black_queen"}
      />
  } else if (pieceId === 'black_king') {
      return <King
      key={"black_king"}
      pieceKey={"black_king"}
      />
  } else if (pieceId === 'black_bishopA') {
      return <Bishop
      key={"black_bishopA"}
      pieceKey={"black_bishopA"}
      />
  } else if (pieceId === 'black_bishopB') {
      return <Bishop
      key={"black_bishopB"}
      pieceKey={"black_bishopB"}
      />
  } else if (pieceId === 'black_rookA') {
      return <Rook
      key={"black_rookA"}
      pieceKey={"black_rookA"}
      />
  } else if (pieceId === 'black_rookB') {
      return <Rook
      key={"black_rookB"}
      pieceKey={"black_rookB"}
      />
  } else if (pieceId === 'black_pawnA') {
      return <Pawn
      key={"black_pawnA"}
      pieceKey={"black_pawnA"}
      />
  } else if (pieceId === 'black_pawnB') {
      return <Pawn
      key={"black_pawnB"}
      pieceKey={"black_pawnB"}
      />
  } else if (pieceId === 'black_pawnC') {
      return <Pawn
      key={"black_pawnC"}
      pieceKey={"black_pawnC"}
      />
  } else if (pieceId === 'black_pawnD') {
      return <Pawn
      key={"black_pawnD"}
      pieceKey={"black_pawnD"}
      />
  } else if (pieceId === 'black_pawnE') {
      return <Pawn
      key={"black_pawnE"}
      pieceKey={"black_pawnE"}
      />
  } else if (pieceId === 'black_pawnF') {
      return <Pawn
      key={"black_pawnF"}
      pieceKey={"black_pawnF"}
      />
  } else if (pieceId === 'black_pawnG') {
      return <Pawn
      key={"black_pawnG"}
      pieceKey={"black_pawnG"}
      />
  } else if (pieceId === 'black_pawnH') {
      return <Pawn
      key={"black_pawnH"}
      pieceKey={"black_pawnH"}
      />
  }

  //White pieces

  else if(pieceId === 'white_knightA') {
      return <Knight
      key={"white_knightA"}
      pieceKey={"white_knightA"}
      />
  } else if (pieceId === 'white_knightB'){
      return <Knight
      key={"white_knightB"}
      pieceKey={"white_knightB"}
      />
  } else if (pieceId === 'white_queen') {
      return <Queen
      key={"white_queen"}
      pieceKey={"white_queen"}
      />
  } else if (pieceId === 'white_king') {
      return <King
      key={"white_king"}
      pieceKey={"white_king"}
      />
  } else if (pieceId === 'white_bishopA') {
      return <Bishop
      key={"white_bishopA"}
      pieceKey={"white_bishopA"}
      />
  } else if (pieceId === 'white_bishopB') {
      return <Bishop
      key={"white_bishopB"}
      pieceKey={"white_bishopB"}
      />
  } else if (pieceId === 'white_rookA') {
      return <Rook
      key={"white_rookA"}
      pieceKey={"white_rookA"}
      />
  } else if (pieceId === 'white_rookB') {
      return <Rook
      key={"white_rookB"}
      pieceKey={"white_rookB"}
      />
  } else if (pieceId === 'white_pawnA') {
      return <Pawn
      key={"white_pawnA"}
      pieceKey={"white_pawnA"}
      />
  } else if (pieceId === 'white_pawnB') {
      return <Pawn
      key={"white_pawnB"}
      pieceKey={"white_pawnB"}
      />
  } else if (pieceId === 'white_pawnC') {
      return <Pawn
      key={"white_pawnC"}
      pieceKey={"white_pawnC"}
      />
  } else if (pieceId === 'white_pawnD') {
      return <Pawn
      key={"white_pawnD"}
      pieceKey={"white_pawnD"}
      />
  } else if (pieceId === 'white_pawnE') {
      return <Pawn
      key={"white_pawnE"}
      pieceKey={"white_pawnE"}
      />
  } else if (pieceId === 'white_pawnF') {
      return <Pawn
      key={"white_pawnF"}
      pieceKey={"white_pawnF"}
      />
  } else if (pieceId === 'white_pawnG') {
      return <Pawn
      key={"white_pawnG"}
      pieceKey={"white_pawnG"}
      />
  } else if (pieceId === 'white_pawnH') {
      return <Pawn
      key={"white_pawnH"}
      pieceKey={"white_pawnH"}
      />
  } else {
      return null
  }
}
