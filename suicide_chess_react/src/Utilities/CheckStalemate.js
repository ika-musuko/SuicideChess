import {getValidMoves} from './GetValidMoves'

export function checkStalemate (pieces, whiteTurn) {
  var newPieces = {};
  for(var piece in pieces) {
    if(pieces.hasOwnProperty(piece) && (piece.substring(0,6) === 'white_' || piece.substring(0,6) === 'black_'))[
      newPieces[piece] = pieces[piece]
    ]
  }
  newPieces['whiteTurn'] = whiteTurn;
  var moves = [];
  if(whiteTurn) {
    for(var piece in newPieces) {
      if (pieces.hasOwnProperty(piece) && piece.substring(0,6) === 'white_' && newPieces[piece].x !== -1) {
        var validMoves = getValidMoves(newPieces, piece)
        moves.push(...getValidMoves(newPieces, piece))
      }
    }
  } else {
    for(piece in newPieces) {
      if(pieces.hasOwnProperty(piece) && piece.substring(0,6) === 'black_' && newPieces[piece].x !== -1) {
        var validMoves = getValidMoves(newPieces, piece)
        moves.push(...getValidMoves(newPieces, piece))
      }
    }
  }
  if(moves.length > 0) {
    return false
  } else {
    return true
  }
}
